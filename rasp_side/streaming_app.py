from importlib import import_module
import os
import io
from io import BytesIO
from flask import Flask, render_template, Response
import requests
from PIL import Image, ImageDraw
#import cv2
import json
import time
from camera_pi import Camera

app = Flask(__name__)

camera = Camera()

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen(camera):

   while True:

      frame = camera.get_frame()

      headers = {'content_type': 'image/jpeg'}
      
      # DONT FORGET TO SET THE RIGHT FLOYDHUB URL! 
      response = requests.post('https://www.floydlabs.com/expose/zD8DfKW2msn29Tsh7hKDDj/scoring_image', headers=headers, data=frame)

      frame =  response.content

      yield (b'--frame\r\n'
             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/video_feed")
def video_feed():

  return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)


