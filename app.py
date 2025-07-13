from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

# Download NLTK data (only needs to be done once)
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')
    nltk.download('punkt')

app = Flask(__name__)

# Pre-processing function for text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return " ".join(tokens)

@app.route('/match', methods=['POST'])
def get_matches():
    data = request.get_json()

    # Extract worker profile and job listings from the request data
    worker_profile = data.get('worker_profile', {})
    jobs = data.get('jobs', [])

    if not worker_profile or not jobs:
        return jsonify({"error": "Missing worker_profile or jobs data"}), 400

    # Combine worker skills and experience into a single string
    worker_text = f"{worker_profile.get('skills', '')} {worker_profile.get('experience', '')}"

    # Create a DataFrame for jobs
    jobs_df = pd.DataFrame(jobs)
    jobs_df['job_text'] = jobs_df['title'] + ' ' + jobs_df['description'] + ' ' + jobs_df['requiredSkills']

    # Pre-process all text
    processed_worker_text = preprocess_text(worker_text)
    jobs_df['processed_job_text'] = jobs_df['job_text'].apply(preprocess_text)

    # Vectorize the text using TF-IDF
    vectorizer = TfidfVectorizer()
    all_text = [processed_worker_text] + jobs_df['processed_job_text'].tolist()
    tfidf_matrix = vectorizer.fit_transform(all_text)

    # Calculate cosine similarity between the worker's profile and all jobs
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

    # Add similarity scores to the DataFrame
    jobs_df['similarity_score'] = cosine_similarities[0]

    # Filter for jobs with a similarity score > 0 (basic threshold)
    recommended_jobs = jobs_df[jobs_df['similarity_score'] > 0.01]

    # Sort jobs by similarity score in descending order
    recommended_jobs = recommended_jobs.sort_values(by='similarity_score', ascending=False)

    # Return the ranked list of job IDs
    ranked_job_ids = recommended_jobs['id'].tolist()

    return jsonify({"recommended_job_ids": ranked_job_ids})

if __name__ == '__main__':
    # Run the app on port 5001 to avoid conflicts with other services
    app.run(debug=True, port=5001)
