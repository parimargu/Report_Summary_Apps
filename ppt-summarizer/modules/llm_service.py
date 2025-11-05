"""
LLM service module for table summarization using Groq.

Handles API calls to Groq LLM with retry logic and error handling.
"""

import time
from pathlib import Path
from typing import Optional

from groq import Groq, AsyncGroq
from groq import RateLimitError, APITimeoutError, APIError

from modules.logger import get_logger
from modules.config_manager import get_config

logger = get_logger(__name__)
config = get_config()


class LLMService:
    """Service for generating table summaries using Groq LLM."""

    def __init__(self):
        """Initialize LLM service with configuration."""
        self.api_key = config.get("llm.api_key")
        self.model_name = config.get("llm.model_name", "llama-3.1-70b-versatile")
        self.temperature = config.get("llm.temperature", 0.3)
        self.max_tokens = config.get("llm.max_tokens", 1024)
        self.timeout = config.get("llm.timeout_seconds", 30)
        self.max_retries = config.get("llm.max_retries", 3)
        self.retry_delay = config.get("llm.retry_delay_seconds", 2)

        # Load prompt template
        self.prompt_template = self._load_prompt_template()

        # Initialize clients
        if not self.api_key:
            logger.error("GROQ_API_KEY not found in configuration")
            raise ValueError("GROQ_API_KEY must be set in environment or config")

        self.client = Groq(api_key=self.api_key, timeout=self.timeout)
        self.async_client = AsyncGroq(api_key=self.api_key, timeout=self.timeout)

        logger.info(f"LLMService initialized with model: {self.model_name}")

    def _load_prompt_template(self) -> str:
        """
        Load prompt template from file.

        Returns:
            Prompt template string

        Raises:
            FileNotFoundError: If template file doesn't exist
        """
        template_file = config.get("prompts.template_file", "prompt_template.txt")
        template_path = Path(template_file)

        try:
            if not template_path.exists():
                logger.error(f"Prompt template file not found: {template_file}")
                raise FileNotFoundError(f"Prompt template not found: {template_file}")

            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()

            logger.info(f"Loaded prompt template from {template_file}")
            return template

        except Exception as e:
            logger.error(f"Error loading prompt template: {str(e)}")
            raise

    def generate_summary(self, table_data: str, retry_count: int = 0) -> Optional[str]:
        """
        Generate summary for table data using Groq LLM.

        Args:
            table_data: Formatted table data as string
            retry_count: Current retry attempt (for internal use)

        Returns:
            Generated summary or None if failed

        Raises:
            Exception: If all retries fail
        """
        try:
            # Prepare prompt
            prompt = self.prompt_template.format(table_data=table_data)
            system_role = config.get(
                "prompts.system_role",
                "You are a financial analyst expert."
            )

            logger.info("Generating table summary with Groq LLM")
            logger.debug(f"Using model: {self.model_name}, temperature: {self.temperature}")

            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            # Extract summary
            summary = response.choices[0].message.content

            # Log token usage
            if hasattr(response, 'usage'):
                logger.info(
                    f"LLM usage - Prompt tokens: {response.usage.prompt_tokens}, "
                    f"Completion tokens: {response.usage.completion_tokens}, "
                    f"Total: {response.usage.total_tokens}"
                )

            logger.info("\n LLM Response: \n")
            logger.info(summary)
            logger.info("\n")

            logger.info("Successfully generated summary")
            return summary

        except RateLimitError as e:
            logger.warning(f"Rate limit error: {str(e)}")
            if retry_count < self.max_retries:
                wait_time = self.retry_delay * (2 ** retry_count)  # Exponential backoff
                logger.info(f"Retrying after {wait_time} seconds (attempt {retry_count + 1}/{self.max_retries})")
                time.sleep(wait_time)
                return self.generate_summary(table_data, retry_count + 1)
            else:
                logger.error("Max retries exceeded for rate limit")
                raise

        except APITimeoutError as e:
            logger.warning(f"API timeout: {str(e)}")
            if retry_count < self.max_retries:
                wait_time = self.retry_delay
                logger.info(f"Retrying after {wait_time} seconds (attempt {retry_count + 1}/{self.max_retries})")
                time.sleep(wait_time)
                return self.generate_summary(table_data, retry_count + 1)
            else:
                logger.error("Max retries exceeded for timeout")
                raise

        except APIError as e:
            logger.error(f"Groq API error: {str(e)}")
            if retry_count < self.max_retries:
                wait_time = self.retry_delay
                logger.info(f"Retrying after {wait_time} seconds (attempt {retry_count + 1}/{self.max_retries})")
                time.sleep(wait_time)
                return self.generate_summary(table_data, retry_count + 1)
            else:
                logger.error("Max retries exceeded for API error")
                raise

        except Exception as e:
            logger.error(f"Unexpected error generating summary: {str(e)}", exc_info=True)
            raise

    async def generate_summary_async(self, table_data: str, retry_count: int = 0) -> Optional[str]:
        """
        Generate summary asynchronously for table data using Groq LLM.

        Args:
            table_data: Formatted table data as string
            retry_count: Current retry attempt (for internal use)

        Returns:
            Generated summary or None if failed
        """
        try:
            # Prepare prompt
            prompt = self.prompt_template.format(table_data=table_data)
            system_role = config.get(
                "prompts.system_role",
                "You are a financial analyst expert."
            )

            logger.info("Generating table summary asynchronously with Groq LLM")

            # Call Groq API asynchronously
            response = await self.async_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            # Extract summary
            summary = response.choices[0].message.content

            logger.info("\n LLM Response: \n")
            logger.info(summary)
            logger.info("\n")
            logger.info("Successfully generated async summary")
            return summary

        except (RateLimitError, APITimeoutError, APIError) as e:
            logger.warning(f"API error (async): {str(e)}")
            if retry_count < self.max_retries:
                wait_time = self.retry_delay * (2 ** retry_count)
                logger.info(f"Retrying after {wait_time} seconds (attempt {retry_count + 1}/{self.max_retries})")
                await self._async_sleep(wait_time)
                return await self.generate_summary_async(table_data, retry_count + 1)
            else:
                logger.error("Max retries exceeded")
                raise

        except Exception as e:
            logger.error(f"Unexpected error in async summary: {str(e)}", exc_info=True)
            raise

    async def _async_sleep(self, seconds: float):
        """Async sleep helper."""
        import asyncio
        await asyncio.sleep(seconds)

    def test_connection(self) -> bool:
        """
        Test connection to Groq API.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            logger.info("Testing Groq API connection")

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": "Hello, this is a connection test. Please respond with 'OK'."}
                ],
                max_tokens=10,
            )

            logger.info("Groq API connection test successful")
            return True

        except Exception as e:
            logger.error(f"Groq API connection test failed: {str(e)}")
            return False


# Example usage
if __name__ == "__main__":
    # Test LLM service
    try:
        service = LLMService()

        # Test connection
        if service.test_connection():
            print("✓ Connection successful")

            # Test summary generation
            sample_table = """
| Segment | Q1 Default Rate (%) | Q2 Default Rate (%) | Net Rate (%) |
|---------|---------------------|---------------------|--------------|
| Commercial | 2.3 | 2.8 | 1.2 |
| Retail | 3.1 | 4.5 | -0.5 |
| Mortgage | 1.5 | 1.6 | 0.8 |
            """

            summary = service.generate_summary(sample_table)
            print(f"\nGenerated Summary:\n{summary}")
        else:
            print("✗ Connection failed")

    except Exception as e:
        print(f"Error: {e}")
