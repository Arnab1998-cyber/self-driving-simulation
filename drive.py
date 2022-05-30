from flask import Flask
import socketio
import eventlet
import numpy as np
from tensorflow.keras.models import load_model
import base64
from io import BytesIO
from PIL import Image
from preprocess import preprocess


app=Flask(__name__)
sio = socketio.Server()
speed_limit = 10

@sio.on('telemetry')
def telemetry(sid, data):
    print(data)
    speed= float(data['speed'])
    image=Image.open(BytesIO(base64.b64decode(data['image'])))
    image = np.asarray(image)
    image = preprocess(image)
    steering = model.predict(image)[0][0]
    throttle = 1.0 - speed/speed_limit
    send_control(steering=steering,throttle=throttle)


@sio.on('connect')
def connect(sid, venv):
    print('connect')
    send_control(0,0)

def send_control(steering, throttle):
    sio.emit('steer', data={
        'steering_angle': steering.__str__(),
        'throttle': throttle.__str__()
    })


if __name__ == '__main__':
    model=load_model('drive.h5')
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
