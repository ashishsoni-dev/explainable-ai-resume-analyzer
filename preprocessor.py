# Text preprocessing pipeline: cleaning → lemmatizing → normalization
from cleaner import clean_text,detect_phrases,lemmatize_text

# Replaces shorthand words using synonyms mapping (ex:- js to javascript)
def normalize_words(words,synonyms):
    normalized = []
    for word in words:
        if word in synonyms:
            normalized.append(synonyms[word])
        else:
            normalized.append(word)
    return normalized

# Full text processing pipeline returning list of normalized words
def process_text(text,synonyms):
    text = clean_text(text)
    text = lemmatize_text(text)
    text = detect_phrases(text)

    words = text.split()

    words = normalize_words(words,synonyms)
    return words