import spacy
from sentence_transformers import SentenceTransformer, util

# Load NLP models
spacy_model = spacy.load("en_core_web_sm")
bert_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_similarity(resume_text, job_description):
    """
    Computes semantic similarity score between resume and job description.

    Parameters:
        resume_text (str): Raw text extracted from resume
        job_description (str): Job description input

    Returns:
        float: Similarity score (0.0 to 1.0)
    """
    embeddings = bert_model.encode([resume_text, job_description], convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1])
    return float(similarity)

# 🧪 Run this file directly to test
if __name__ == "__main__":
    resume_sample = """
    John Doe is a data scientist with experience in Python, machine learning, NLP, and data analysis.
    Worked on classification models, data cleaning, and visualization.
    """
    
    job_desc_sample = """
    We are looking for a data scientist skilled in Python, NLP, and machine learning for model building.
    """

    score = get_similarity(resume_sample, job_desc_sample)
    print(f"Match Score: {score:.2f}")
