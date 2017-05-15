import sys
sys.path.append("../")
sys.path.append("../config_and_database")
sys.path.append("../detection")
sys.path.append("../loose_lib")
sys.path.append("../loose_lib/python-ipy")
sys.path.append("../manip")

import cli_wizard
import config
import database
import global_var
import manip_file_or_folder
import manip_str

def set_first_run_to_false():
    config.set_value_to_config_file(
        global_var.config_section_value[global_var.flag],
        global_var.first_run[global_var.field],
        False
    )

def wizard_first_run():
    cli_wizard.start_wizard()
    global_var.application_start = True
    set_first_run_to_false()

def process_doc_args(_doc_args):
    """ Check if there is a configuration file exists. """
    if not config.check_config_file(): config.create_config_file()

    first_run = manip_str.convert_str_to_bool(config.get_value_from_config_file(
        global_var.config_section_value[global_var.flag],
        global_var.first_run[global_var.field]
    ))

    """ Delete. """
    if _doc_args.get(global_var.delete_cli):
        if _doc_args.get(global_var.config_cli):
            if manip_file_or_folder.path_is_file(global_var.uri_config):
                config.manip_file_or_folder.delete(global_var.uri_config)
                config.create_config_file()
        if _doc_args.get(global_var.db_cli):
            database.del_db(
                database.conn(
                    config.get_value_from_config_file(
                        global_var.config_section_value[global_var.database],
                        global_var.host_db[global_var.field]
                    )
                ),
                config.get_value_from_config_file(
                    global_var.config_section_value[global_var.database],
                    global_var.name_db[global_var.field]
                )
            )
        if _doc_args.get(global_var.log_cli):
            if manip_file_or_folder.path_is_folder(global_var.uri_folder_log):
                config.manip_file_or_folder.delete(global_var.uri_folder_log)
    """ Set. """
    if _doc_args.get(global_var.set_cli):
        """ Assign the configuration file. """
        if len(_doc_args.get(global_var.host_db[global_var.args]))     > 0          : config.set_value_to_config_file(global_var.config_section_value[global_var.database], global_var.host_db[global_var.field]    , _doc_args.get(global_var.host_db[global_var.args])[0])
        if len(_doc_args.get(global_var.key_ir[global_var.args]))      > 0          : config.set_value_to_config_file(global_var.config_section_value[global_var.client]  , global_var.key_ir[global_var.field]     , _doc_args.get(global_var.key_ir[global_var.args])[0])
        if len(_doc_args.get(global_var.name_client[global_var.args])) > 0          : config.set_value_to_config_file(global_var.config_section_value[global_var.client]  , global_var.name_client[global_var.field], _doc_args.get(global_var.name_client[global_var.args])[0])
        if len(_doc_args.get(global_var.name_db[global_var.args]))     > 0          : config.set_value_to_config_file(global_var.config_section_value[global_var.database], global_var.name_db[global_var.field]    , _doc_args.get(global_var.name_db[global_var.args])[0])
        if len(_doc_args.get(global_var.port_db[global_var.args]))     > 0          : config.set_value_to_config_file(global_var.config_section_value[global_var.database], global_var.port_db[global_var.field]    , _doc_args.get(global_var.port_db[global_var.args])[0])
        if _doc_args.get(global_var.no_db[global_var.args_set])                 == 1: config.inverse_value_boolean_of_config_file(global_var.config_section_value[global_var.setting], global_var.no_db[global_var.field])
        if _doc_args.get(global_var.no_detection_face[global_var.args_set])     == 1: config.inverse_value_boolean_of_config_file(global_var.config_section_value[global_var.setting], global_var.no_detection_face[global_var.field])
        if _doc_args.get(global_var.no_detection_pitch[global_var.args_set])    == 1: config.inverse_value_boolean_of_config_file(global_var.config_section_value[global_var.setting], global_var.no_detection_pitch[global_var.field])
        if _doc_args.get(global_var.no_detection_presence[global_var.args_set]) == 1: config.inverse_value_boolean_of_config_file(global_var.config_section_value[global_var.setting], global_var.no_detection_presence[global_var.field])
        if _doc_args.get(global_var.no_detection_volume[global_var.args_set])   == 1: config.inverse_value_boolean_of_config_file(global_var.config_section_value[global_var.setting], global_var.no_detection_volume[global_var.field])
        if _doc_args.get(global_var.no_print_log[global_var.args_set])          == 1: config.inverse_value_boolean_of_config_file(global_var.config_section_value[global_var.setting], global_var.no_print_log[global_var.field])
        if _doc_args.get(global_var.use_gui_opencv[global_var.args])            == 1: config.inverse_value_boolean_of_config_file(global_var.config_section_value[global_var.setting], global_var.use_gui_opencv[global_var.field])
        if _doc_args.get(global_var.use_rpi[global_var.args])                   == 1: config.inverse_value_boolean_of_config_file(global_var.config_section_value[global_var.setting], global_var.use_rpi[global_var.field])
        if _doc_args.get(global_var.use_rpi_cam[global_var.args])               == 1: config.inverse_value_boolean_of_config_file(global_var.config_section_value[global_var.setting], global_var.use_rpi_cam[global_var.field])
        set_first_run_to_false()
        config.show_config_file()
    """ Set every settings back to default. """
    if _doc_args.get(global_var.set_default_cli):
        config.set_config_file_all_to_default()
        set_first_run_to_false()
        config.show_config_file()
    """ Show configuration.ini file. """
    if _doc_args.get(global_var.show_config_cli):
        config.show_config_file()
    """ Start this application. """
    if _doc_args.get(global_var.start_cli):
        if first_run: wizard_first_run()
        else:
            global_var.application_start = True
            if len(_doc_args.get(global_var.host_db[global_var.args]))     > 0            : config.set_value_to_config_file(global_var.config_section_value[global_var.database]  , global_var.host_db[global_var.field]              , _doc_args.get(global_var.host_db[global_var.args])[0])
            if len(_doc_args.get(global_var.key_ir[global_var.args]))      > 0            : config.set_value_to_config_file(global_var.config_section_value[global_var.client]    , global_var.key_ir[global_var.field]               , _doc_args.get(global_var.key_ir[global_var.args])[0])
            if len(_doc_args.get(global_var.name_client[global_var.args])) > 0            : config.set_value_to_config_file(global_var.config_section_value[global_var.client]    , global_var.name_client[global_var.field]          , _doc_args.get(global_var.name_client[global_var.args])[0])
            if len(_doc_args.get(global_var.name_db[global_var.args]))     > 0            : config.set_value_to_config_file(global_var.config_section_value[global_var.database]  , global_var.name_db[global_var.field]              , _doc_args.get(global_var.name_db[global_var.args])[0])
            if len(_doc_args.get(global_var.port_db[global_var.args]))     > 0            : config.set_value_to_config_file(global_var.config_section_value[global_var.database]  , global_var.port_db[global_var.field]              , _doc_args.get(global_var.port_db[global_var.args])[0])
            if _doc_args.get(global_var.no_detection_face[global_var.args_start])     == 1: config.set_value_to_config_file(global_var.config_section_value[global_var.setting]   , global_var.no_detection_face[global_var.field]    , False)
            if _doc_args.get(global_var.no_detection_pitch[global_var.args_start])    == 1: config.set_value_to_config_file(global_var.config_section_value[global_var.setting]   , global_var.no_detection_pitch[global_var.field]   , False)
            if _doc_args.get(global_var.no_detection_presence[global_var.args_start]) == 1: config.set_value_to_config_file(global_var.config_section_value[global_var.setting]   , global_var.no_detection_presence[global_var.field], False)
            if _doc_args.get(global_var.no_detection_volume[global_var.args_start])   == 1: config.set_value_to_config_file(global_var.config_section_value[global_var.setting]   , global_var.no_detection_volume[global_var.field]  , False)
            if _doc_args.get(global_var.no_detection_volume[global_var.args_start])   == 1: config.set_value_to_config_file(global_var.config_section_value[global_var.setting]   , global_var.no_print_log[global_var.field]         , False)
            if _doc_args.get(global_var.use_gui_opencv[global_var.args])              == 1: config.set_value_to_config_file(global_var.config_section_value[global_var.setting]   , global_var.use_gui_opencv[global_var.field]       , True)
            if _doc_args.get(global_var.use_rpi[global_var.args])                     == 1: config.set_value_to_config_file(global_var.config_section_value[global_var.setting]   , global_var.use_rpi[global_var.field]              , True)
            if _doc_args.get(global_var.use_rpi_cam[global_var.args])                 == 1: config.set_value_to_config_file(global_var.config_section_value[global_var.setting]   , global_var.use_rpi_cam[global_var.field]          , True)
            config.set_runtime_all_to_config()
            set_first_run_to_false()
            global_var.application_start = True
        config.show_config_file()
    """ Start this application with all default value. """
    if _doc_args.get(global_var.start_default_cli):
        if first_run: wizard_first_run()
        else:
            config.set_runtime_all_to_default()
            if _doc_args.get(global_var.use_gui_opencv[global_var.args]) == 1: config.set_value_to_config_file(global_var.config_section_value[global_var.setting]   , global_var.use_gui_opencv[global_var.field]       , True)
            if _doc_args.get(global_var.use_rpi[global_var.args])        == 1: config.set_value_to_config_file(global_var.config_section_value[global_var.setting]   , global_var.use_rpi[global_var.field]              , True)
            if _doc_args.get(global_var.use_rpi_cam[global_var.args])    == 1: config.set_value_to_config_file(global_var.config_section_value[global_var.setting]   , global_var.use_rpi_cam[global_var.field]          , True)
            config.set_runtime_all_to_config()
            set_first_run_to_false()
            global_var.application_start = True
        config.show_config_file()
    """ Start this application with wizard. """
    if _doc_args.get(global_var.start_wizard_cli):
        cli_wizard.start_wizard()
        set_first_run_to_false()
        global_var.application_start = True
        config.show_config_file()