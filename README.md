# AI Resume Matcher

This project is an AI-based resume screening system designed to evaluate and rank candidates against a given job description. It combines natural language processing techniques with structured scoring to provide a more meaningful assessment than simple keyword matching.

The goal is to assist in identifying suitable candidates by analyzing both the presence of relevant skills and the overall contextual similarity between resumes and job requirements.

---

## Overview

The system processes a job description and multiple resumes, extracts relevant information, and produces a ranked list of candidates. It considers not only keyword matches but also the importance of skills, their frequency, and where they appear within the resume.

---

## Key Features

* Extraction of text from PDF resumes
* Text cleaning and normalization using NLP techniques
* Keyword and skill identification
* Weighted scoring system based on skill types and resume sections
* TF-IDF based relevance scoring
* Semantic similarity using transformer-based models
* Role prediction (e.g., Backend Developer, Frontend Developer, ML Engineer)
* Identification of missing skills with actionable suggestions

---

## How It Works

1. The job description is processed to extract important keywords
2. Each resume is parsed and preprocessed
3. Skills and keywords are identified and normalized
4. TF-IDF scores are calculated to measure relevance
5. Additional weights are applied based on:

   * Skill categories (hard, soft, mid-level)
   * Resume sections (experience, projects, skills, education)
6. A semantic similarity score is computed using a transformer model
7. A final score is generated and candidates are ranked accordingly

---

## Installation

Clone the repository:

```bash id="a1d9k3"
git clone https://github.com/YOUR_USERNAME/AI-Resume-Matcher.git
cd AI-Resume-Matcher
```

Install dependencies:

```bash id="b7f2q1"
pip install -r requirements.txt
```

---

## Usage

Run the program with one or more resumes and a job description file:

```bash id="c4m8x2"
python main.py resume1.pdf resume2.pdf job_description.txt
```

---

## Example Output

```bash id="d9r6p0"
Candidate Ranking:

1. resume1.pdf → 92%
   Role: Backend Developer
   Matched Skills: python, sql, api
   Missing Skills: docker, aws
   Suggestions:
      - Add DOCKER (bonus)
      - Add AWS (bonus)
```

---

## Technologies Used

* Python
* NLTK for text processing
* PDFPlumber for PDF parsing
* Sentence Transformers for semantic similarity
* TF-IDF for relevance scoring

---

## Project Structure

```bash id="e2k7w9"
main.py            # Application entry point
parser.py          # PDF text extraction
cleaner.py         # Text cleaning utilities
preprocessor.py    # Preprocessing pipeline
matcher.py         # Keyword extraction and TF-IDF
semantic.py        # Semantic similarity computation
config_loader.py   # Configuration handling
logger.py          # Logging setup
config.json        # Skill weights and configuration
```

---

## Future Enhancements

* Web-based interface for easier interaction
* Resume upload and visualization dashboard
* Improved skill extraction using advanced NLP models
* Integration with job listing platforms

---

## License

This project is released under the MIT License.

---

## Author

Your Name
