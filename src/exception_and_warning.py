import sys
sys.path.append("./config_and_database")
sys.path.append("./cli")
sys.path.append("./detection")
sys.path.append("./loose_lib")
sys.path.append("./manip")

import warnings as warn

def c_warning(
    _object_name:str,
    _object_type:str,
    _function_where_convention_defined:str,
    _file_where_convention_defined:str
):
    warn.warn(
        "{} {} is not according to the naming convention in {} in {}".format(
            _object_type,
            _object_name,
            _function_where_convention_defined,
            _file_where_convention_defined
        ),
        ConventionWarning,
        stacklevel=3
    )

def cd_warning(
    _object_name:str,
    _object_type:str,
    _created_or_deleted:bool,
    _function_where_convention_defined:str,
    _file_where_convention_defined:str
):
    _created_or_deleted = "created" if _created_or_deleted else "deleted"

    warn.warn(
        "{} {}".format(
            "{} {} is not {} due to string".format(
                _object_name,
                _object_type,
                _created_or_deleted
            ),
            "check retuning false in `{}` in `{}.py`.".format(
                _function_where_convention_defined,
                _file_where_convention_defined
            )
        ),
        CreationDeletionWarning,
        stacklevel=3
    )

class ConventionWarning(Warning):
    pass

class CreationDeletionWarning(Warning):
    pass
