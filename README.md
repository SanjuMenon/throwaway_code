# Data Summarization Service

A FastAPI service that fetches raw data from a data collection service and summarizes it using Azure OpenAI.

## Features

- Fetches raw data from an external data collection service
- Summarizes data using Azure OpenAI
- RESTful API with FastAPI
- Error handling and logging
- Environment-based configuration

## Requirements

- Python 3.8 or higher

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   - Copy `.env.example` to `.env`
   - Update the values in `.env` with your actual configuration:
     - `DATA_COLLECTION_SERVICE_URL`: URL of your data collection service
     - `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint
     - `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
     - `AZURE_OPENAI_API_VERSION`: API version (default: 2023-12-01-preview)
     - `AZURE_OPENAI_DEPLOYMENT_NAME`: Your deployment/model name

## Running the Service

```bash
# Using uvicorn directly
uvicorn main:app --reload --port 8000

# Or run the main file
python main.py
```

The service will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- **GET** `/` - Service information
- **GET** `/health` - Health check endpoint

### Summarization
- **POST** `/summarize` - Summarize data from the data collection service

#### Request Body (optional):
```json
{
  "data_source": "optional-source-identifier"
}
```

#### Response:
```json
{
  "summary": "Generated summary text...",
  "original_data_length": 1234,
  "summary_length": 567,
  "status": "success"
}
```

## API Documentation

Once the service is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing with Mock Data Collection Service

A mock data collection service is included for testing purposes:

```bash
# Run the mock service on port 8001
python mock_data_collection_service.py
```

The mock service provides sample data sets:
- **default**: User data with statistics
- **sales**: Sales data with revenue information
- **events**: Event data with scheduling information

You can test the summarization service by:
1. Setting `DATA_COLLECTION_SERVICE_URL=http://localhost:8001` in your `.env`
2. Running the mock service: `python mock_data_collection_service.py`
3. Running the main service: `uvicorn main:app --reload --port 8000`
4. Making a POST request to `/summarize` with optional `data_source` parameter

## Data Collection Service Integration

The service expects the data collection service to have:
- **Endpoint**: `GET /data`
- **Optional Query Parameter**: `source` (for specifying data source)
- **Response**: JSON data (dict, list, or any JSON-serializable structure)

A sample JSON file (`sample_data.json`) is also included to show the expected data format.

## Error Handling

The service handles:
- HTTP errors from the data collection service
- Azure OpenAI API errors
- Missing or invalid configuration
- Network timeouts

All errors are returned with appropriate HTTP status codes and error messages.

