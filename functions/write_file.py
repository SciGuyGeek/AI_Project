import os

def write_file(working_directory, file_path, content):
    try:
        abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_file = os.path.commonpath([abs_path, target_path]) == abs_path
        parent_dir = os.path.dirname(target_path)
        if not valid_target_file:
            return (f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        if os.path.isdir(target_path):
            return (f'Error: Cannot write to "{file_path}" as it is a directory')
        os.makedirs(parent_dir, exist_ok=True)
        with open(target_path, 'w') as file:
            file.write(content)
            return (f'Successfully wrote to "{target_path}" ({len(content)} characters written)')
    except Exception as e:
        return f'Error: Cannot write to "{target_path}" {e}'  