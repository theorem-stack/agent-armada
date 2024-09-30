import openai
from dotenv import load_dotenv
import os

from .config import LLM_PROMPT_USER_INPUT, LLM_PROMPT_SYSTEM_RESPONSE

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variables
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")

# Initialize the OpenAI API client with your API key
openai.api_key = OPEN_AI_API_KEY

def LLM(user_query, response_type):
    # Define the prompt for the language model
    if response_type == "user_input":
        llm_prompt = f"{LLM_PROMPT_USER_INPUT}:\n\nUser: {user_query}\nAI:"
    elif response_type == "system_response":
        llm_prompt = f"{LLM_PROMPT_SYSTEM_RESPONSE}:\n\nSystem: {user_query}\nAI:"

    try:
        # Make the API call to OpenAI's GPT model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can change this to a different model if needed
            messages=[
                {"role": "user", "content": llm_prompt}
            ],
            max_tokens=150,  # Adjust this as necessary for your needs
            temperature=0.7,  # Adjusts randomness of responses; lower values make output more focused
        )
        
        # Extract the response content
        ai_response = response['choices'][0]['message']['content'].strip()
        return ai_response

    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage
if __name__ == "__main__":
    user_input = "What are the benefits of exercise?"
    response = LLM(user_input)
    print(response)
