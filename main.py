import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key==None:
    raise RuntimeError("Env Var with API key not found")

from google import genai
from google.genai import types
import argparse
client = genai.Client(api_key=api_key)

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
    model='gemini-2.5-flash', contents=messages
)
    if response.usage_metadata == None:
        raise RuntimeError("No response found")
    elif args.verbose:
        X = response.usage_metadata.prompt_token_count
        Y = response.usage_metadata.candidates_token_count
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {X}\nResponse tokens: {Y}")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
