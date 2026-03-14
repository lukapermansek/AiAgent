import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        absolute_path_working_dir = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_path_working_dir, file_path))

        #Find the common path between asbsolute path of working dir and target dir.
        #If that path == absolute path of working dir, that means that target dir is within the working dir.
        #Check is represented by a bool value assigned to valid_target_dir variable.
        valid_target_file_path = os.path.commonpath([absolute_path_working_dir, target_path]) == absolute_path_working_dir

        if not valid_target_file_path:
            return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"

        if not os.path.isfile(target_path):
            return f"Error: \"{file_path}\" does not exist or is not a regular file"
        
        if not target_path.endswith(".py"):
            return f"Error: \"{file_path}\" is not a Python file"
        
        command = ["python", target_path]
        command.extend(args or [])

        completed_process = subprocess.run(command, capture_output=True, text=True, timeout=30)

        return_string = ""

        if completed_process.returncode != 0:
            return_string += f"Process exited with code {completed_process.returncode} "
        
        if completed_process.stderr == "" and completed_process.stdout == "":
            return_string += f"No output produced "
        elif completed_process.stderr != "":
            return_string += f"STDERR: {completed_process.stderr} "
        elif completed_process.stdout != "":
            return_string += f"STDOUT: {completed_process.stdout} "

        return return_string

    except Exception as e:
        return f"Error: exectuing Python file: {e}"