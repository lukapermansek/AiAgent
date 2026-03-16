import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    
    try:
        absolute_path_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path_working_dir, directory))
    
        #Find the common path between asbsolute path of working dir and target dir.
        #If that path == absolute path of working dir, that means that target dir is within the working dir.
        #Check is represented by a bool value assigned to valid_target_dir variable.
        valid_target_dir = os.path.commonpath([absolute_path_working_dir, target_dir]) == absolute_path_working_dir

        if valid_target_dir is False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        result_list = []    
        for item in os.listdir(target_dir):
            item_path = os.path.normpath(os.path.join(target_dir, item))
            is_dir = os.path.isdir(item_path)

            result_list.append(f"- {item}: file_size={os.path.getsize(item_path)}, is_dir={is_dir}")

        return "\n".join(result_list)
    
    except Exception as e:
        return f"Error: {str(e)}"
    
schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
                ),
            },
        ),
    )

