# modules/llm_handler.py

import os
import time
import asyncio
import logging
import pandas as pd
from groq import Groq, AsyncGroq
from groq import APIConnectionError, RateLimitError, APIStatusError, APITimeoutError
#from app_logger import get_logger

logger = logging.getLogger(__name__)
#logger = get_logger(__name__)

from dotenv import load_dotenv

load_dotenv()

class LLMSummarizer:
    def __init__(self, model_name: str, api_key_env_var: str,
                 timeout: float = 20.0, max_retries: int = 3, async_mode: bool = False):
        self.model_name = model_name
        self.api_key = os.getenv(api_key_env_var)
        if not self.api_key:
            raise ValueError(f"Environment variable {api_key_env_var} is not set.")
        self.timeout = timeout
        self.max_retries = max_retries
        self.async_mode = async_mode
        if async_mode:
            self.client = AsyncGroq(api_key=self.api_key, timeout=self.timeout)
        else:
            self.client = Groq(api_key=self.api_key, timeout=self.timeout)

    def _build_prompt(self, prompt_template: str, table_df: pd.DataFrame) -> str:
        table_text = table_df.to_string(index=False)
        prompt = prompt_template.replace("{table_data}", table_text)
        return prompt

    def _handle_error_retry(self, attempt: int):
        delay = 2 ** attempt
        logger.warning(f"Retrying after error, attempt {attempt + 1}/{self.max_retries}, waiting {delay}s")
        time.sleep(delay)

    def summarize(self, table_df: pd.DataFrame, prompt_template: str) -> str:
        """Synchronous summarization via Groq."""
        prompt = self._build_prompt(prompt_template, table_df)
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Groq API call (sync) attempt {attempt + 1}")
                response = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a financial analytics assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    model=self.model_name,
                    temperature=0.3,
                    max_tokens=400
                )
                summary = response.choices[0].message.content.strip()
                logger.info("Groq API call successful (sync)")
                return summary
            except RateLimitError:
                self._handle_error_retry(attempt)
            except (APIConnectionError, APIStatusError, APITimeoutError) as e:
                logger.warning(f"Groq API error (sync): {e}")
                self._handle_error_retry(attempt)
        error_msg = "Failed to get summary from Groq after retries (sync)"
        logger.error(error_msg)
        return error_msg

    async def summarize_async(self, table_df: pd.DataFrame, prompt_template: str) -> str:
        """Asynchronous summarization via Groq."""
        prompt = self._build_prompt(prompt_template, table_df)
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Groq API call (async) attempt {attempt + 1}")
                response = await asyncio.wait_for(
                    self.client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "You are a financial analytics assistant."},
                            {"role": "user", "content": prompt}
                        ],
                        model=self.model_name,
                        temperature=0.3,
                        max_tokens=400
                    ),
                    timeout=self.timeout
                )
                summary = response.choices[0].message.content.strip()
                logger.info("Groq API call successful (async)")
                return summary
            except RateLimitError:
                await asyncio.sleep(2 ** attempt)
            except (APIConnectionError, APIStatusError, APITimeoutError) as e:
                logger.warning(f"Groq API error (async): {e}")
                await asyncio.sleep(2 ** attempt)
        error_msg = "Failed to get summary from Groq after retries (async)"
        logger.error(error_msg)
        return error_msg
