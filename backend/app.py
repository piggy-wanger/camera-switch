from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from CameraSwitch import *

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(CameraSwitch, '/camera_switch')
api.add_resource(Video, '/video')


if __name__ == '__main__':
    app.run()
