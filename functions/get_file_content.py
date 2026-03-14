import os
from config import *

def get_file_content(working_directory, file_path):
    try:
        absolute_path_working_dir = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_path_working_dir, file_path))

        #Find the common path between asbsolute path of working dir and target dir.
        #If that path == absolute path of working dir, that means that target dir is within the working dir.
        #Check is represented by a bool value assigned to valid_target_dir variable.
        valid_target_file_path = os.path.commonpath([absolute_path_working_dir, target_path]) == absolute_path_working_dir
        
        if not valid_target_file_path:
            return f"Error: Cannot read {file_path} as it is outside the permitted working directory"
    
        if not os.path.isfile(target_path):
            return f"Error: File not found or is not a regular file: {file_path}"

        with open(target_path, "r") as f:
            #MAX_CHARS set in config.py (10,000 by default)
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f"[...File {file_path} truncated at {MAX_CHARS} characters]"
        
        return file_content_string
    
    except Exception as e:
        return f"Error: {str(e)}"
    