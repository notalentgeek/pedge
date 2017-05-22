import sys
sys.path.append("../")
sys.path.append("../cli")
sys.path.append("../detection")
sys.path.append("../loose_lib")
sys.path.append("../loose_lib/python-ipy")
sys.path.append("../manip")

from mod_thread import mod_thread

import config
import database
import global_var
import json
import manip_file_or_folder
import manip_str
import os
import rethinkdb as r
import timer

class database_inserter(mod_thread):
    def __init__(
        self,
        _array_thread,
        _name_thread,
        _timeout
    ):
        """ Setup super class. """
        _array_thread.append(self)
        mod_thread.__init__(
            self,
            _array_thread.index(self) + 1,
            _array_thread.index(self) + 1,
            _name_thread
        )
        self.data_insert  = []            # Queue for data to be put into
                                          # database.

        """ Create the log folder. """
        manip_file_or_folder.create_file_of_folder(
            global_var.uri_log,
            False,
            global_var.name_folder_log
        )
        """ Create the log file. """
        manip_file_or_folder.create_file_of_folder(
            global_var.uri_folder_log,
            True,
            global_var.name_file_log
        )

        """ Creating persistent database connection. """
        if not global_var.no_db[global_var.runtime]:
            self.c = database.conn(
                global_var.host_db[global_var.runtime],
                _timeout
            )

    def run(self):
        while not self.kill_me:
            """ Check if there is at least a data in queue. """
            if len(self.data_insert) > 0:
                log        = ""   # Log string.
                json_raw   = {}
                json_ready = None # JSON formatted.

                """ Take the first element to be put into database. """
                data_first_in  = self.data_insert[0]
                detection      = data_first_in[global_var.name_column_dict_detection]
                dt             = data_first_in[global_var.name_column_dt]
                timezone       = data_first_in[global_var.name_column_timezone]
                value          = data_first_in[global_var.name_column_value_detection]

                """ This application needs to re - adjust incoming data from
                `"presence"` detection. The IR key received from the running
                detection class should be matched with client name.
                """
                print(detection)
                if detection == global_var.name_table_presence:
                    value_temp = []
                    print(value)
                    if type(value) == str:
                        value = manip_str.convert_str_to_list(value)
                    for i in value:
                        value_temp.append(database.get_doc_first_value(
                            self.c,
                            value,
                            global_var.name_column_key_ir,
                            global_var.name_column_name_client,
                            global_var.name_table_client,
                            global_var.name_db[global_var.runtime]
                        ))
                    value_temp = str(value_temp).replace("['", "").replace("', '", ",").replace("']", "")
                    value      = value_temp
                value = str(value)

                """ Package the JSON raw. """
                json_raw[global_var.name_column_dt]              = str(dt)
                json_raw[global_var.name_column_timezone]        = str(timezone)
                json_raw[global_var.name_column_value_detection] = str(value)
                """ Setup the JSON file. """
                json_ready = json.loads(json.dumps(json_raw))
                """ Add informations to log. """
                log = log + global_var.name_client[global_var.runtime] + "-"
                log = log + dt                                         + "-"
                log = log + timezone                                   + "-"
                log = log + detection                                  + "-"
                log = log + value
                if not global_var.no_db[global_var.runtime]:
                    """ Insert it into database. """
                    try:
                        r.expr([
                            database.create_doc(
                                self.c,
                                json_ready,
                                "{}_{}".format(detection, global_var.name_client[global_var.runtime]),
                                global_var.name_db[global_var.runtime],
                                [global_var.name_column_dt],
                                True
                            ),
                            database.update_doc_first_value(
                                self.c,
                                global_var.name_client[global_var.runtime],
                                dt,
                                global_var.name_column_name_client,
                                global_var.name_column_dt,
                                global_var.name_table_client,
                                global_var.name_db[global_var.runtime],
                                True
                            ),
                            database.update_doc_first_value(
                                self.c,
                                global_var.name_client[global_var.runtime],
                                global_var.key_ir[global_var.runtime],
                                global_var.name_column_name_client,
                                global_var.name_column_key_ir,
                                global_var.name_table_client,
                                global_var.name_db[global_var.runtime],
                                True
                            )
                        ]).run(self.c)
                    except r.ReqlOpFailedError as e:
                        database.create_db(
                            self.c,
                            global_var.name_db[global_var.runtime]
                        )
                        database.create_table(
                            self.c,
                            global_var.name_table_client,
                            global_var.name_db[global_var.runtime]
                        )
                        database.create_table(
                            self.c,
                            "{}_{}".format(detection, global_var.name_client[global_var.runtime]),
                            global_var.name_db[global_var.runtime]
                        )
                        database.create_doc(
                            self.c,
                            json_ready,
                            "{}_{}".format(detection, global_var.name_client[global_var.runtime]),
                            global_var.name_db[global_var.runtime],
                            [global_var.name_column_dt]
                        )
                        dict_client = {}
                        dict_client[global_var.name_column_dt]          = str(dt)
                        dict_client[global_var.name_column_key_ir]      = global_var.key_ir[global_var.runtime]
                        dict_client[global_var.name_column_name_client] = global_var.name_client[global_var.runtime]
                        database.create_doc(
                            self.c,
                            dict_client,
                            global_var.name_table_client,
                            global_var.name_db[global_var.runtime],
                            [global_var.name_column_dt]
                        )
                """ Print the `log`. """
                if not global_var.no_print_log[global_var.runtime]: print(log)
                """ Write the log file. """
                with open(global_var.uri_file_log, "a") as file_log: file_log.write(log + "\n")
                """ Remove the data from the list. """
                self.data_insert.pop(0)