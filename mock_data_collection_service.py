"""
Mock Data Collection Service
A simple FastAPI service that returns sample JSON data for testing purposes.
Run this on port 8001 to test the main summarization service.
"""
from fastapi import FastAPI
from typing import Optional
import json

app = FastAPI(
    title="Mock Data Collection Service",
    description="A mock service that returns sample data for testing",
    version="1.0.0"
)

# Sample data sets
SAMPLE_DATA_SETS = {
    "default": {
        "users": [
            {"id": 1, "name": "John Doe", "email": "john@example.com", "role": "admin", "active": True},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "role": "user", "active": True},
            {"id": 3, "name": "Bob Johnson", "email": "bob@example.com", "role": "user", "active": False}
        ],
        "statistics": {
            "total_users": 3,
            "active_users": 2,
            "inactive_users": 1
        },
        "metadata": {
            "last_updated": "2024-01-15T10:30:00Z",
            "version": "1.0"
        }
    },
    "sales": {
        "sales_data": [
            {"product": "Widget A", "quantity": 150, "revenue": 15000, "date": "2024-01-10"},
            {"product": "Widget B", "quantity": 200, "revenue": 30000, "date": "2024-01-11"},
            {"product": "Widget C", "quantity": 75, "revenue": 11250, "date": "2024-01-12"}
        ],
        "summary": {
            "total_quantity": 425,
            "total_revenue": 56250,
            "average_revenue_per_item": 132.35
        }
    },
    "events": {
        "events": [
            {
                "event_id": "E001",
                "name": "Product Launch",
                "date": "2024-02-01",
                "attendees": 500,
                "status": "scheduled"
            },
            {
                "event_id": "E002",
                "name": "Team Meeting",
                "date": "2024-01-20",
                "attendees": 25,
                "status": "completed"
            }
        ],
        "upcoming_events": 1,
        "completed_events": 1
    }
}


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Mock Data Collection Service",
        "status": "running",
        "available_sources": list(SAMPLE_DATA_SETS.keys())
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/data")
async def get_data(source: Optional[str] = None):
    """
    Returns mock data based on the source parameter.
    If no source is specified, returns the default dataset.
    
    Args:
        source: Optional data source identifier (default, sales, events)
    
    Returns:
        JSON data matching the requested source
    """
    # Use the specified source or default to "default"
    data_key = source if source and source in SAMPLE_DATA_SETS else "default"
    
    return SAMPLE_DATA_SETS[data_key]


if __name__ == "__main__":
    import uvicorn
    print("Starting Mock Data Collection Service on http://localhost:8001")
    print("Available data sources:", list(SAMPLE_DATA_SETS.keys()))
    uvicorn.run(app, host="0.0.0.0", port=8001)

