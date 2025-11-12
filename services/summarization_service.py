from openai import AzureOpenAI
from typing import Any
import logging
import json
import asyncio
from functools import partial

logger = logging.getLogger(__name__)


class SummarizationService:
    """Service to summarize data using Azure OpenAI"""
    
    def __init__(
        self,
        azure_endpoint: str,
        api_key: str,
        api_version: str = "2023-12-01-preview",
        deployment_name: str = None
    ):
        """
        Initialize the Azure OpenAI client
        
        Args:
            azure_endpoint: Azure OpenAI endpoint URL
            api_key: Azure OpenAI API key
            api_version: API version to use
            deployment_name: Name of the deployment/model to use
        """
        if not azure_endpoint or not api_key:
            raise ValueError("Azure OpenAI endpoint and API key are required")
        
        if not deployment_name:
            raise ValueError("Deployment name is required")
        
        self.client = AzureOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=api_key,
            api_version=api_version
        )
        self.deployment_name = deployment_name
    
    async def summarize(self, data: Any, max_tokens: int = 500) -> str:
        """
        Summarize the provided data using Azure OpenAI
        
        Args:
            data: The data to summarize (can be dict, list, or string)
            max_tokens: Maximum tokens for the summary
        
        Returns:
            Summary string
        """
        try:
            # Convert data to string if it's not already
            if isinstance(data, (dict, list)):
                data_str = json.dumps(data, indent=2)
            else:
                data_str = str(data)
            
            logger.info(f"Summarizing data of length: {len(data_str)} characters")
            
            # Create the prompt for summarization
            prompt = f"""Please provide a concise summary of the following data. 
Focus on the key points, important information, and main insights.

Data:
{data_str}

Summary:"""
            
            # Call Azure OpenAI API (run in executor to avoid blocking event loop)
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                partial(
                    self.client.chat.completions.create,
                    model=self.deployment_name,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that provides concise and informative summaries of data."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=max_tokens,
                    temperature=0.3  # Lower temperature for more consistent summaries
                )
            )
            
            # Extract the summary
            summary = response.choices[0].message.content.strip()
            logger.info(f"Successfully generated summary of length: {len(summary)} characters")
            
            return summary
        
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            raise

