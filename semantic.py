# Semantic similarity using sentence transformers model
from sentence_transformers import SentenceTransformer,util
import os
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import logging
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)

# Loading pretrained sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-V2')

# Computing semantic similarity score between job and resume
def compute_semantic_similarity(job_text,resume_text):
    job_embedding = model.encode(job_text,convert_to_tensor=True, show_progress_bar=False)
    resume_embedding = model.encode(resume_text,convert_to_tensor=True, show_progress_bar=False)

    similarity = util.cos_sim(job_embedding,resume_embedding)

    return float(similarity[0][0])