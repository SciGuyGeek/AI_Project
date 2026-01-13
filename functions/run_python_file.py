import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_file = os.path.commonpath([abs_path, target_file]) == abs_path
        if not valid_target_file:
            return (f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_file):
            return (f'Error: "{file_path}" does not exist or is not a regular file')
        root_ext = os.path.splitext(target_file)
        if root_ext[1] != ".py":
            return (f'Error: "{file_path}" is not a Python file')
        command = ["python", target_file]
        if args:
            command.extend(args)
        result = subprocess.run(
            command,
            cwd=abs_path,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output_str = ""
        if result.returncode != 0:
            output_str = (f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output_str += "No output produced"
        else:
            if result.stdout:
                output_str += (f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output_str += (f"STDERR:\n{result.stderr}")
        return output_str
    except Exception as e:
        return (f"Error: executing Python file: {e}")