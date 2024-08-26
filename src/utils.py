from dotenv import load_dotenv, find_dotenv
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("utils")


def get_openai_api_key():
    # Try to load environment variables from .env file
    load_dotenv(find_dotenv())

    # Try to get the API key using dotenv's get method
    api_key = os.getenv("OPEN_AI_TOKEN")

    if api_key is None:
        logger.error("OPEN_AI_TOKEN not found in .env file or OS environment.")
        raise ValueError(
            "OpenAI API key not found. Please set the OPEN_AI_TOKEN in your .env file or as an environment variable."
        )

    logger.info("Successfully retrieved OpenAI API key.")
    return api_key
