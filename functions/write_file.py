import os

def write_file(working_directory, file_path, content):
    try:
        absolute_path_working_dir = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_path_working_dir, file_path))

        #Find the common path between asbsolute path of working dir and target dir.
        #If that path == absolute path of working dir, that means that target dir is within the working dir.
        #Check is represented by a bool value assigned to valid_target_dir variable.
        valid_target_file_path = os.path.commonpath([absolute_path_working_dir, target_path]) == absolute_path_working_dir
        
        if not valid_target_file_path:
            return f"Error: Cannot write to {file_path} as it is outside the permitted working directory"

        if os.path.isdir(target_path):
            return f"Error: Cannot write to {file_path} as it is a directory"

        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, "w") as f:
            f.write(content)

        return f"Successfully wrote to {file_path} ({len(content)} characters written)"

    except Exception as e:
        return f"Error: {str(e)}"