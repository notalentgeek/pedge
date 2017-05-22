import sys
sys.path.append("../")
sys.path.append("../cli")
sys.path.append("../config_and_database")
sys.path.append("../loose_lib")
sys.path.append("../loose_lib/python-ipy")
sys.path.append("../manip")

from mod_thread import mod_thread
from timer      import timer_x_second

import database
import global_var
import lirc
import subprocess

class detection_presence_ir_receive(mod_thread):
    def __init__(
        self,
        _array_thread,
        _name_thread,
        _database_inserter
    ):

        """ Restart LIRC service. This is very important. """
        subprocess.call(["sudo /etc/init.d/lirc stop && timeout 2s  mode2 -d /dev/lirc0 & wait && sudo /etc/init.d/lirc restart"], shell=True)

        """ Setup super class. """
        _array_thread.append(self)
        mod_thread.__init__(
            self,
            _array_thread.index(self) + 1,
            _array_thread.index(self) + 1,
            _name_thread
        )
        """ Variable to contain `database_inserter` object. """
        self.database_inserter = _database_inserter
        """ Variable to contain timer. """
        self.timer = timer_x_second(global_var.timer_system_wide)

        """ Class - wide variables. """
        self.value_presence = []

        """ Initiate LIRC. """
        lirc.init("pysoc", blocking=False) # Change later!

    def run(self):
        while not self.kill_me:
            self.stream()
            self.timer.loop()
            """ If sample time (in second) passed then do pitch and volume
            detection.
            """
            if self.timer.please_update:
                if len(self.value_presence) > 0:
                    database.setup_document(
                        global_var.name_column_dict_detection,
                        global_var.name_table_presence,
                        self.value_presence,
                        self.database_inserter
                    )
                self.value_presence = []

    def stream(self):
        value_presence_temp = lirc.nextcode()
        print(value_presence_temp)
        if len(self.value_presence) == 0:
            self.value_presence.append(value_presence_temp)
        for i in self.value_presence:
            if not value_presence_temp in self.value_presence:
                self.value_presence.append(value_presence_temp)
                self.value_presence.sort()

class detection_presence_ir_send(mod_thread):
    def __init__(
        self,
        _array_thread,
        _name_thread
    ):
        """ Setup super class. """
        _array_thread.append(self)
        mod_thread.__init__(
            self,
            _array_thread.index(self) + 1,
            _array_thread.index(self) + 1,
            _name_thread
        )

        """ Class - wide variables. """
        self.counter_tick = 0
        self.interval_tick = 1000

    def run(self):
        while not self.kill_me:
            self.counter_tick = self.counter_tick + 1
            if self.counter_tick > self.interval_tick:
                self.counter_tick = 0
                subprocess.call(
                    [
                        "irsend SEND_ONCE {} {}".format(
                            "pysoc", # Change later to `global_var.name_application`.
                            global_var.key_ir[global_var.runtime]
                        )
                    ],
                    shell=True
                )