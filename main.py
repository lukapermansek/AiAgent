import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import *
from call_functions import *

def get_client():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("API key not found.")
    return genai.Client(api_key=api_key)

def get_args():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()

def main():
    client = get_client()
    args = get_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]
            )
    )

    if response.usage_metadata is None:
        raise RuntimeError("Likely failed API request.")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if response.function_calls is not None:
        for i in response.function_calls:
            print(f"Calling function: {i.name}({i.args})")
            
            function_call_result = call_function(i)
            function_results = []
            
            if function_call_result.parts is None:
                raise Exception("Function call returned a empty .parts list")
            
            if function_call_result.parts[0].function_response is None:
                raise Exception("FunctionReponse object is None")
            
            if function_call_result.parts[0].function_response.response is None:
                raise Exception(".response field of FunctionResponse is empty")

            function_results.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

            print(function_results)
    else:
        print(response.text)


if __name__ == "__main__":
    main()
