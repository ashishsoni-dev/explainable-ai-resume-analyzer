# Keyword extraction and TF-IDF scoring logic
import math

VALID_SKILL_HINTS = {
    "python", "java", "sql", "html", "css", "javascript",
    "react", "node", "api", "django", "flask", "ml"
}

NON_SKILL_WORDS = {
    "demand", "require", "required", "need", "want",
    "ability", "knowledge", "understanding",
    "responsibility", "role", "work", "team"
}

# Extracting meaningful keywords based on frequency and filters
def extract_keywords(words,min_freq=2):
    GENERIC_SKILLS = {"backend", "frontend", "database"}
    stopwords = {
        "with", "that", "this", "from", "have", "were", "been",
        "need", "years", "and", "the", "for", "are",
        "one","two","three","four","five","six","seven","eight","nine",
        "ten"
    }
    freq={}
    for word in words:
        if not word.replace("_","").isalpha():
            continue
        if len(word) <= 2:
            continue
        if word in stopwords:
            continue
        freq[word] = freq.get(word,0)+1

    keywords = [
    word for word, count in freq.items()
    if count >= min_freq
    and word not in GENERIC_SKILLS
    and (
            word in VALID_SKILL_HINTS
            or (
                len(word) > 4
                and word not in NON_SKILL_WORDS
                and not word.endswith(("ion", "ment", "ness"))
            )
        )
    ]

    return keywords


# Computing TF-IDF scores between job description and resume
def compute_tfidf(job_freq,resume_freq):
    scores = {}
    all_words = set(job_freq.keys())
    
    N = 2
    for word in all_words:
        # tf_job = job_freq.get(word, 0)
        tf_resume = resume_freq.get(word, 0)
        if tf_resume == 0:
            scores[word] = 0
            continue
        
        tf = 1 + math.log(tf_resume)

        df = 0
        if word in job_freq:
            df += 1
        if word in resume_freq:
            df += 1

        idf = math.log((N + 1)/(df + 1))+1
        scores[word] = tf*idf

    return scores
        
