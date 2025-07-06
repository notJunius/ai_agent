import os
import types
from google import genai.types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def get_files_info(working_directory, directory = None):
    abs_path = os.path.abspath(working_directory)
    target_dir = abs_path
    if directory:
        target_dir = os.path.abspath(os.path.join(working_directory, directory))
    if not target_dir.startswith(abs_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    try:
        file_info = []
        for file in os.listdir(target_dir):
            filepath = os.path.join(target_dir, file)
            file_size = 0
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)
            file_info.append(
                f"- {file}: file_size={file_size} bytes, is_dir={is_dir}"
            )
        return "\n".join(file_info)
    except Exception as e:
        return f"Error listing files: {e}"


