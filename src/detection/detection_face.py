import sys
sys.path.append("../")
sys.path.append("../cli")
sys.path.append("../config_and_database")
sys.path.append("../loose_lib")
sys.path.append("../loose_lib/python-ipy")
sys.path.append("../manip")

from mod_thread import mod_thread
from timer      import timer_x_second

import cv2
import database
import global_var
import manip_str

class detection_face(mod_thread):
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

        """ Class - wide variables."""
        self.cam = None
        """ There are 2 different cases for face detection when using Raspbian
        in Raspberry PI variant boards: using normal USB web cam and using
        PICamera.

        Normal USB web cam is usual normal web cam people can find in general
        consumer electronics store.

        PICamera is a ribbon camera specially designed for Raspberry PI.

        If not using PICamera means that this application runs with normal
        USB web cam.
        """
        if manip_str.convert_str_to_bool(global_var.use_rpi_cam[global_var.runtime]):
            """ Import additional libraries. """
            from picamera       import PiCamera
            from picamera.array import PiRGBArray
            """ Assign PICamera variables. """
            self.cam            = PiCamera()
            self.cam.framerate  = 32
            self.cam.resolution = (640, 480)
            self.raw_capture    = PiRGBArray(self.cam)
        else:
            self.cam = cv2.VideoCapture(0) # Get the first available camera on
                                           # the system.
        """ Variables for face detection. """
        self.cascade_face = cv2.CascadeClassifier(global_var.uri_cascade)

        self.frame                    = None # Frame captured from cam.
        self.return_value             = None # Return value from cam.
        self.value_face_list          = []   # All detected face.

    def run(self):
        if self.kill_me:
            self.stream_stop()

        while not self.kill_me:
            self.stream()
            self.timer.loop()
            """ If sample time (in second) passed then do pitch and volume
            detection.
            """
            if self.timer.please_update: self.detection_face()

    def detection_face(self):
        if self.return_value:
            """ Convert captured frame into greyscale. """
            grey_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            """ Face detection. """
            self.value_face_list = self.cascade_face.detectMultiScale(
                grey_frame,
                scaleFactor =1.1,
                minNeighbors=5,
                minSize     =(30, 30),
                flags       =cv2.CASCADE_SCALE_IMAGE
            )
            value_face = len(self.value_face_list)
            """ Process face detection before inserting it into database."""
            if value_face > 0:
                """ Insert to database. """
                database.setup_document(
                    global_var.name_column_dict_detection,
                    global_var.name_table_face,
                    value_face,
                    self.database_inserter
                )

    def stream(self):
        if manip_str.convert_str_to_bool(global_var.use_rpi_cam[global_var.runtime]):
            self.cam.capture(self.raw_capture, format="bgr")
            self.frame        = self.raw_capture.array
            self.return_value = True
        else:
            self.return_value, self.frame = self.cam.read()

        """ Draw the face detection GUI or not. """
        if manip_str.convert_str_to_bool(global_var.use_gui_opencv[global_var.runtime]):
            if len(self.value_face_list) > 0:
                for (x, y, w, h) in self.value_face_list:
                    cv2.rectangle(
                        self.frame,
                        (x, y),
                        (x + w, y + h),
                        (0, 0, 255),
                        2
                    )
            cv2.startWindowThread()
            cv2.namedWindow(global_var.name_table_face)
            cv2.imshow(global_var.name_table_face, self.frame)

            """ Do not forget to clear cache when using PICamera.
            This is very important!
            """
            if manip_str.convert_str_to_bool(global_var.use_rpi_cam[global_var.runtime]): self.raw_capture.truncate(0)

    def stream_stop(self):
        cv2.destroyAllWindows()
        self.cam.release()