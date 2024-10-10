from dotenv import load_dotenv
import os
from openai import OpenAI

from ..config import OPENAI_MODEL, MAX_TOKENS, TEMPERATURE
from ..translator.translator import translate
from ..lib.dataProcessing import map_to_string
from ..lib.utils import parse_yaml_steps
from .prompts.model_prompt import MODEL_PROMPT
from ..llm.prompts.prompt_function_examples import PROMPT_FUNCTION_EXAMPLES

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variables
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
AI_ML_API_KEY = os.getenv("AI_ML_API_KEY")

async def OpenAI_API_CALL(user_mission_statement, prompt):
    try:
        print("Calling OpenAI API...")

        client = OpenAI(
            base_url="https://api.aimlapi.com/v1",
            api_key=AI_ML_API_KEY,
            # api_key=OPEN_AI_API_KEY,
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

    mission_prompt = f"{MODEL_PROMPT}\n Function Examples:{PROMPT_FUNCTION_EXAMPLES}\n Context Objects:{satellite_map_string}"

    try:
        # Get the LLM plan
        llm_response = await OpenAI_API_CALL(user_mission_statement, mission_prompt)
    except Exception as e:
        print(f"Error during LLM API call: {e}")
        return False  # or retry logic

    # Parse the YAML string
    parsed_steps = parse_yaml_steps(llm_response)

    # Execute the LLM plan 
    for step_number, step_details in parsed_steps.items():

        try:
            code = step_details["python_function"]
            function_type = step_details["function_type"]

            # Verify & Evaluate the code
            step_eval = translate(code, N, map_objects_dict, BBox)

            # Store the evaluated code output
            if function_type == "role":
                parsed_steps[step_number]["role"] = step_eval
            elif function_type == "group":
                parsed_steps[step_number]["group"] = step_eval
            elif function_type == "coordinates":
                parsed_steps[step_number]["coordinates"] = step_eval
        except Exception as e:
            print(f"Error during step {step_number}: {e}")
            return False  # or continue based on the criticality of the step

    return parsed_steps.copy()


