"""pedge

Usage:
    pedge.py (--help)
    pedge.py (--version)
    pedge.py delete (--config|--db|--log)...
    pedge.py set [--dbh=<dbhv>|--key=<keyv>|--cname=<cnamev>|--dbname=<dbnamev>|--port=<portv>]...
    pedge.py set [--cvgui|--db|--face|--picam|--pitch|--presence|--printlog|--rpi|--volume]...
    pedge.py set-default
    pedge.py show-config
    pedge.py start [--dh=<dbhv>|--key=<keyv>|--cname=<cnamev>|--dbname=<dbnamev>|--port=<portv>]...
    pedge.py start [--cvgui|--nodb|--noface|--nopitch|--nopresence|--noprintlog|[--rpi[--picam]]]...
    pedge.py start-default [--rpi[--picam]]
    pedge.py start-wizard

Options:
    --help|-h           refer to this help manual
    --version|-v        refer to this version of application

    --config            refer to configuration .ini file
    --db                refer to database
    --log               refer to a folder filled with offline "database"

    --dbh=<dbhv>        database ip address
    --dbname=<dbnamev>  database name
    --port=<portv>      database port

    --cname=<cnamev>    client name
    --key=<keyv>        ir key reference from lirc

    --nocvgui           run this application without opencv gui
    --nodb              run this application without database
    --noface            run this application without face detection
    --nopitch           run this application without pitch detection
    --nopresence        run this application without face-to-face presence detection
    --noprintlog        run this application without log
    --novolume          run this application without volume detection.

    --picam             start this application with web cam channeled with PICam
    --rpi               start this application in raspberry pi

    --save              save all mentioned setting into configuration .ini file

    delete              refer to delete operation
    set                 set values but don't start this application
    set-default         set all values to be default but don't start this application
    show-config         show configuration from .ini file
    start               start this application
    start-default       start this application with default setting value
    start-wizard        start this application with wizard
"""

import sys
sys.path.append("./src")
sys.path.append("./src/config_and_database")
sys.path.append("./src/cli")
sys.path.append("./src/detection")
sys.path.append("./src/loose_lib")
sys.path.append("./src/loose_lib/python-ipy")
sys.path.append("./src/manip")

from database_inserter import database_inserter
from detection_pv      import detection_pv
from docopt            import docopt
from sys               import platform

import cascade_front_face_default
import cli_docopt
import global_var
import manip_str
import os
import subprocess

if __name__ == "__main__":
    """ Clear the screen. """
    if   platform == "darwin" or platform == "linux" or platform == "linux2": subprocess.call(["reset"], shell=True)
    elif platform == "cygwin" or platform == "win32"                        : subprocess.call(["cls"], shell=True)

    """ docopt arguments. """
    doc_args       = docopt(__doc__, version="0.0.1")
    array_thread   = []
    cli_docopt.process_doc_args(doc_args)
    if global_var.application_start:
        di = None
        di = database_inserter(array_thread, "database_inserter", 5)

        if not manip_str.convert_str_to_bool(global_var.no_detection_face[global_var.runtime]):
            from detection_face import detection_face
            detection_face(array_thread, "detection_face", di)

        if not manip_str.convert_str_to_bool(global_var.no_detection_pitch[global_var.runtime]) or\
           not manip_str.convert_str_to_bool(global_var.no_detection_volume[global_var.runtime]):
            detection_pv(array_thread, "detection_pv", di)

        if not manip_str.convert_str_to_bool(global_var.use_rpi[global_var.runtime]):
            if not manip_str.convert_str_to_bool(global_var.no_detection_presence[global_var.runtime]):
                from detection_presence_ir import detection_presence_ir
                detection_presence_ir(array_thread, "detection_presence_ir", di)

        for i in array_thread: i.start()
        while True:
            try:
                for i in array_thread:
                    if i.isAlive() and i != None: i.join(1)
            except KeyboardInterrupt as error:
                for i in array_thread:
                    i.kill_me = True
                    os._exit(1)
