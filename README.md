# WorkConnect AI Recommendation Service

This directory contains the AI-powered job recommendation service for the WorkConnect application.

## Files

- `app.py` - Main FastAPI application with recommendation endpoints
- `requirements.txt` - Python dependencies
- `test_ai_integration.py` - Basic integration tests
- `test_ai_integration_enhanced.py` - Comprehensive integration tests with edge cases
- `workconnect-AI.iml` - IntelliJ module file

## Running the Service

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the service:
   ```bash
   python app.py
   ```

3. The service will be available at `http://localhost:8000`

## Testing

Run the basic integration tests:
```bash
python test_ai_integration.py
```

Run the enhanced integration tests (includes edge cases and performance tests):
```bash
python test_ai_integration_enhanced.py
```

## API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health check
- `POST /recommendations/jobs` - Get job recommendations based on worker skills
