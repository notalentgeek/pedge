"""server_pedge

Usage:
    server_pedge.py (--help|-h)
    server_pedge.py (--version|-v)
    server_pedge.py [--dbh=<dbhv>|--dbn=<dbnv>|--nodb|--tout=<toutv>]...
    server_pedge.py [--cert=<certv>|--key=<keyv>]...
    server_pedge.py [--https|-o]...

Options:
    --help -h      Refer to this help manual.
    --version -v   Refer to this web server version.

    --dbh=<dbhv>   RethinkDB database host [default: 127.0.0.1].
    --dbn=<dbnv>   RethinkDB database name [default: server_pedge].
    --nodb         Run this web server without RethinkDB database.
    --tout=<toutv> Connection timeout. Amount of this web server needs to wait for
                   database connection [default: 5].

    --cert=<certv> Certificate for https
                   [default: /etc/ssl/certs/apache-selfsigned.crt].
    --key=<keyv>   Private file for https
                   [default: /etc/ssl/private/apache-selfsigned.key].
    --https        Start this web web server with HTTPS.

    -o             Make this web server to be available online.
"""

import sys
sys.path.append("./src")
sys.path.append("./src/config_and_database")
sys.path.append("./src/cli")
sys.path.append("./src/detection")
sys.path.append("./src/loose_lib")
sys.path.append("./src/loose_lib/python-ipy")
sys.path.append("./src/manip")

from docopt         import docopt          as doc
from flask          import Flask
from flask          import render_template
from flask_socketio import emit
from flask_socketio import SocketIO
from socket         import socket
from sys            import platform

import database
import global_var
import manip_str
import rethinkdb as r
import subprocess

""" Function to get table API in JSON format. """
def get_table_api(
    _c,          # Connection.
    _name_table, # Table name to be turned into JSON API.
    _name_db,    # Database name.
    _no_db=False # Whether this web server runs with database.
):
    if _no_db: return "this web server is running without connection to database"
    else     : return str(list(database.get_table(_c, _name_table, _name_db)))



""" Function to get latest `dt` from the `client` table. This meant to get the
date and time for the latest data inputted into database.
"""
def get_input_latest(_c, _name_db):
    latest_input_float = None
    latest_input_str   = None

    for i in database.get_table(_c, global_var.name_table_client, _name_db):
        latest_input_str_temp   = i.get(global_var.name_column_dt)
        latest_input_float_temp = float(latest_input_str_temp)/1000

        if latest_input_float == None:
            latest_input_float = latest_input_float_temp
            latest_input_str   = latest_input_str_temp

        if latest_input_float < latest_input_float_temp:
            latest_input_float = latest_input_float_temp
            latest_input_str   = latest_input_str_temp

    return latest_input_str



if __name__ == "__main__":
    """ Clear the screen. """
    if   platform == "darwin" or platform == "linux" or platform == "linux2": subprocess.call(["reset"], shell=True)
    elif platform == "cygwin" or platform == "win32"                        : subprocess.call(["cls"], shell=True)

    """ docopt arguments. """
    doc_args        = doc(__doc__, version="0.0.1")
    cert            = str(doc_args["--cert"][0])
    host_db         = str(doc_args["--dbh"][0])
    key             = str(doc_args["--key"][0])
    name_db         = str(doc_args["--dbn"][0])
    timeout         = int(doc_args["--tout"][0])
    https           = True if (int(doc_args["--https"]) == 1) else (False if (int(doc_args["--https"]) == 0) else None)
    no_db           = True if (int(doc_args["--nodb" ]) == 1) else (False if (int(doc_args["--nodb" ]) == 0) else None)
    online          = True if (int(doc_args["-o"     ]) == 1) else (False if (int(doc_args["-o"     ]) == 0) else None)
    """ Flask and SocketIO. """
    app             = Flask(__name__)
    https_context   = (cert, key)
    socket_io       = SocketIO(app)

    """ CAUTION: learned the hard way here, that RethinkDB connection should not be
    put in parallel functions. Here, I set different connection object per -
    decorator.
    """

    """ Routings. """
    @app.route("/")
    def index(): return render_template("index.html")

    @app.route("/api/" + global_var.name_table_client)
    def api_client():
        if   no_db: return "web server is running without connection to database server"
        else      :
            return str(list(database.get_table(
                database.conn(host_db, timeout),
                global_var.name_table_client,
                name_db
            )));

    @app.route("/api/" + global_var.name_table_face + "/<_name_client>")
    def api_face(_name_client):
        if   no_db: return "web server is running without connection to database server"
        else      :
            return str(list(database.get_table(
                database.conn(host_db, timeout),
                "{}_{}".format(global_var.name_table_face, _name_client),
                name_db
            )));

    @app.route("/api/" + global_var.name_table_pitch + "/<_name_client>")
    def api_pitch(_name_client):
        if   no_db: return "web server is running without connection to database server"
        else      :
            return str(list(database.get_table(
                database.conn(host_db, timeout),
                "{}_{}".format(global_var.name_table_pitch, _name_client),
                name_db
            )));

    @app.route("/api/" + global_var.name_table_presence + "/<_name_client>")
    def api_presence(_name_client):
        if   no_db: return "web server is running without connection to database server"
        else      :
            return str(list(database.get_table(
                database.conn(host_db, timeout),
                "{}_{}".format(global_var.name_table_presence, _name_client),
                name_db
            )));

    @app.route("/api/" + global_var.name_table_volume + "/<_name_client>")
    def api_volume(_name_client):
        if   no_db: return "web server is running without connection to database server"
        else      :
            return str(list(database.get_table(
                database.conn(host_db, timeout),
                "{}_{}".format(global_var.name_table_volume, _name_client),
                name_db
            )));

    """ Web socket routings. """
    @socket_io.on("request_input_dt")
    def request_input_dt(_data_received):
        if not no_db:
            c_temp = database.conn(host_db, timeout)
            dt     = _data_received[global_var.name_column_dt]

            if not no_db:
                """ Create database and client table if they are not exists. """
                database.create_db   (c_temp, name_db)
                database.create_table(c_temp, global_var.name_table_client, name_db)

                data_sent    = []
                table_client = database.get_table(c_temp, global_var.name_table_client, name_db)

                for i in table_client:
                    name_client_temp = i.get(global_var.name_column_name_client)
                    face_temp        = database.get_doc_first_value(c_temp, dt, global_var.name_column_dt, global_var.name_column_value_detection, "{}_{}".format(global_var.name_table_face    , name_client_temp), name_db)
                    pitch_temp       = database.get_doc_first_value(c_temp, dt, global_var.name_column_dt, global_var.name_column_value_detection, "{}_{}".format(global_var.name_table_pitch   , name_client_temp), name_db)
                    presence_temp    = database.get_doc_first_value(c_temp, dt, global_var.name_column_dt, global_var.name_column_value_detection, "{}_{}".format(global_var.name_table_presence, name_client_temp), name_db)
                    volume_temp      = database.get_doc_first_value(c_temp, dt, global_var.name_column_dt, global_var.name_column_value_detection, "{}_{}".format(global_var.name_table_volume  , name_client_temp), name_db)
                    #i[global_var.name_column_dt] = dt;
                    if type(face_temp)     is not list: i[global_var.name_table_face]     = face_temp
                    if type(pitch_temp)    is not list: i[global_var.name_table_pitch]    = pitch_temp
                    if type(presence_temp) is not list: i[global_var.name_table_presence] = presence_temp
                    if type(volume_temp)   is not list: i[global_var.name_table_volume]   = volume_temp
                    data_sent.append(i)

                emit("sent_input", data_sent)

    @socket_io.on("request_input_latest")
    def request_input_latest():
        if not no_db:
            c_temp = database.conn(host_db, timeout)
            if not no_db:
                """ Create database and client table if they are not exists. """
                database.create_db   (c_temp, name_db)
                database.create_table(c_temp, global_var.name_table_client, name_db)

                data_sent    = []
                table_client = database.get_table(c_temp, global_var.name_table_client, name_db)
                input_latest = get_input_latest(c_temp, name_db)

                for i in table_client:
                    if i.get(global_var.name_column_dt) == input_latest:
                        name_client_temp = i.get(global_var.name_column_name_client)
                        #face_temp        = database.get_doc_first_value(c_temp, input_latest, global_var.name_column_dt, global_var.name_column_value_detection, "{}_{}".format(global_var.name_table_face    , name_client_temp), name_db)
                        #print(face_temp)
                        pitch_temp       = database.get_doc_first_value(c_temp, input_latest, global_var.name_column_dt, global_var.name_column_value_detection, "{}_{}".format(global_var.name_table_pitch   , name_client_temp), name_db)
                        #presence_temp    = database.get_doc_first_value(c_temp, input_latest, global_var.name_column_dt, global_var.name_column_value_detection, "{}_{}".format(global_var.name_table_presence, name_client_temp), name_db)
                        volume_temp      = database.get_doc_first_value(c_temp, input_latest, global_var.name_column_dt, global_var.name_column_value_detection, "{}_{}".format(global_var.name_table_volume  , name_client_temp), name_db)
                        #i[global_var.name_column_dt] = dt;
                        #if type(face_temp)     is not list: i[global_var.name_table_face]     = face_temp
                        #if type(pitch_temp)    is not list: i[global_var.name_table_pitch]    = pitch_temp
                        #if type(presence_temp) is not list: i[global_var.name_table_presence] = presence_temp
                        #if type(volume_temp)   is not list: i[global_var.name_table_volume]   = volume_temp
                        data_sent.append(i)

                emit("sent_input", data_sent)

    @socket_io.on("request_input_to_database")
    def request_input_to_database(_data_received):
        if not no_db:
            c_temp = database.conn(host_db, timeout)
            #print(_data_received)
            #if global_var.name_column_name_client             in _data_received: print("{:<20}: {}".format("name_client"       , _data_received[global_var.name_column_name_client]))
            #if global_var.name_column_dt                      in _data_received: print("{:<20}: {}".format("dt"                , _data_received[global_var.name_column_dt]))
            #if global_var.name_table_face     in _data_received: print("{:<20}: {}".format("detection_face"    , _data_received[global_var.name_table_face]))
            #if global_var.name_table_pitch    in _data_received: print("{:<20}: {}".format("detection_pitch"   , _data_received[global_var.name_table_pitch]))
            #if global_var.name_table_presence in _data_received: print("{:<20}: {}".format("detection_presence", _data_received[global_var.name_table_presence]))
            #if global_var.name_table_volume   in _data_received: print("{:<20}: {}".format("detection_volume"  , _data_received[global_var.name_table_volume]))
            if global_var.name_column_dt in _data_received:
                value_dt_temp = _data_received[global_var.name_column_dt]
                if global_var.name_column_name_client in _data_received:
                    doc_client_table_temp                                           = {}
                    doc_client_table_temp[global_var.name_column_dt]                = value_dt_temp
                    doc_client_table_temp[global_var.name_column_name_client]       = _data_received[global_var.name_column_name_client]
                if global_var.name_table_face in _data_received:
                    doc_face_table_temp                                             = {}
                    doc_face_table_temp[global_var.name_column_dt]                  = value_dt_temp
                    doc_face_table_temp[global_var.name_column_value_detection]     = _data_received[global_var.name_table_face]
                if global_var.name_table_pitch in _data_received:
                    doc_pitch_table_temp                                            = {}
                    doc_pitch_table_temp[global_var.name_column_dt]                 = value_dt_temp
                    doc_pitch_table_temp[global_var.name_column_value_detection]    = _data_received[global_var.name_table_pitch]
                if global_var.name_table_presence in _data_received:
                    doc_presence_table_temp                                         = {}
                    doc_presence_table_temp[global_var.name_column_dt]              = value_dt_temp
                    doc_presence_table_temp[global_var.name_column_value_detection] = _data_received[global_var.name_table_presence]
                if global_var.name_table_volume in _data_received:
                    doc_volume_table_temp                                           = {}
                    doc_volume_table_temp[global_var.name_column_dt]                = value_dt_temp
                    doc_volume_table_temp[global_var.name_column_value_detection]   = _data_received[global_var.name_table_volume]
                name_client_temp = _data_received[global_var.name_column_name_client]
                r.expr([
                    database.create_db(c_temp, name_db, True),                                                                      # Create database.
                    database.create_table(c_temp, global_var.name_table_client, name_db, True),                                     # Create table for client.
                    database.create_table(c_temp, "{}_{}".format(global_var.name_table_face    , name_client_temp), name_db, True), # Create table for face.
                    database.create_table(c_temp, "{}_{}".format(global_var.name_table_pitch   , name_client_temp), name_db, True), # Create table for pitch.
                    database.create_table(c_temp, "{}_{}".format(global_var.name_table_presence, name_client_temp), name_db, True), # Create table for presence.
                    database.create_table(c_temp, "{}_{}".format(global_var.name_table_volume  , name_client_temp), name_db, True)  # Create table for volume.
                ]).run(c_temp)
                # Update data for client. Check for existing client document.
                check_client = database.get_doc_first_value(
                    c_temp,
                    name_client_temp,
                    global_var.name_column_name_client,
                    global_var.name_column_name_client,
                    global_var.name_table_client,
                    name_db
                )
                if isinstance(check_client, list):
                    database.create_doc(
                        c_temp,
                        doc_client_table_temp,
                        global_var.name_table_client,
                        name_db,
                        [global_var.name_column_dt]
                    )
                else:
                    database.update_doc_first_value(
                        c_temp,
                        name_client_temp,
                        value_dt_temp,
                        global_var.name_column_name_client,
                        global_var.name_column_dt,
                        global_var.name_table_client,
                        name_db
                    )
                # Update data for face value.
                if global_var.name_table_face in _data_received:
                    database.create_doc(
                        c_temp,
                        doc_face_table_temp,
                        "{}_{}".format(global_var.name_table_face, name_client_temp),
                        name_db,
                        [global_var.name_column_dt]
                    )
                # Update data for pitch value.
                if global_var.name_table_pitch in _data_received:
                    database.create_doc(
                        c_temp,
                        doc_pitch_table_temp,
                        "{}_{}".format(global_var.name_table_pitch, name_client_temp),
                        name_db,
                        [global_var.name_column_dt]
                    )
                # Update data for presence value.
                if global_var.name_table_presence in _data_received:
                    database.create_doc(
                        c_temp,
                        doc_presence_table_temp,
                        "{}_{}".format(global_var.name_table_presence, name_client_temp),
                        name_db,
                        [global_var.name_column_dt]
                    )
                # Update data for volume value.
                if global_var.name_table_volume in _data_received:
                    database.create_doc(
                        c_temp,
                        doc_volume_table_temp,
                        "{}_{}".format(global_var.name_table_volume, name_client_temp),
                        name_db,
                        [global_var.name_column_dt]
                    )

    @socket_io.on("request_table_client")
    def request_table_client():
        if not no_db:
            emit("sent_table_client", list(database.get_table(database.conn(host_db, timeout), global_var.name_table_client, name_db)))

    @socket_io.on("request_table_face")
    def request_table_face(_data_received):
        if not no_db:
            emit("sent_table_face", list(database.get_table(database.conn(host_db, timeout), _data_received["name_table"], name_db)))

    @socket_io.on("request_table_pitch")
    def request_table_pitch(_data_received):
        if not no_db:
            emit("sent_table_pitch", list(database.get_table(database.conn(host_db, timeout), _data_received["name_table"], name_db)))

    @socket_io.on("request_table_presence")
    def request_table_presence(_data_received):
        if not no_db:
            emit("sent_table_presence", list(database.get_table(database.conn(host_db, timeout), _data_received["name_table"], name_db)))

    @socket_io.on("request_table_volume")
    def request_table_volume(_data_received):
        if not no_db:
            emit("sent_table_volume", list(database.get_table(database.conn(host_db, timeout), _data_received["name_table"], name_db)))

    """ If `https == True` change all `http` into `https` in `./templates/index.html`.
    If `https == False` change all `https` into `http` in `./templates/index.html`.
    """
    """
    if https:
        manip_str.file_search_and_replace_exact("./templates/index.html", "http", "https")
    else    :
        manip_str.file_search_and_replace_exact("./templates/index.html", "https", "http")
    """

    if online:
        if https: socket_io.run(app, host="0.0.0.0", ssl_context=https_context) # Start with HTTPS.
        else:     socket_io.run(app, host="0.0.0.0")                            # Start without HTTPS.
    else:         socket_io.run(app)                                            # Start this web server locally.