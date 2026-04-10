import pandas
import sys
import os

# file -> directory name -> outer directory name
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(main_dir)

from bundle_cli.api import Bundle
from bundle_cli import helper_functions

file_path = helper_functions.get_latest_file_in_folder(
    "Takomo_workarounds/TAG_inventory", file_extension="xlsx"
)

print(file_path)
