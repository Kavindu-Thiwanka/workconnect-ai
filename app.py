# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
import re
import logging
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="WorkConnect AI Recommendation Service",
    description="AI-powered job recommendation service using NLP and machine learning",
    version="1.0.0"
)

# Download NLTK data on startup
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    logger.info("Downloading NLTK stopwords...")
    nltk.download("stopwords", quiet=True)

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    logger.info("Downloading NLTK punkt tokenizer...")
    nltk.download("punkt", quiet=True)

# Get English stopwords
ENGLISH_STOPWORDS = set(stopwords.words("english"))

# Pydantic models matching the backend DTOs
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

def preprocess_text(text: str) -> str:
    """
    Preprocess text data for NLP analysis.
    
    Args:
        text: Raw text input
        
    Returns:
        Preprocessed text string
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove non-alphanumeric characters (keep spaces)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    
    # Replace multiple spaces with single space
    text = re.sub(r"\s+", " ", text)
    
    # Split into words and filter out stopwords
    words = text.split()
    filtered_words = [word for word in words if word not in ENGLISH_STOPWORDS and len(word) > 2]
    
    return " ".join(filtered_words)

def calculate_similarity_scores(worker_skills: str, job_postings: List[JobPosting]) -> List[tuple]:
    """
    Calculate cosine similarity between worker profile and job postings.
    
    Args:
        worker_skills: Preprocessed worker skills string
        job_postings: List of job postings with required skills
        
    Returns:
        List of tuples (job_id, similarity_score)
    """
    if not worker_skills.strip() or not job_postings:
        logger.warning("Empty worker skills or no job postings provided")
        return []
    
    # Prepare documents for vectorization
    documents = [worker_skills]
    job_ids = []
    
    for job in job_postings:
        processed_skills = preprocess_text(job.required_skills)
        documents.append(processed_skills)
        job_ids.append(job.id)
    
    # Check if we have meaningful content to process
    if len(documents) < 2 or not any(doc.strip() for doc in documents[1:]):
        logger.warning("No meaningful job content to process")
        return []
    
    try:
        # Create TF-IDF vectorizer with optimized parameters
        vectorizer = TfidfVectorizer(
            max_features=1000,  # Limit vocabulary size
            ngram_range=(1, 2),  # Include unigrams and bigrams
            min_df=1,  # Minimum document frequency
            stop_words=None  # We already preprocessed stopwords
        )
        
        # Fit and transform documents
        tfidf_matrix = vectorizer.fit_transform(documents)
        
        # Calculate cosine similarity between worker profile and all jobs
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        
        # Create list of (job_id, similarity_score) tuples
        job_similarities = list(zip(job_ids, similarities))
        
        logger.info(f"Calculated similarities for {len(job_similarities)} jobs")
        return job_similarities
        
    except ValueError as e:
        logger.error(f"Error in TF-IDF vectorization: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in similarity calculation: {str(e)}")
        return []

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "WorkConnect AI Recommendation Service is running",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "service": "WorkConnect AI Recommendation Service",
        "nltk_data": {
            "stopwords": "available",
            "punkt": "available"
        }
    }

@app.post("/recommendations/jobs", response_model=RecommendationResponse)
async def get_job_recommendations(request: RecommendationRequest):
    """
    Get job recommendations based on worker profile and available jobs.
    
    Args:
        request: RecommendationRequest containing worker profile and job postings
        
    Returns:
        RecommendationResponse with ranked job IDs
        
    Raises:
        HTTPException: If request validation fails or processing error occurs
    """
    try:
        logger.info(f"Processing recommendation request for {len(request.job_postings)} jobs")
        
        # Validate input
        if not request.worker_profile or not request.worker_profile.skills:
            logger.warning("Empty worker profile or skills")
            return RecommendationResponse(ranked_job_ids=[])
        
        if not request.job_postings:
            logger.warning("No job postings provided")
            return RecommendationResponse(ranked_job_ids=[])
        
        # Preprocess worker skills
        processed_worker_skills = preprocess_text(request.worker_profile.skills)
        
        if not processed_worker_skills.strip():
            logger.warning("Worker skills contain no meaningful content after preprocessing")
            return RecommendationResponse(ranked_job_ids=[])
        
        # Calculate similarity scores
        job_similarities = calculate_similarity_scores(processed_worker_skills, request.job_postings)
        
        if not job_similarities:
            logger.warning("No similarities calculated")
            return RecommendationResponse(ranked_job_ids=[])
        
        # Filter jobs with similarity score > 0 and sort by score (descending)
        MIN_SIMILARITY_THRESHOLD = 0.01  # Minimum similarity threshold
        filtered_jobs = [
            (job_id, score) for job_id, score in job_similarities 
            if score > MIN_SIMILARITY_THRESHOLD
        ]
        
        # Sort by similarity score in descending order
        ranked_jobs = sorted(filtered_jobs, key=lambda x: x[1], reverse=True)
        
        # Extract job IDs in ranked order
        ranked_job_ids = [job_id for job_id, _ in ranked_jobs]
        
        logger.info(f"Returning {len(ranked_job_ids)} recommended jobs")
        
        return RecommendationResponse(ranked_job_ids=ranked_job_ids)
        
    except Exception as e:
        logger.error(f"Error processing recommendation request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
