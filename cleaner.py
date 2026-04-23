# Text cleaning and normalization utilities for resumes/job descriptions
import re
from nltk.stem import WordNetLemmatizer

# Cleaning raw text: lowercase, fix spaced words, remove symbols and numbers
def clean_text(text):
    text = text.lower()
    # fixing spaced words which usually appears in informated files
    text = text.replace("s k i l l s", "skills")
    text = text.replace("e x p e r i e n c e", "experience")
    text = text.replace("e d u c a t i o n", "education")
    text = text.replace("l a n g u a g e", "language")
    text = text.replace("r e f e r e n c e s", "references")
    text = text.replace("apis", "api")
    # to remove symbols
    text = re.sub(r"[^\w\s]"," ",text)
    # to remove numbers
    text = re.sub(r"\d+"," ",text)

    text = " ".join(text.split())
    return text

lemmatizer = WordNetLemmatizer()
# Converting words to it's base form (ex., running to run)
def lemmatize_text(text):
    words = text.split()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(lemmatized_words)

# Detecting important multi-word phrases and joining them with underscore
def detect_phrases(text):
    phrases = [
        "machine learning",
        "data science",
        "web development",
        "deep learning",
        "artificial intelligence",
        "software engineering",
        "data analysis",
        "backend development",
        "frontend development"
    ]

    for phrase in phrases:
        if phrase in text:
            text = text.replace(phrase,phrase.replace(" ","_"))

    return text
