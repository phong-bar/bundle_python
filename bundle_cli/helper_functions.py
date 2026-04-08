import os
import glob
from typing import Optional


def get_latest_file_in_folder(folder_path: str, file_extension: Optional[str] = "*") -> Optional[str]:
    '''
    Get the last modified file within folder_path
    '''
    if file_extension and file_extension != "*":
        ext = file_extension if file_extension.startswith('.') else f'.{file_extension}'
        pattern = os.path.join(folder_path, f"*{ext}")
    else:
        pattern = os.path.join(folder_path, "*")

    list_of_files = glob.glob(pattern)
    
    # Filter out directories
    list_of_files = [f for f in list_of_files if os.path.isfile(f)]

    if not list_of_files:
        return None

    return max(list_of_files, key=os.path.getmtime)