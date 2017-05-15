import sys
sys.path.append("../")
sys.path.append("../cli")
sys.path.append("../config_and_database")
sys.path.append("../detection")
sys.path.append("../loose_lib")
sys.path.append("../loose_lib/python-ipy")

import os
import shutil

def create_file_of_folder(
    _path_source:str,
    _is_file:bool,
    _name:str
) -> bool:
    """Function to create file or folder.

    Args:
        _path_source : The absolute directory for the created file or folder.
        _is_file     : If this is set to `True`  this function will create a
                       file. If this is set to `False` this function will
                       create a folder.
        _name        : The name of the file or folder, the user wants to
                       create.
    Returns:
        `True`       : If the file or folder is created.
        `False`      : If the file or folder is not created.
    """

    create      = False
    path_source = join(_path_source, _name)

    if _is_file and not path_is_file(path_source):
        create = True
    elif not _is_file and not path_is_folder(path_source):
        create = True

    if create:
        if _is_file:
            open(path_source, "w").close()
        else:
            os.makedirs(path_source)

    return create

def delete(_path_source:str) -> bool:
    if path_is_exists(_path_source):
        if path_is_file(_path_source):
            os.remove(_path_source)
        else:
            shutil.rmtree(_path_source, ignore_errors=True)
        return True

    return False

def join(
    _path_source:str,
    _name:str
) -> str:
    return os.path.join(_path_source, _name)

def path_is_exists(_path_source:str) -> bool:
    return os.path.exists(_path_source)

def path_is_file(_path_source:str) -> bool:
    return os.path.isfile(_path_source)

def path_is_folder(_path_source:str) -> bool:
    return os.path.isdir(_path_source)