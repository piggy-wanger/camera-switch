import cv2
import threading
from flask import Response
from flask_restful import Resource, reqparse

from camera import USBCamera


lock = threading.Lock()
webcam = USBCamera()


def gen():
    global lock, webcam
    while True:
        with lock:
            frame = webcam.frame
            if frame is None:
                continue

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", frame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield (b'--frame\r\n' 
               b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')


class CameraSwitch(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'status', dest='status', type=bool, required=True, help='The order to switch the camera'
        )

    def post(self):
        global webcam
        args = self.parser.parse_args()
        status = args.status
        if status:
            try:
                webcam.camera_open()
                return {
                    'message': 'Open the camera successfully!',
                    'result': 'success'
                }
            except Exception as e:
                print('打开摄像头失败:', e)
                return {
                    'result': 'fail'
                }
        else:
            webcam.camera_close()
            return {
                'message': 'Close the camera'
            }


class Video(Resource):
    def get(self):
        print('Video has been loaded.')
        return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
