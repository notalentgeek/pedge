import sys
sys.path.append("../")
sys.path.append("../config_and_database")
sys.path.append("../detection")
sys.path.append("../loose_lib")
sys.path.append("../loose_lib/python-ipy")
sys.path.append("../manip")

import check_string
import config
import database
import global_var
import manip_str

def start_wizard():
    def input_wizard_template(
        _description,
        _requirement,
        _example,
        _default,
        _entry_input,
        _config_var,
        _check_function
    ):
        description = "\n{}".format(_description)
        while True:
            print(description)
            print(_requirement)
            print(_example)
            print(_default)

            description = _description

            """ Replace "http://" or "https://". """
            value_input = input(_entry_input)\
                .replace("http://", "")\
                .replace("https://", "")\
                .replace("/", "");

            """ If `value_input` is blank. """
            if not bool(value_input.strip()):
                _config_var[global_var.runtime] = _config_var[global_var.default]
                break
            elif _check_function(value_input):
                _config_var[global_var.runtime] = value_input
                break
            print("\ninput failed\n")
    def input_wizard_template_host_db_wizard()    : input_wizard_template(global_var.host_db_wizard[global_var.description]    , global_var.host_db_wizard[global_var.requirement]    , global_var.host_db_wizard[global_var.example]    , global_var.host_db_wizard[global_var.default]    , global_var.host_db_wizard[global_var.entry_input]    , global_var.host_db    , check_string.check_host_db)
    def input_wizard_template_key_ir_wizard()     : input_wizard_template(global_var.key_ir_wizard[global_var.description]     , global_var.key_ir_wizard[global_var.requirement]     , global_var.key_ir_wizard[global_var.example]     , global_var.key_ir_wizard[global_var.default]     , global_var.key_ir_wizard[global_var.entry_input]     , global_var.key_ir     , check_string.check_key_ir)
    def input_wizard_template_name_client_wizard(): input_wizard_template(global_var.name_client_wizard[global_var.description], global_var.name_client_wizard[global_var.requirement], global_var.name_client_wizard[global_var.example], global_var.name_client_wizard[global_var.default], global_var.name_client_wizard[global_var.entry_input], global_var.name_client, check_string.check_name_client)
    def input_wizard_template_name_db_wizard()    : input_wizard_template(global_var.name_db_wizard[global_var.description]    , global_var.name_db_wizard[global_var.requirement]    , global_var.name_db_wizard[global_var.example]    , global_var.name_db_wizard[global_var.default]    , global_var.name_db_wizard[global_var.entry_input]    , global_var.name_db    , check_string.check_name_db)
    def input_wizard_template_port_db_wizard()    : input_wizard_template(global_var.port_db_wizard[global_var.description]    , global_var.port_db_wizard[global_var.requirement]    , global_var.port_db_wizard[global_var.example]    , global_var.port_db_wizard[global_var.default]    , global_var.port_db_wizard[global_var.entry_input]    , global_var.port_db    , check_string.check_port_db)
    def input_wizad_boolean_template(
        _input,
        _config_var,
        _inverse
    ):
        while True:
            value_input = input(_input)

            if   not bool(value_input.strip())                 : _config_var[global_var.runtime] = False if _inverse else True
            elif     manip_str.convert_str_to_bool(value_input): _config_var[global_var.runtime] = False if _inverse else True
            elif not manip_str.convert_str_to_bool(value_input): _config_var[global_var.runtime] = True  if _inverse else False
            else                                               : _config_var[global_var.runtime] = None

            if _config_var[global_var.runtime] != None: break
            print("\ninput failed\n")
    def input_wizad_boolean_template_no_db_wizard()                : input_wizad_boolean_template(global_var.no_db_wizard_input                , global_var.no_db                , True)
    def input_wizad_boolean_template_no_detection_face_wizard()    : input_wizad_boolean_template(global_var.no_detection_face_wizard_input    , global_var.no_detection_face    , True)
    def input_wizad_boolean_template_no_detection_pitch_wizard()   : input_wizad_boolean_template(global_var.no_detection_pitch_wizard_input   , global_var.no_detection_pitch   , True)
    def input_wizad_boolean_template_no_detection_presence_wizard(): input_wizad_boolean_template(global_var.no_detection_presence_wizard_input, global_var.no_detection_presence, True)
    def input_wizad_boolean_template_no_detection_volume_wizard()  : input_wizad_boolean_template(global_var.no_detection_volume_wizard_input  , global_var.no_detection_volume  , True)
    def input_wizad_boolean_template_no_print_log_wizard()         : input_wizad_boolean_template(global_var.no_print_log_wizard_input         , global_var.no_print_log         , True)
    def input_wizad_boolean_template_use_gui_opencv_wizard()       : input_wizad_boolean_template(global_var.use_gui_opencv_wizard_input       , global_var.use_gui_opencv       , False)
    def input_wizad_boolean_template_use_rpi_cam_wizard()          : input_wizad_boolean_template(global_var.use_rpi_cam_wizard_input          , global_var.use_rpi_cam          , False)
    def input_wizad_boolean_template_use_rpi_wizard()              : input_wizad_boolean_template(global_var.use_rpi_wizard_input              , global_var.use_rpi              , False)
    input_wizard_template_name_client_wizard()
    input_wizard_template_host_db_wizard()
    input_wizard_template_name_db_wizard()
    input_wizard_template_port_db_wizard()
    input_wizard_template_key_ir_wizard()
    print("\n{}".format(global_var.template_description_yes_or_no))
    print(global_var.template_example_yes_or_no)
    print(global_var.template_default_yes_or_no)
    input_wizad_boolean_template_no_db_wizard()
    input_wizad_boolean_template_no_detection_face_wizard()
    input_wizad_boolean_template_no_detection_pitch_wizard()
    input_wizad_boolean_template_no_detection_presence_wizard()
    input_wizad_boolean_template_no_detection_volume_wizard()
    input_wizad_boolean_template_use_gui_opencv_wizard()
    input_wizad_boolean_template_no_print_log_wizard()
    input_wizad_boolean_template_use_rpi_cam_wizard()
    input_wizad_boolean_template_use_rpi_wizard()
    config.set_config_file_all_to_runtime()

""" Mini "unit test"."""
if __name__ == "__main__":
    config.delete_config_file()
    config.create_config_file()
    start_wizard()
    config.show_config_file()