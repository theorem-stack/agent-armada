from dotenv import load_dotenv
import os
import json
from openai import OpenAI

from ..config import LLM_MISSION_STATEMENT_PROMPT, LLM_PLAN_REVIEWER_PROMPT, LLM_PROMPT_SYSTEM_RESPONSE, OPENAI_MODEL, MAX_TOKENS, TEMPERATURE
from ..translator.translator import translate
from ..lib.dataProcessing import map_to_string
from ..lib.utils import read_yaml_to_string, parse_yaml_steps
from ..llm.prompts.large_model_prompt import LARGE_MODEL_PROMPT
from ..llm.prompts.prompt_function_examples import PROMPT_FUNCTION_EXAMPLES

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variables
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")

async def OpenAI_API_CALL(user_mission_statement, prompt):
    try:
        print("Calling OpenAI API...")

        client = OpenAI(
            # This is the default and can be omitted
            api_key=OPEN_AI_API_KEY,
        )

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_mission_statement},
            ],
            model=OPENAI_MODEL,
            max_tokens=MAX_TOKENS,  # Adjust this as necessary for your needs
            temperature=TEMPERATURE,  # Adjusts randomness of responses; lower values make output more focused
        )

        # Extract the response content
        ai_response = response.choices[0].message.content
        return ai_response

    except Exception as e:
        return f"An error occurred: {str(e)}"
    
async def LLM_Planning(user_mission_statement, N, map_objects, BBox):

    # Stringify the satellite map as context for the LLM
    satellite_map_string = map_to_string(map_objects)

    # Convert the map objects to list of dictionaries
    map_objects_dict = [obj.convert_to_dict() for obj in map_objects]

    mission_prompt = f"{LARGE_MODEL_PROMPT}\n Function Examples:{PROMPT_FUNCTION_EXAMPLES}\n Context Objects:{satellite_map_string}"

    # # Get the LLM plan
    llm_response = await OpenAI_API_CALL(user_mission_statement, mission_prompt)

    # print(llm_response)

    # Parse the YAML string
    parsed_steps = parse_yaml_steps(llm_response)

    # Execute the LLM plan ---------------------
    for step_number, step_details in parsed_steps.items():
        code = step_details["python_function"]
        target_coordinates = translate(code, N, map_objects_dict, BBox)
        parsed_steps[step_number]["target_coordinates"] = target_coordinates

    return parsed_steps