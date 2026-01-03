from openai import OpenAI
import os
import logging

# Optional basic logging (recommended)
logging.basicConfig(level=logging.INFO)

# Default model (can be changed without touching agent logic)
MODEL_NAME = "gpt-4o-mini"


def chat_completion(messages: list, tools: list | None = None):
    """
    Wrapper around OpenAI Chat Completions API.

    Responsibilities:
    - Call OpenAI with messages and tools
    - Allow model to decide tool usage
    - Return raw OpenAI response

    This follows OpenAI tool-calling documentation.
    """

    try:
        # Initialize OpenAI client here to ensure env is loaded
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.2
        )

        return response

    except Exception as e:
        logging.error(f"OpenAI API error: {str(e)}")
        raise
