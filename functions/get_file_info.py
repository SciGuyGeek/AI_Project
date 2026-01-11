import os
def get_files_info(working_directory, directory="."):
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, directory))
        # Will be True or False
        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path
        if not valid_target_dir:
            return (f'Error: Cannot list "{target_dir}" as it is outside the permitted working directory')
        if not os.path.isdir(target_dir):
            return (f'Error: "{target_dir}" is not a directory')
        str_list = []
        for ii in os.listdir(target_dir):
            file_path = os.path.join(target_dir,ii)
            file_name = ii
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            str_list.append("- " + str(file_name) + ":file_size=" + str(file_size) + " bytes, is_dir=" + str(is_dir))
        str_list = "\n".join(str_list)
        return str_list
    except Exception as e:
        return f'Error: {e}'