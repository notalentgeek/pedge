import sys
sys.path.append("../")
sys.path.append("../cli")
sys.path.append("../detection")
sys.path.append("../loose_lib")
sys.path.append("../loose_lib/python-ipy")
sys.path.append("../manip")

import configparser
import global_var
import io
import manip_file_or_folder
import manip_str
import os
import sys
import timer

def check_config_file():
    """ Check if a file is exists. """
    if manip_file_or_folder.path_is_file(global_var.uri_config):
        """ Check if file extension is correct. """
        if global_var.uri_config.lower().endswith(global_var.ext_config_file):
            return True
    return False

def create_config_file():
    """ Create configuration file using FileIO. """
    io.FileIO        (global_var.uri_config, "w")
    config     = open(global_var.uri_config, "w")
    config_raw = configparser.ConfigParser()

    """ Add section to the configuration file. """
    config_raw.add_section(global_var.config_section_value[global_var.database])
    config_raw.add_section(global_var.config_section_value[global_var.flag])
    config_raw.add_section(global_var.config_section_value[global_var.setting])
    config_raw.add_section(global_var.config_section_value[global_var.client])

    """ Assign configuration for global_var.database. """
    config_raw.set(global_var.config_section_value[global_var.database], global_var.name_db[global_var.field]              , str(global_var.name_db[global_var.default]))
    config_raw.set(global_var.config_section_value[global_var.database], global_var.host_db[global_var.field]              , str(global_var.host_db[global_var.default]))
    config_raw.set(global_var.config_section_value[global_var.database], global_var.port_db[global_var.field]              , str(global_var.port_db[global_var.default]))
    """ Assign configuration for global_var.flag. """
    config_raw.set(global_var.config_section_value[global_var.flag]    , global_var.first_run[global_var.field]            , str(global_var.first_run[global_var.default]))
    """ Assign configuration for global_var.setting. """
    config_raw.set(global_var.config_section_value[global_var.setting] , global_var.no_db[global_var.field]                , str(global_var.no_db[global_var.default]))
    config_raw.set(global_var.config_section_value[global_var.setting] , global_var.no_detection_face[global_var.field]    , str(global_var.no_detection_face[global_var.default]))
    config_raw.set(global_var.config_section_value[global_var.setting] , global_var.no_detection_pitch[global_var.field]   , str(global_var.no_detection_pitch[global_var.default]))
    config_raw.set(global_var.config_section_value[global_var.setting] , global_var.no_detection_presence[global_var.field], str(global_var.no_detection_presence[global_var.default]))
    config_raw.set(global_var.config_section_value[global_var.setting] , global_var.no_detection_volume[global_var.field]  , str(global_var.no_detection_volume[global_var.default]))
    config_raw.set(global_var.config_section_value[global_var.setting] , global_var.no_print_log[global_var.field]         , str(global_var.no_print_log[global_var.default]))
    config_raw.set(global_var.config_section_value[global_var.setting] , global_var.use_gui_opencv[global_var.field]       , str(global_var.use_gui_opencv[global_var.default]))
    config_raw.set(global_var.config_section_value[global_var.setting] , global_var.use_rpi[global_var.field]              , str(global_var.use_rpi[global_var.default]))
    config_raw.set(global_var.config_section_value[global_var.setting] , global_var.use_rpi_cam[global_var.field]          , str(global_var.use_rpi_cam[global_var.default]))
    """ Assign configuration for global_var.client. """
    config_raw.set(global_var.config_section_value[global_var.client]  , global_var.key_ir[global_var.field]               , str(global_var.key_ir[global_var.default]))
    config_raw.set(global_var.config_section_value[global_var.client]  , global_var.name_client[global_var.field]          , str(global_var.name_client[global_var.default]))

    """ Write the configuration file. """
    config_raw.write(config)
    config.close()

def delete_config_file():
    if check_config_file():
        os.remove(global_var.uri_config)

def delete_section_from_config_file(*_section):
    config_raw = configparser.ConfigParser()
    with open(global_var.uri_config, "r") as config:
        config_raw.readfp(config)

    for i in _section:
        config_raw.remove_section(i)

    with open(global_var.uri_config, "w") as config:
        config_raw.write(config)

def delete_option_from_config_file(*_section_field_dict):
    config_raw = configparser.ConfigParser()
    with open(global_var.uri_config, "r") as config:
        config_raw.readfp(config)

    for i in _section_field_dict:
        config_raw.remove_option(i[global_var.config_section], i[global_var.config_field])

    with open(global_var.uri_config, "w") as config:
        config_raw.write(config)

def get_value_from_config_file(_section, _field):
    config_raw = configparser.ConfigParser()
    config_raw.read(global_var.uri_config)
    return config_raw.get(_section, _field)



def inverse_value_boolean_of_config_file(_section, _field):
    bool_temp = get_value_from_config_file(_section, _field)
    bool_temp = not manip_str.convert_str_to_bool(bool_temp)
    set_value_to_config_file(_section, _field, bool_temp)



def set_config_file_all_to_default():
    set_value_to_config_file(global_var.config_section_value[global_var.client]  , global_var.key_ir[global_var.field]               , str(global_var.key_ir[global_var.default]))
    set_value_to_config_file(global_var.config_section_value[global_var.client]  , global_var.name_client[global_var.field]          , str(global_var.name_client[global_var.default]))
    set_value_to_config_file(global_var.config_section_value[global_var.database], global_var.host_db[global_var.field]              , str(global_var.host_db[global_var.default]))
    set_value_to_config_file(global_var.config_section_value[global_var.database], global_var.name_db[global_var.field]              , str(global_var.name_db[global_var.default]))
    set_value_to_config_file(global_var.config_section_value[global_var.database], global_var.port_db[global_var.field]              , str(global_var.port_db[global_var.default]))
    set_value_to_config_file(global_var.config_section_value[global_var.flag]    , global_var.first_run[global_var.field]            , str(global_var.first_run[global_var.default]))
    set_value_to_config_file(global_var.config_section_value[global_var.setting] , global_var.no_db[global_var.field]                , str(global_var.no_db[global_var.default]))
    set_value_to_config_file(global_var.config_section_value[global_var.setting] , global_var.no_detection_face[global_var.field]    , str(global_var.no_detection_face[global_var.default]))
    set_value_to_config_file(global_var.config_section_value[global_var.setting] , global_var.no_detection_pitch[global_var.field]   , str(global_var.no_detection_pitch[global_var.default]))
    set_value_to_config_file(global_var.config_section_value[global_var.setting] , global_var.no_detection_presence[global_var.field], str(global_var.no_detection_presence[global_var.default]))
    set_value_to_config_file(global_var.config_section_value[global_var.setting] , global_var.no_detection_volume[global_var.field]  , str(global_var.no_detection_volume[global_var.default]))
    set_value_to_config_file(global_var.config_section_value[global_var.setting] , global_var.no_print_log[global_var.field]         , str(global_var.no_print_log[global_var.default]))
    set_value_to_config_file(global_var.config_section_value[global_var.setting] , global_var.use_gui_opencv[global_var.field]       , str(global_var.use_gui_opencv[global_var.default]))
    set_value_to_config_file(global_var.config_section_value[global_var.setting] , global_var.use_rpi[global_var.field]              , str(global_var.use_rpi[global_var.default]))
    set_value_to_config_file(global_var.config_section_value[global_var.setting] , global_var.use_rpi_cam[global_var.field]          , str(global_var.use_rpi_cam[global_var.default]))

def set_config_file_all_to_runtime():
    set_value_to_config_file(global_var.config_section_value[global_var.client]  , global_var.key_ir[global_var.field]               , str(global_var.key_ir[global_var.runtime]))
    set_value_to_config_file(global_var.config_section_value[global_var.client]  , global_var.name_client[global_var.field]          , str(global_var.name_client[global_var.runtime]))
    set_value_to_config_file(global_var.config_section_value[global_var.database], global_var.host_db[global_var.field]              , str(global_var.host_db[global_var.runtime]))
    set_value_to_config_file(global_var.config_section_value[global_var.database], global_var.name_db[global_var.field]              , str(global_var.name_db[global_var.runtime]))
    set_value_to_config_file(global_var.config_section_value[global_var.database], global_var.port_db[global_var.field]              , str(global_var.port_db[global_var.runtime]))
    set_value_to_config_file(global_var.config_section_value[global_var.flag]    , global_var.first_run[global_var.field]            , str(global_var.first_run[global_var.runtime]))
    set_value_to_config_file(global_var.config_section_value[global_var.setting] , global_var.no_db[global_var.field]                , str(global_var.no_db[global_var.runtime]))
    set_value_to_config_file(global_var.config_section_value[global_var.setting] , global_var.no_detection_face[global_var.field]    , str(global_var.no_detection_face[global_var.runtime]))
    set_value_to_config_file(global_var.config_section_value[global_var.setting] , global_var.no_detection_pitch[global_var.field]   , str(global_var.no_detection_pitch[global_var.runtime]))
    set_value_to_config_file(global_var.config_section_value[global_var.setting] , global_var.no_detection_presence[global_var.field], str(global_var.no_detection_presence[global_var.runtime]))
    set_value_to_config_file(global_var.config_section_value[global_var.setting] , global_var.no_detection_volume[global_var.field]  , str(global_var.no_detection_volume[global_var.runtime]))
    set_value_to_config_file(global_var.config_section_value[global_var.setting] , global_var.no_print_log[global_var.field]         , str(global_var.no_print_log[global_var.runtime]))
    set_value_to_config_file(global_var.config_section_value[global_var.setting] , global_var.use_gui_opencv[global_var.field]       , str(global_var.use_gui_opencv[global_var.runtime]))
    set_value_to_config_file(global_var.config_section_value[global_var.setting] , global_var.use_rpi[global_var.field]              , str(global_var.use_rpi[global_var.runtime]))
    set_value_to_config_file(global_var.config_section_value[global_var.setting] , global_var.use_rpi_cam[global_var.field]          , str(global_var.use_rpi_cam[global_var.runtime]))

def set_runtime_all_to_default():
    global_var.first_run[global_var.runtime]             = global_var.first_run[global_var.default]
    global_var.host_db[global_var.runtime]               = global_var.host_db[global_var.default]
    global_var.key_ir[global_var.runtime]                = global_var.key_ir[global_var.default]
    global_var.name_client[global_var.runtime]           = global_var.name_client[global_var.default]
    global_var.name_db[global_var.runtime]               = global_var.name_db[global_var.default]
    global_var.no_db[global_var.runtime]                 = global_var.no_db[global_var.default]
    global_var.no_detection_face[global_var.runtime]     = global_var.no_detection_face[global_var.default]
    global_var.no_detection_pitch[global_var.runtime]    = global_var.no_detection_pitch[global_var.default]
    global_var.no_detection_presence[global_var.runtime] = global_var.no_detection_presence[global_var.default]
    global_var.no_detection_volume[global_var.runtime]   = global_var.no_detection_volume[global_var.default]
    global_var.no_print_log[global_var.runtime]          = global_var.no_print_log[global_var.default]
    global_var.port_db[global_var.runtime]               = global_var.port_db[global_var.default]
    global_var.use_gui_opencv[global_var.runtime]        = global_var.use_gui_opencv[global_var.default]
    global_var.use_rpi[global_var.runtime]               = global_var.use_rpi[global_var.default]
    global_var.use_rpi_cam[global_var.runtime]           = global_var.use_rpi_cam[global_var.default]

def set_runtime_all_to_config():
    global_var.first_run[global_var.runtime]             = get_value_from_config_file(global_var.config_section_value[global_var.flag]    , global_var.first_run[global_var.field])
    global_var.host_db[global_var.runtime]               = get_value_from_config_file(global_var.config_section_value[global_var.database], global_var.host_db[global_var.field])
    global_var.key_ir[global_var.runtime]                = get_value_from_config_file(global_var.config_section_value[global_var.client]  , global_var.key_ir[global_var.field])
    global_var.name_client[global_var.runtime]           = get_value_from_config_file(global_var.config_section_value[global_var.client]  , global_var.name_client[global_var.field])
    global_var.name_db[global_var.runtime]               = get_value_from_config_file(global_var.config_section_value[global_var.database], global_var.name_db[global_var.field])
    global_var.no_db[global_var.runtime]                 = manip_str.convert_str_to_bool(get_value_from_config_file(global_var.config_section_value[global_var.setting] , global_var.no_db[global_var.field]))
    global_var.no_detection_face[global_var.runtime]     = manip_str.convert_str_to_bool(get_value_from_config_file(global_var.config_section_value[global_var.setting] , global_var.no_detection_face[global_var.field]))
    global_var.no_detection_pitch[global_var.runtime]    = manip_str.convert_str_to_bool(get_value_from_config_file(global_var.config_section_value[global_var.setting] , global_var.no_detection_pitch[global_var.field]))
    global_var.no_detection_presence[global_var.runtime] = manip_str.convert_str_to_bool(get_value_from_config_file(global_var.config_section_value[global_var.setting] , global_var.no_detection_presence[global_var.field]))
    global_var.no_detection_volume[global_var.runtime]   = manip_str.convert_str_to_bool(get_value_from_config_file(global_var.config_section_value[global_var.setting] , global_var.no_detection_volume[global_var.field]))
    global_var.no_print_log[global_var.runtime]          = manip_str.convert_str_to_bool(get_value_from_config_file(global_var.config_section_value[global_var.setting] , global_var.no_print_log[global_var.field]))
    global_var.port_db[global_var.runtime]               = manip_str.convert_str_to_bool(get_value_from_config_file(global_var.config_section_value[global_var.database], global_var.port_db[global_var.field]))
    global_var.use_gui_opencv[global_var.runtime]        = get_value_from_config_file(global_var.config_section_value[global_var.setting], global_var.use_gui_opencv[global_var.field])
    global_var.use_rpi[global_var.runtime]               = manip_str.convert_str_to_bool(get_value_from_config_file(global_var.config_section_value[global_var.setting] , global_var.use_rpi[global_var.field]))
    global_var.use_rpi_cam[global_var.runtime]           = manip_str.convert_str_to_bool(get_value_from_config_file(global_var.config_section_value[global_var.setting] , global_var.use_rpi_cam[global_var.field]))

def set_section_to_config_file(_section, _section_new):
    _section_new = str(_section_new)
    config_raw   = configparser.ConfigParser()
    with open(global_var.uri_config, "r") as config:
        config_raw.readfp(config)

    section_item_list = config_raw.items(_section)
    section_new = config_raw.add_section(_section_new)

    for f, v in section_item_list:
        config_raw.set(_section_new, f, v)

    config_raw.remove_section(_section)

    with open(global_var.uri_config, "w") as config:
        config_raw.write(config)


def set_value_to_config_file(_section, _field, _value):
    _value     = str(_value)
    config_raw = configparser.ConfigParser()
    config_raw.read(global_var.uri_config)
    config_raw.set(_section, _field, _value)
    with open(global_var.uri_config, "w") as config:
        config_raw.write(config)

def show_config_runtime():
    print("="*50)
    print("values from runtime")
    print("="*50)
    print("{:<25}: {}".format(global_var.first_run[global_var.field]            , str(global_var.first_run[global_var.runtime])))
    print("{:<25}: {}".format(global_var.host_db[global_var.field]              , str(global_var.host_db[global_var.runtime])))
    print("{:<25}: {}".format(global_var.key_ir[global_var.field]               , str(global_var.key_ir[global_var.runtime])))
    print("{:<25}: {}".format(global_var.name_client[global_var.field]          , str(global_var.name_client[global_var.runtime])))
    print("{:<25}: {}".format(global_var.name_db[global_var.field]              , str(global_var.name_db[global_var.runtime])))
    print("{:<25}: {}".format(global_var.port_db[global_var.field]              , str(global_var.port_db[global_var.runtime])))
    print("{:<25}: {}".format(global_var.no_db[global_var.field]                , str(global_var.no_db[global_var.runtime])))
    print("{:<25}: {}".format(global_var.no_detection_face[global_var.field]    , str(global_var.no_detection_face[global_var.runtime])))
    print("{:<25}: {}".format(global_var.no_detection_pitch[global_var.field]   , str(global_var.no_detection_pitch[global_var.runtime])))
    print("{:<25}: {}".format(global_var.no_detection_presence[global_var.field], str(global_var.no_detection_presence[global_var.runtime])))
    print("{:<25}: {}".format(global_var.no_detection_volume[global_var.field]  , str(global_var.no_detection_volume[global_var.runtime])))
    print("{:<25}: {}".format(global_var.no_print_log[global_var.field]         , str(global_var.no_print_log[global_var.runtime])))
    print("{:<25}: {}".format(global_var.use_gui_opencv[global_var.field]       , str(global_var.use_gui_opencv[global_var.runtime])))
    print("{:<25}: {}".format(global_var.use_rpi[global_var.field]              , str(global_var.use_rpi[global_var.runtime])))
    print("{:<25}: {}".format(global_var.use_rpi_cam[global_var.field]          , str(global_var.use_rpi_cam[global_var.runtime])))
    print("="*50)

def show_config_file():
    print("="*50)
    print("values from configuration .ini file")
    print("="*50)
    print("{:<25}: {}".format(global_var.first_run[global_var.field]            , get_value_from_config_file(global_var.config_section_value[global_var.flag]    , global_var.first_run[global_var.field])))
    print("{:<25}: {}".format(global_var.host_db[global_var.field]              , get_value_from_config_file(global_var.config_section_value[global_var.database], global_var.host_db[global_var.field])))
    print("{:<25}: {}".format(global_var.key_ir[global_var.field]               , get_value_from_config_file(global_var.config_section_value[global_var.client]  , global_var.key_ir[global_var.field])))
    print("{:<25}: {}".format(global_var.name_client[global_var.field]          , get_value_from_config_file(global_var.config_section_value[global_var.client]  , global_var.name_client[global_var.field])))
    print("{:<25}: {}".format(global_var.name_db[global_var.field]              , get_value_from_config_file(global_var.config_section_value[global_var.database], global_var.name_db[global_var.field])))
    print("{:<25}: {}".format(global_var.port_db[global_var.field]              , get_value_from_config_file(global_var.config_section_value[global_var.database], global_var.port_db[global_var.field])))
    print("{:<25}: {}".format(global_var.no_db[global_var.field]                , get_value_from_config_file(global_var.config_section_value[global_var.setting] , global_var.no_db[global_var.field])))
    print("{:<25}: {}".format(global_var.no_detection_face[global_var.field]    , get_value_from_config_file(global_var.config_section_value[global_var.setting] , global_var.no_detection_face[global_var.field])))
    print("{:<25}: {}".format(global_var.no_detection_pitch[global_var.field]   , get_value_from_config_file(global_var.config_section_value[global_var.setting] , global_var.no_detection_pitch[global_var.field])))
    print("{:<25}: {}".format(global_var.no_detection_presence[global_var.field], get_value_from_config_file(global_var.config_section_value[global_var.setting] , global_var.no_detection_presence[global_var.field])))
    print("{:<25}: {}".format(global_var.no_detection_volume[global_var.field]  , get_value_from_config_file(global_var.config_section_value[global_var.setting] , global_var.no_detection_volume[global_var.field])))
    print("{:<25}: {}".format(global_var.no_print_log[global_var.field]         , get_value_from_config_file(global_var.config_section_value[global_var.setting] , global_var.no_print_log[global_var.field])))
    print("{:<25}: {}".format(global_var.use_gui_opencv[global_var.field]       , get_value_from_config_file(global_var.config_section_value[global_var.setting] , global_var.use_gui_opencv[global_var.field])))
    print("{:<25}: {}".format(global_var.use_rpi[global_var.field]              , get_value_from_config_file(global_var.config_section_value[global_var.setting] , global_var.use_rpi[global_var.field])))
    print("{:<25}: {}".format(global_var.use_rpi_cam[global_var.field]          , get_value_from_config_file(global_var.config_section_value[global_var.setting] , global_var.use_rpi_cam[global_var.field])))
    print("="*50)

""" Mini "unit test". """
if __name__ == "__main__":
    delete_config_file()
    create_config_file()
    print(check_config_file())
    print(get_value_from_config_file(global_var.config_section_value[global_var.database], global_var.host_db[global_var.field]))
    set_value_to_config_file(global_var.config_section_value[global_var.database], global_var.host_db[global_var.field], "192.168.1.1")
    set_section_to_config_file(global_var.config_section_value[global_var.database], "database_new")
    set_section_to_config_file("database_new", global_var.config_section_value[global_var.database])
    show_config_runtime()
    show_config_file()
    set_config_file_all_to_runtime()
    show_config_runtime()
    delete_option_from_config_file({ global_var.config_section: global_var.config_section_value[global_var.database], global_var.config_field: global_var.host_db[global_var.field] }, { global_var.config_section: global_var.config_section_value[global_var.flag], global_var.config_field: global_var.first_run[global_var.field] })
    delete_section_from_config_file(global_var.config_section_value[global_var.database], global_var.config_section_value[global_var.setting])