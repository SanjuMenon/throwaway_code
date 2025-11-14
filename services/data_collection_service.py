import httpx
from typing import Optional, Any, Dict
import logging
import os

logger = logging.getLogger(__name__)


class DataCollectionService:
    """Service to fetch raw data from an external data collection service"""
    
    def __init__(self, base_url: str, timeout: int = 30, api_key: Optional[str] = None):
        """
        Initialize the data collection service client
        
        Args:
            base_url: Base URL of the data collection service
            timeout: Request timeout in seconds
            api_key: Optional API key for authentication (can also be set via env var DATA_COLLECTION_API_KEY)
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.api_key = api_key or os.getenv("DATA_COLLECTION_API_KEY")
        self.client = httpx.AsyncClient(timeout=timeout)
    
    async def fetch_data(self, data_source: Optional[str] = None) -> Any:
        """
        Fetch raw data from the data collection service
        
        Args:
            data_source: Optional parameter to specify which data source to fetch
        
        Returns:
            Raw data from the service (can be dict, list, or string)
        
        Raises:
            httpx.HTTPError: If the request fails
        
        NOTE: To modify the endpoint for your real data collection service:
        - Change the endpoint path on line 38 (e.g., "/data" -> "/api/v1/data")
        - Change HTTP method on line 48 if needed (get -> post, put, etc.)
        - Add headers if authentication is required (see example below)
        - Add request body for POST/PUT requests (see example below)
        """
        try:
            # Construct the endpoint URL
            # MODIFY THIS: Change "/data" to your actual endpoint path
            endpoint = f"{self.base_url}/data"
            
            # Prepare request parameters
            # MODIFY THIS: Add or modify query parameters as needed
            params = {}
            if data_source:
                params["source"] = data_source
            
            # MODIFY THIS: Add headers if your service requires authentication
            headers: Dict[str, str] = {}
            if self.api_key:
                # Example: Bearer token authentication
                headers["Authorization"] = f"Bearer {self.api_key}"
                # Or for API key in header:
                # headers["X-API-Key"] = self.api_key
            # Add other headers as needed:
            # headers["Content-Type"] = "application/json"
            
            logger.info(f"Fetching data from {endpoint} with params: {params}")
            
            # Make the request
            # MODIFY THIS: Change method (get/post/put) and add headers/body as needed
            # For GET request:
            response = await self.client.get(endpoint, params=params, headers=headers)
            
            # For POST request with body, use:
            # body = {"key": "value"}
            # response = await self.client.post(endpoint, json=body, headers=headers)
            
            response.raise_for_status()
            
            # Return the data (assuming JSON response)
            data = response.json()
            logger.info(f"Successfully fetched data, size: {len(str(data))} characters")
            
            return data
        
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching data: {e.response.status_code} - {e.response.text}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Request error fetching data: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching data: {str(e)}")
            raise
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

