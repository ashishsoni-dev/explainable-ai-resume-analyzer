# Main entry point: loads data, processes resumes, and ranks candidates
import sys
import logging
from colorama import Fore,Style
from parser import extract_text_from_pdf
from matcher import extract_keywords,compute_tfidf
from preprocessor import process_text
from config_loader import load_config
from semantic import compute_semantic_similarity
from logger import setup_logger
setup_logger()

# Loads configuration and initialize skill weights
config = load_config()

HARD_SKILLS = set(config["skills"]["hard_skills"])
SOFT_SKILLS = set(config["skills"]["soft_skills"])
MID_SKILLS = set(config["skills"]["mid_skills"])
CORE_SKILLS = {"python", "sql", "javascript", "html"}

HARD_WEIGHT = config["weights"]["hard_skill"]
SOFT_WEIGHT = config["weights"]["soft_skill"]
DEFAULT_WEIGHT = config["weights"]["default"]

SECTION_WEIGHTS = config["section_weights"]


# ============================Helper Functions============================

# Detects candidate role based on skill signals (backend/frontend/ml)
def detect_role(words):
    backend_score = 0
    frontend_score = 0
    ml_score = 0

    # backend signals
    for w in ["api", "backend", "sql", "database", "flask", "django"]:
        if w in words:
            backend_score += 1

    # frontend signals
    for w in ["react", "frontend", "css", "html"]:
        if w in words:
            frontend_score += 1

    # ml signals
    for w in ["machine_learning", "ml", "data"]:
        if w in words:
            ml_score += 1

    # decision
    if backend_score >= frontend_score and backend_score >= ml_score:
        return "Backend Developer"
    elif frontend_score >= backend_score:
        return "Frontend Developer"
    elif ml_score > 0:
        return "ML Engineer"
    else:
        return "General Developer"
    

# Generate suggestions based on missing and weak skills
def suggest_skills(missing_skills, matched_skills, role):
    suggestions = []

    critical_skills = {"python", "sql", "api"}
    bonus_skills = {"docker", "aws", "ci", "cd"}

    # suggestions based on missing skills
    for skill in missing_skills:
        if skill in critical_skills:
            suggestions.append(f"Add {skill.upper()} (critical)")
        elif skill in bonus_skills:
            suggestions.append(f"Add {skill.upper()} (bonus)")
        else:
            suggestions.append(f"Add {skill}")

    # only suggest improvement if skill is weak or absent
    if role == "Backend Developer":
        if "api" not in matched_skills and "api" in missing_skills:
            suggestions.append("Add REST API experience (high impact)")
        elif len(matched_skills) <= 2:
            suggestions.append("Improve backend project depth (medium impact)")

    return suggestions


# Counts frequency of each word
def count_frequency(words):
    freq = {}
    for word in words:
        freq[word] = freq.get(word,0)+1
    return freq


# Extracting different sections (skills, experience, etc.) from resume text
def get_skills_section(text):
    text = " ".join(text) if isinstance(text, list) else text

    section_names = ["skills", "experience", "projects", "education"]

    # finding positions of sections
    found_sections = []
    for section in section_names:
        pos = text.find(section)
        if pos != -1:
            found_sections.append((section, pos))

    # sorting by position in text
    found_sections.sort(key=lambda x: x[1])

    # extracting sections using boundaries
    extracted_sections = {}

    for i in range(len(found_sections)):
        section, start = found_sections[i]

        # end = start of next section
        if i + 1 < len(found_sections):
            end = found_sections[i + 1][1]
        else:
            end = len(text)

        extracted_sections[section] = text[start:end].strip()

    return extracted_sections


# Assigning weight to skill based on type (hard/mid/soft)
def get_skill_weight(word):
    if word in HARD_SKILLS:
        return HARD_WEIGHT
    elif word in MID_SKILLS:
        return 0.2   # lower than hard akills
    elif word in SOFT_SKILLS:
        return SOFT_WEIGHT
    else:
        return DEFAULT_WEIGHT
    

# ============================functions ends here============================

synonyms = {
    "js" : "javascript",
    "py" : "python",
    "c++" : "cpp"
}


if len(sys.argv) < 3:
    print(Fore.CYAN + "Usage: python main.py <resume1> <resume2> ... <job file>")
    print(Style.RESET_ALL)
    sys.exit()

resume_files = sys.argv[1:-1]
job_file = sys.argv[-1]

# Load and validate job description file
try:
    with open(job_file,"r") as file:
        job_discription = file.read()

    if not job_discription.strip():
        logging.error("Job description is empty")
        print("❌ Job description is empty")
        sys.exit()

except FileNotFoundError:
    logging.error("Job File Not Found!")
    print("Job File Not Found!")
    sys.exit()


logging.info("Job Description and Resume loaded Successfully!")

# Processing job description into structured keywords
job_words = process_text(job_discription, synonyms)

if not job_words:
    logging.error("Job processing failed")
    print("❌ Job description processing failed")
    sys.exit()

job_freq = count_frequency(job_words)
job_keywords = extract_keywords(job_words, min_freq=1)

if not job_keywords:
    logging.warning("No keywords found in job description")
    print("⚠️ No relevant job skills detected")
    sys.exit()

results = []

# Process each resume and compute match score
for resume_path in resume_files:
    resume_text = extract_text_from_pdf(resume_path)

    if not resume_text:
        logging.warning(f"Skipping {resume_path} (Empty or Unreadable)")
        continue

    resume_words = process_text(resume_text, synonyms)

    if not resume_words:
        logging.warning(f"Skipping {resume_path} (Processing Failed)")
        continue

    resume_freq = count_frequency(resume_words)
    resume_keywords = extract_keywords(resume_words, 1)

    if not resume_keywords:
        logging.warning(f"No Keywords in {resume_path}")
        continue

   
    filtered_job_freq = {word: job_freq.get(word, 0) for word in job_keywords}
    filtered_resume_freq = {word: resume_freq.get(word, 0) for word in job_keywords}

    tfidf_scores = compute_tfidf(filtered_job_freq, filtered_resume_freq)

    resume_sections = get_skills_section(resume_text)

    total_score = 0
    matched_score = 0

    resume_word_set = set(resume_words)
    role = detect_role(resume_words)

    # Calculate TF-IDF based relvance score
    for word, base_score in tfidf_scores.items():

        skill_weight = get_skill_weight(word)

        section_multiplier = 1.0

        for section, content in resume_sections.items():
            if word in content:
                section_multiplier = SECTION_WEIGHTS.get(section, 1.0)
                break

        final_score = base_score * skill_weight * section_multiplier

        if word not in HARD_SKILLS and word not in MID_SKILLS:
            continue

        total_score += final_score

        freq = resume_freq.get(word, 0)

        if freq > 0:
            matched_score += final_score
            if freq > 1:
                matched_score += final_score * 0.2

            if word in CORE_SKILLS:
                matched_score += final_score * 0.5
    

    filtered_words = [word for word in tfidf_scores if word in HARD_SKILLS or word in MID_SKILLS]

    ALL_SKILLS = HARD_SKILLS.union(MID_SKILLS)

    matched_skills = [
        word for word in job_keywords
        if word in ALL_SKILLS and resume_freq.get(word, 0) > 0
    ]

    missing_skills = [
        word for word in job_keywords
        if word in ALL_SKILLS and resume_freq.get(word, 0) == 0
    ]


    suggestions = suggest_skills(missing_skills, matched_skills, role)

    base_score = (matched_score / (len(filtered_words) + 1)) * 35
    

    total_keywords = len(filtered_words)

    matched_keywords = sum(1 for word in filtered_words if resume_freq.get(word, 0) > 0)

    coverage = matched_keywords / total_keywords if total_keywords > 0 else 0
    
    match_percentage = base_score * (0.7 + 0.3 * coverage)
    unique_skill_count = len([word for word in resume_word_set if word in HARD_SKILLS])

    diversity_bonus = min(unique_skill_count * 1.5, 15)

    match_percentage += diversity_bonus

    extra_skills = {"aws", "docker", "microservices", "system", "design", "scalable"}

    extra_bonus = sum(1 for word in resume_words if word in extra_skills)

    match_percentage += min(extra_bonus * 2, 10)
    # stronger experience detection
    experience_years_keywords = {"year", "years"}

    experience_bonus = 0

    # detecting years
    for word in resume_words:
        if word.isdigit():
            years = int(word)
            if years >= 5:
                experience_bonus += 15
            elif years >= 2:
                experience_bonus += 8

    strong_experience_words = {"led", "architected", "designed", "optimized"}

    strong_exp_count = sum(1 for word in resume_words if word in strong_experience_words)

    experience_bonus += min(strong_exp_count * 2, 10)

    match_percentage += experience_bonus

    CORE_REQUIRED = {"python", "sql"}

    core_matches = sum(1 for skill in CORE_REQUIRED if resume_freq.get(skill, 0) > 0)

    if core_matches == 0:
        match_percentage = 0
    elif core_matches == 1:
        match_percentage *= 0.4

    semantic_score = compute_semantic_similarity(job_discription, resume_text)
    semantic_weight = (semantic_score - 0.5) * 20
    match_percentage += semantic_weight
    match_percentage = max(match_percentage, 0)
    match_percentage = int(match_percentage)
    if core_matches == 2:
        tier = 2   # strong candidate
    elif core_matches == 1:
        tier = 1   # partial
    else:
        tier = 0   # reject

    results.append((
        resume_path,
        match_percentage,
        tier,
        matched_skills,
        missing_skills,
        role,
        suggestions
    ))

# Normalize and rank candidates
results.sort(key=lambda x: (x[2], x[1]), reverse=True)
if results:
    max_score = results[0][1]
    normalized_results = []
    for resume, score, tier, matched, missing, role,suggestions in results:
        normalized_score = (score / max_score) * 100 if max_score > 0 else 0
        
        normalized_results.append((
            resume,
            int(normalized_score),
            matched,
            missing,
            role,
            suggestions
        ))

    results = normalized_results
# Displays final ranked results
print("\n🏆 Candidate Ranking:\n")

for i, (resume, score, matched, missing, role, suggestions) in enumerate(results, start=1):
    print(f"{i}. {resume} → {score}%")
    
    print(f"   📌 Role: {role}")
    
    print(f"   ✅ Matched Skills: {', '.join(matched) if matched else 'None'}")
    
    print(f"   ❌ Missing Skills: {', '.join(missing) if missing else 'None'}")
    
    print(f"   💡 Suggestions:")
    if suggestions:
        for s in suggestions[:3]:
            print(f"      - {s}")
        print()
    else:
        print(f"      - Strong match for this role")
        print()
