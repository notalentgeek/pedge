import sys
sys.path.append("../")
sys.path.append("../cli")
sys.path.append("../config_and_database")
sys.path.append("../detection")
sys.path.append("../loose_lib")
sys.path.append("../loose_lib/python-ipy")

import fileinput
import re

def convert_str_to_bool(_str):
    if   str(_str).lower() in ["1", "t", "true" , "y", "yes"]: return True
    elif str(_str).lower() in ["0", "f", "false", "n", "no" ]: return False
    else                                                     : return None

def convert_str_to_list(_str):
    return _str.replace("'", "").split("[")[1].split("]")[0].split(", ")

def file_search_and_replace(_path_abs, _search, _replace):
    with fileinput.FileInput(_path_abs, inplace=True) as file:
        for line in file: print(line.replace(_search, _replace), end="")

def file_search_and_replace_exact(_path_abs, _search, _replace):
    outfile = open(_path_abs, "r")
    temp = outfile.read()
    temp = re.sub(_search, _replace, temp)
    outfile.close()
    outfile = open("test.c","w")
    outfile.write(temp)
    outfile.close()