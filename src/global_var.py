import sys
sys.path.append("./config_and_database")
sys.path.append("./cli")
sys.path.append("./detection")
sys.path.append("./loose_lib")
sys.path.append("./manip")

""" tzlocal is a Python library to get UTC timezone. """
from tzlocal import get_localzone

import datetime
import os
import manip_file_or_folder

""" Fixing up `/root` issue in Raspbian. """
uri_default = os.path.expanduser("~")
if os.path.expanduser("~") == "/root":
    uri_default = "/home/pi"

""" Function that is used in this file. """
def get_dt():
    now      = str(datetime.datetime.now()).split(".")[0] # Remove the
                                                          # millisecond.
    date     = now .split(" ")[0]
    time     = now .split(" ")[1]
    year     = date.split("-")[0]
    month    = date.split("-")[1]
    day      = date.split("-")[2]
    hour     = time.split(":")[0]
    minute   = time.split(":")[1]
    second   = time.split(":")[2]
    dt       = "{}{}{}{}{}{}".format(year, month, day, hour, minute, second)
    timezone = str(get_localzone()).lower()

    return {
        name_column_day     : day,
        name_column_dt      : dt,
        name_column_hour    : hour,
        name_column_minute  : minute,
        name_column_month   : month,
        name_column_second  : second,
        name_column_timezone: timezone,
        name_column_year    : year
    }

""" Contents.
    * Configuration file.
    * Configuration file sections.
    * Configuration file dictionary columns.
    * Configuration fields.
    * Configuration.
    * Database naming constants.
    * Dictionary naming constants.
    * CLI commands.
    * CLI wizard strings.
    * CLI wizard templates.
    * Log.
    * Start application.
    * Timer.

Cascade.
"""
uri_cascade                            = manip_file_or_folder.join(
    uri_default,
    "cascade_face_front_default.xml"
)



""" Configuration file. """
ext_config_file                        = ".ini"
name_application                       = "pedge"
uri_config                             = manip_file_or_folder.join(uri_default, "config_{}.ini".format(name_application))



""" Configuration file sections. """
client                                 = "client"
database                               = "database"
flag                                   = "flag"
setting                                = "setting"



""" Configuration file dictionary columns. """
args                                   = "args"
args_set                               = "args_set"
args_start                             = "args_start"
default                                = "default"
field                                  = "field"
runtime                                = "runtime"



""" Configuration fields. """
config_section       = "section"
config_field         = "field"
config_section_value = {
    database: "database",
    flag    : "flag",
    setting : "setting",
    client  : "client"
}



""" Configuration. """
first_run = {
    args      : None,
    default   : True,
    field     : "first_run",
    runtime   : None
}
host_db = {
    args      : "--dbh",
    default   : "127.0.0.1",
    field     : "host_db",
    runtime   : None
}
key_ir = {
    args      : "--key",
    default   : "KEY_1",
    field     : "key_ir",
    runtime   : None
}
name_client = {
    args      : "--cname",
    default   : "testClient",
    field     : "name_client",
    runtime   : None
}
name_db = {
    args      : "--dbname",
    default   : "server_{}".format(name_application),
    field     : "name_db",
    runtime   : None
}
no_db = {
    args_set  : "--db",
    args_start: "--nodb",
    default   : False,
    field     : "no_db",
    runtime   : None
}
no_detection_face = {
    args_set  : "--face",
    args_start: "--noface",
    default   : False,
    field     : "no_face",
    runtime   : None
}
no_detection_pitch = {
    args_set  : "--pitch",
    args_start: "--nopitch",
    default   : False,
    field     : "no_pitch",
    runtime   : None
}
no_detection_presence = {
    args_set  : "--presence",
    args_start: "--nopresence",
    default   : False,
    field     : "no_presence",
    runtime   : None
}
no_detection_volume = {
    args_set  : "--pitch",
    args_start: "--nopitch",
    default   : False,
    field     : "no_volume",
    runtime   : None
}
no_print_log = {
    args_set  : "--printlog",
    args_start: "--noprintlog",
    default   : False,
    field     : "no_print_log",
    runtime   : None
}
port_db = {
    args      : "--port",
    default   : "28015",
    field     : "port_db",
    runtime   : None
}
use_gui_opencv = {
    args      : "--cvgui",
    default   : False,
    field     : "use_gui_opencv",
    runtime   : None
}
use_rpi = {
    args      : "--rpi",
    default   : False,
    field     : "use_rpi",
    runtime   : None
}
use_rpi_cam = {
    args      : "--picam",
    default   : False,
    field     : "use_rpi_cam",
    runtime   : None
}



"""Database naming constants."""
name_column_day                        = "day"
name_column_dt                         = "dt"
name_column_hour                       = "hour"
name_column_key_ir                     = "key_ir"
name_column_minute                     = "minute"
name_column_month                      = "month"
name_column_name_client                = "name"
name_column_second                     = "second"
name_column_timezone                   = "timezone"
name_column_value_detection            = "value"
name_column_year                       = "year"
name_table_client                      = "client"
name_table_face                        = "face"
name_table_pitch                       = "pitch"
name_table_presence                    = "presence"
name_table_volume                      = "volume"



""" Dictionary naming constants. """
name_column_dict_detection             = "detection"



""" CLI commands. """
config_cli                             = "--config"
db_cli                                 = "--db"
help_cli                               = "--help"
log_cli                                = "--log"
version_cli                            = "--version"
delete_cli                             = "delete"
set_cli                                = "set"
set_default_cli                        = "set-default"
show_config_cli                        = "show-config"
start_cli                              = "start"
start_default_cli                      = "start-default"
start_wizard_cli                       = "start-wizard"



""" CLI wizard strings. """
description                            = "description"
entry_input                            = "input"
example                                = "example"
requirement                            = "requirement"



""" CLI wizard templates. """
template_default                       = "default                  : do not fill and just press enter to fill the default value of \"{}\""
template_default_yes_or_no             = "default                  : do not fill and just press enter to automatically response \"yes\""
template_description                   = "please input             : {}"
template_description_yes_or_no         = "please specify components you want to use"
template_example                       = "example                  : {}"
template_example_yes_or_no             = "example                  : \"no\"/\"n\" for not using this features or \"yes\"/\"y\" for using this features"
template_input                         = "{:<25}: "
template_input_yes_or_no               = "do you want to use {} (y/n)? "
template_requirement                   = "requirement              : {}"
template_requirement_alpha_numeric     = "alpha-numeric"
template_requirement_case_camel        = "camelCase"
template_requirement_case_lower        = "lower case"
template_requirement_case_sensitive    = "case sensitive"
template_requirement_case_sensitive_no = "mot case sensitive"
template_requirement_case_underscore   = "underscore_case"
template_requirement_case_upper        = "upper_case"
template_requirement_numeric           = "numeric"
template_requirement_space_no          = "no space"
host_db_wizard = {
    default       :template_default.format(host_db[default]),
    description   :template_description.format("database IP address"),
    example       :template_example.format("127.0.0.1 or http://127.0.0.1"),
    entry_input   :template_input.format("database address"),
    requirement   :template_requirement.format("{}, {}, {}".format(
        template_requirement_alpha_numeric,
        template_requirement_case_sensitive_no,
        template_requirement_space_no
    ))
}
key_ir_wizard = {
    default       :template_default.format(key_ir[default]),
    description   :template_description.format("lirc registered ir code"),
    example       :template_example.format("KEY_1"),
    entry_input   :template_input.format("key ir"),
    requirement   :template_requirement.format("{}, {}, {}, {}".format(
        template_requirement_alpha_numeric,
        template_requirement_case_underscore,
        template_requirement_case_upper,
        template_requirement_space_no
    ))
}
name_client_wizard = {
    default       :template_default.format(name_client[default]),
    description   :template_description.format("client name"),
    example       :template_example.format("richardDawkins"),
    entry_input   :template_input.format("client name"),
    requirement   :template_requirement.format("{}, {}, {}, {}".format(
        template_requirement_alpha_numeric,
        template_requirement_case_camel,
        template_requirement_case_sensitive,
        template_requirement_space_no
    ))
}
name_db_wizard = {
    default       :template_default.format(name_db[default]),
    description   :template_description.format("database name"),
    example       :template_example.format("my_database"),
    entry_input   :template_input.format("database name"),
    requirement   :template_requirement.format("{}, {}, {}, {}".format(
        template_requirement_alpha_numeric,
        template_requirement_case_lower,
        template_requirement_case_underscore,
        template_requirement_space_no
    ))
}
port_db_wizard = {
    default       :template_default.format(port_db[default]),
    description   :template_description.format("database port"),
    example       :template_example.format("28015"),
    entry_input   :template_input.format("database port"),
    requirement   :template_requirement.format("{}, {}".format(
        template_requirement_numeric,
        template_requirement_space_no
    ))
}
no_db_wizard_input                     = template_input_yes_or_no.format("database")
no_detection_face_wizard_input         = template_input_yes_or_no.format("face detection")
no_detection_pitch_wizard_input        = template_input_yes_or_no.format("pitch detection")
no_detection_presence_wizard_input     = template_input_yes_or_no.format("presence detection")
no_detection_volume_wizard_input       = template_input_yes_or_no.format("volume detection")
no_print_log_wizard_input              = template_input_yes_or_no.format("log during runtime")
use_gui_opencv_wizard_input            = template_input_yes_or_no.format("opencv face detection gui")
use_rpi_cam_wizard_input               = template_input_yes_or_no.format("picam")
use_rpi_wizard_input                   = template_input_yes_or_no.format("raspberry pi")



""" Log. """
current_session                        = get_dt()[name_column_dt]
name_file_log                          = "log_{}_{}.txt".format(name_application, current_session)
name_folder_log                        = "log_{}".format(name_application)
uri_log                                = uri_default
uri_folder_log                         = manip_file_or_folder.join(uri_log, name_folder_log)
uri_file_log                           = manip_file_or_folder.join(uri_folder_log, name_file_log)



""" Start application. """
application_start                      = False



""" Timer. """
timer_system_wide                      = 1