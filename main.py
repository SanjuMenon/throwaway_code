from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

from services.data_collection_service import DataCollectionService
from services.summarization_service import SummarizationService

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Data Summarization Service",
    description="A service that fetches raw data and summarizes it using Azure OpenAI",
    version="1.0.0"
)

# Initialize services
data_collection_service = DataCollectionService(
    base_url=os.getenv("DATA_COLLECTION_SERVICE_URL", "http://localhost:8001")
)

summarization_service = SummarizationService(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-12-01-preview"),
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
)


class SummarizeRequest(BaseModel):
    """Request model for summarization endpoint"""
    data_source: Optional[str] = None  # Optional parameter to specify which data source to fetch


class SummarizeResponse(BaseModel):
    """Response model for summarization endpoint"""
    summary: str
    original_data_length: int
    summary_length: int
    status: str


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Data Summarization Service",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/summarize", response_model=SummarizeResponse)
async def summarize_data(request: SummarizeRequest = SummarizeRequest()):
    """
    Main endpoint that:
    1. Fetches raw data from the data collection service
    2. Summarizes the data using Azure OpenAI
    3. Returns the summary
    """
    try:
        # Step 1: Fetch raw data from data collection service
        raw_data = await data_collection_service.fetch_data(data_source=request.data_source)
        
        if not raw_data:
            raise HTTPException(
                status_code=404,
                detail="No data found from data collection service"
            )
        
        original_data_length = len(str(raw_data))
        
        # Step 2: Summarize the data using Azure OpenAI
        summary = await summarization_service.summarize(raw_data)
        
        if not summary:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate summary"
            )
        
        # Step 3: Return the results
        return SummarizeResponse(
            summary=summary,
            original_data_length=original_data_length,
            summary_length=len(summary),
            status="success"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

