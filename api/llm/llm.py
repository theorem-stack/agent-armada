from dotenv import load_dotenv
import os
import json
from openai import OpenAI

from ..config import LLM_MISSION_STATEMENT_PROMPT, LLM_PROMPT_SYSTEM_RESPONSE, OPENAI_MODEL, MAX_TOKENS, TEMPERATURE
from ..translator.translator import translate
from ..lib.dataProcessing import map_to_json

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variables
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")

async def OpenAI_API_CALL(user_mission_statement):
    try:
        print("Calling OpenAI API...")

        client = OpenAI(
            # This is the default and can be omitted
            api_key=OPEN_AI_API_KEY,
        )

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": LLM_MISSION_STATEMENT_PROMPT},
                {"role": "user", "content": user_mission_statement},
            ],
            model=OPENAI_MODEL,
            max_tokens=MAX_TOKENS,  # Adjust this as necessary for your needs
            temperature=TEMPERATURE,  # Adjusts randomness of responses; lower values make output more focused
        )

        # Extract the response content
        ai_response = response['choices'][0]['message']['content'].strip()
        return ai_response

    except Exception as e:
        return f"An error occurred: {str(e)}"
    
async def LLM_Planning(user_mission_statement, satellite_map):

    # Stringify the satellite map as context for the LLM
    satellite_map_json = map_to_json(satellite_map)

    input_data = {
        "user_mission_statement": user_mission_statement,
        "satellite_map_objects": satellite_map_json
    }

    # convert the input data to a json string
    llm_mission_input = json.dumps(input_data)

    # Get the LLM plan
    actions = await OpenAI_API_CALL(user_mission_statement)

    print(actions)

    # Execute the LLM plan ---------------------
    targets = []
    # for action in actions:
    #     translation = translate(action)
    #     targets.append(translation)

    return targets