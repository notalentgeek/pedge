import sys
sys.path.append("../")
sys.path.append("../cli")
sys.path.append("../config_and_database")
sys.path.append("../loose_lib")
sys.path.append("../loose_lib/python-ipy")
sys.path.append("../manip")

from mod_thread import mod_thread
from sys        import platform
from timer      import timer_x_second

import alsaaudio
import aubio
import database
import global_var
import manip_str
import numpy as num
import pyaudio
import timer

class detection_pv(mod_thread):
    def __init__(
        self,
        _array_thread,
        _name_thread,
        _database_inserter
    ):
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

        """ Pitch and volume detection variables. """
        buffer_size = 2048
        channel     = 1
        format_pa   = pyaudio.paFloat32
        format_alsa = alsaaudio.PCM_FORMAT_FLOAT_LE
        method      = "default"
        sample_rate = 44100
        hop_size    = buffer_size//2
        pa          = pyaudio.PyAudio() # Initiating PyAudio object.
        self.period = hop_size

        """ There is a problem with PyAudio running in Linus at the point this
        codes are written. The problem is that PyAudio is unable to determine
        default audio I/O devices. The error is `IOError: No Default Output
        Device Available`.

        The fix is to use `pyalsaaudio` to interface with audio I/O. However,
        `pyalsaaudio` is not cross - platform (it is only for Linux operating
        system). So, PyAudio is preferred if it has no problems.

        If not using Linux then try to use PyAudio.
        If using Linux Raspbian then use PyAudio.
        If using Linux then use `pyalsaaudio`.
        """
        if platform == "linux" or platform == "linux2" and not global_var.use_rpi[global_var.runtime]:
            self.mic = alsaaudio.PCM(type=alsaaudio.PCM_CAPTURE)
            self.mic.setchannels(channel)
            self.mic.setformat(format_alsa)
            self.mic.setperiodsize(self.period)
            self.mic.setrate(sample_rate)
        else:
            self.mic = pa.open(
                channels          =channel,
                format            =format_pa,
                frames_per_buffer =self.period,
                input             =True,
                input_device_index=2 if manip_str.convert_str_to_bool(global_var.use_rpi[global_var.runtime]) else None,
                rate              =sample_rate
            )

        """ Create the pitch detection object. """
        self.detection_pitch = aubio.pitch(
            method,
            buffer_size,
            hop_size,
            sample_rate
        )
        self.detection_pitch.set_unit("Hz")   # Set unit.
        self.detection_pitch.set_silence(-40) # Ignore incoming sound below
                                              # -40 dB.

        """ Variable to contain streamed data. """
        self.stream_data = None

    def run(self):
        while not self.kill_me:
            self.stream()     # Keep the microphone audio stream open.
            self.timer.loop() # Update the timer.
            """ If sample time (in second) passed then do pitch and volume
            detection.
            """
            if self.timer.please_update: self.detection_pv()

    def detection_pv(self):
        sample       = num.fromstring(self.stream_data, dtype=aubio.float_type)
        value_pitch  = self.detection_pitch(sample)[0]
        value_volume = num.sum(sample**2)/len(sample)
        value_volume = "{:.6f}".format(value_volume)

        """ Insert to database. """
        database.setup_document(
            global_var.name_column_dict_detection,
            global_var.name_table_pitch,
            value_pitch,
            self.database_inserter
        )
        database.setup_document(
            global_var.name_column_dict_detection,
            global_var.name_table_volume,
            value_volume,
            self.database_inserter
        )

    def stream(self):
        if platform == "linux" or platform == "linux2" and not global_var.use_rpi[global_var.runtime]:
            length, self.stream_data = self.mic.read()
        else:
            self.stream_data = self.mic.read(
                self.period,
                exception_on_overflow=False
            )