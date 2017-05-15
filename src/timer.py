import sys
sys.path.append("./config_and_database")
sys.path.append("./cli")
sys.path.append("./detection")
sys.path.append("./loose_lib")
sys.path.append("./manip")

import database
import global_var

""" This class is to detect change in `_x` second. """
class timer_x_second(object):
    def __init__(self, _x):
        self.counter            = 0

        self.please_update      = False
        self.current_second     = global_var.get_dt()[global_var.name_column_second]
        self.interval_in_second = _x
        self.stored_second      = self.current_second

    def loop(self):
        self.dt             = global_var.get_dt()
        self.current_second = self.dt[global_var.name_column_second]

        """ If there is a change in second then this means that a second has
        passed.
        """
        if self.current_second != self.stored_second:
            self.stored_second = self.current_second
            self.counter       = self.counter + 1

        if self.counter >= self.interval_in_second:
              self.please_update = True
              self.counter       = 0
        else: self.please_update = False