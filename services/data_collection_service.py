import httpx
from typing import Optional, Any
import logging

logger = logging.getLogger(__name__)


class DataCollectionService:
    """Service to fetch raw data from an external data collection service"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialize the data collection service client
        
        Args:
            base_url: Base URL of the data collection service
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
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
        """
        try:
            # Construct the endpoint URL
            endpoint = f"{self.base_url}/data"
            
            # Prepare request parameters
            params = {}
            if data_source:
                params["source"] = data_source
            
            logger.info(f"Fetching data from {endpoint} with params: {params}")
            
            # Make the request
            response = await self.client.get(endpoint, params=params)
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

