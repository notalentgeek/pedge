import sys
sys.path.append("../")
sys.path.append("../cli")
sys.path.append("../config_and_database")
sys.path.append("../detection")
sys.path.append("../loose_lib")
sys.path.append("../loose_lib/python-ipy")

"""Collections of function(s) to manipulate dictionary. Usually used to deal with
value returned from RethinkDB query
"""

def sort_dict_list(_list:list, _name_column_target:str, _ascending:bool=True):
    """PENDING: This function is not yet unit tested!"""

    if _ascending:
        l = sorted(_list, key=lambda k : k[_name_column_target])
    else:
        l = sorted(_list, key=lambda k : k[_name_column_target], reverse=True)

    return l



def take_a_dict_from_dict_list(_list:list, _name_column_target:str,
    _ascending:bool=True):
    """PENDING: This function is not yet unit tested!"""

    try:
        return sort_dict_list(_list, _name_column_target, _ascending)[0]
    except IndexError:
        return []



def take_a_value_from_dict_list(
    _list:list,
    _name_column_target:str,
    _ascending:bool=True
):
    """Function to take a value from dictionaries in a list. The value can
    be the first or the least in alphabetical order.

    For example there are these two dictionaries/documents in a list,
    `test_list = [{ "name":"name_1" }, document_2 = { "name":"name_2" }`.

    `take_a_value_from_dict_list(test_list, "name")` will return `"name_1"`.
    `take_a_value_from_dict_list(test_list, "name", False)` will return
    `"name_2"`.

    PENDING: This function is not yet unit tested!
    """

    try:
        return sort_dict_list(_list, _name_column_target, _ascending)[0]\
            [_name_column_target]
    except IndexError:
        return []