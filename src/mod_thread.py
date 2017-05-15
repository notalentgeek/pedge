import sys
sys.path.append("./config_and_database")
sys.path.append("./cli")
sys.path.append("./detection")
sys.path.append("./loose_lib")
sys.path.append("./manip")

""" This is a super class for Python's threading.Thread. With additional
variables for counter, thread ID, thread name, and a termination flag.
"""
from threading import Thread

class mod_thread(Thread):

    def __init__(
        self,
        _counter,
        _id_thread,
        _name_thread
    ):

        Thread.__init__(self)

        self.counter     = _counter
        self.id_thread   = _id_thread
        self.name_thread = _name_thread

        """ Termination flag. """
        self.kill_me = False