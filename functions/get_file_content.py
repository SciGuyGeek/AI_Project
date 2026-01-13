import os
from config import MAX_CHARS
from google import genai
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
            name="get_file_content",
            description="Reads the .txt file and returns the content (up to 10000 characters)",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                required=["file_path"],
                properties={
                    "directory": types.Schema(
                        type=types.Type.STRING,
                        description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
                    ),
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="Relative file path to relative to the working directory (default is the working directory itself)",
                    )
                }
            )
        )

def get_file_content(working_directory, file_path):
    try:
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_file = os.path.commonpath([abs_path, target_file]) == abs_path
        if not valid_target_file:
            return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_file):
            return (f'Error: File not found or is not a regular file: "{file_path}"')
        with open(target_file, 'r') as file:
            content = file.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if file.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except Exception as e:
        return f'Error: {file_path} {e}'  