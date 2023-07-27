import os
import shutil

"""
Removes a directory if it exists.
"""
def remove_dir(directory: str) -> None:
    if os.path.exists(directory):
        shutil.rmtree(directory)


"""
Returns list of files in a directory
"""
def get_files(dir) -> list:
    return [os.path.join(dir, f) for f in os.listdir(dir)]
