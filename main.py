import os
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key==None:
    raise RuntimeError("Env Var with API key not found")

from google import genai
from google.genai import types
import argparse
client = genai.Client(api_key=api_key)

def main():
    model_name = "gemini-2.5-flash"
    results = []
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for ii in range(20):
        results = []
        response = client.models.generate_content(
            model=model_name,
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions],
                                            system_instruction=system_prompt,
                                            temperature=0),
        )
        if response.candidates != []:
                for jj in response.candidates:
                    messages.append(jj.content)
        if response.usage_metadata == None:
            raise RuntimeError("No response found")
        else:
            if response.function_calls:
                for kk in response.function_calls:
                    function_call_result = call_function(kk)
                    if function_call_result.parts == []:
                        raise Exception("parts list is empty")
                    if function_call_result.parts[0].function_response.response == None:
                        raise Exception("Response is empty")
                    results.append(function_call_result.parts[0])
                messages.append(types.Content(role="user", parts=results))
            else:
                print(response.text)
                break
        if args.verbose:
            X = response.usage_metadata.prompt_token_count
            Y = response.usage_metadata.candidates_token_count
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {X}\nResponse tokens: {Y}")
            print(f"-> {function_call_result.parts[0].function_response.response}")
        if ii == 19:
            print("Maximum iterations reached")
            exit(1)

if __name__ == "__main__":
    main()