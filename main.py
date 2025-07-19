from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

app = FastAPI()


# Define the data models for the request and response
class WorkerProfile(BaseModel):
    skills: str


class JobPosting(BaseModel):
    id: int
    required_skills: str


class RecommendationRequest(BaseModel):
    worker_profile: WorkerProfile
    job_postings: List[JobPosting]


class RecommendationResponse(BaseModel):
    ranked_job_ids: List[int]


@app.post("/recommendations/jobs", response_model=RecommendationResponse)
def get_job_recommendations(request: RecommendationRequest):
    # 1. Create a list of all skill texts (documents)
    documents = [request.worker_profile.skills or ""]
    job_ids = []
    for job in request.job_postings:
        documents.append(job.required_skills or "")
        job_ids.append(job.id)

    # ** THE FIX: Check if there is anything to process **
    # If there are no jobs or all documents are empty, return early.
    if not any(documents) or len(documents) < 2:
        return RecommendationResponse(ranked_job_ids=[])

    # 2. Use TF-IDF to convert the text into numerical vectors
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(documents)
    except ValueError:
        # This handles the "empty vocabulary" error if all words are stop words
        return RecommendationResponse(ranked_job_ids=[])

    # 3. Calculate cosine similarity
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # 4. Rank the jobs
    ranked_jobs = sorted(zip(job_ids, cosine_similarities), key=lambda item: item[1], reverse=True)
    ranked_ids = [job_id for job_id, score in ranked_jobs if score > 0]

    return RecommendationResponse(ranked_job_ids=ranked_ids)
