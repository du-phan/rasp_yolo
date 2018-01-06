from importlib import import_module
import os
import io 
from flask import Flask, render_template, Response, request, send_file
from darkflow.net.build import TFNet
import cv2
import time
from io import BytesIO
import time
import requests
from PIL import Image, ImageDraw
import numpy as np
import subprocess
import matplotlib.pyplot as plt
import numpy as np



options = {"model": "/cfg/yolo.cfg", 
           "load": "/weights/yolo.weights", 
           "threshold": 0.4,
           "GPU": 1.0}

tfnet = TFNet(options)

app = Flask(__name__)


def gen_detection(d):
    
    t0 = time.clock()

    # read and convert the binary image file
    curr_img = Image.open(BytesIO(d))
    curr_img_cv2 = cv2.cvtColor(np.array(curr_img), cv2.COLOR_RGB2BGR)

    t1 = time.clock()
    result = tfnet.return_predict(curr_img_cv2)
    print("Scoring time: {0} seconds".format((time.clock() - t1))) 

    draw = ImageDraw.Draw(curr_img)

    for det in result:
        
        draw.rectangle([det['topleft']['x'], det['topleft']['y'], 
                        det['bottomright']['x'], det['bottomright']['y']],
                        outline=(255, 0, 0))

        result_text = '{0} {1:.2f}%'.format(det['label'], det['confidence']*100)

        draw.text([det['topleft']['x'], det['topleft']['y'] - 13], result_text, fill=(255, 0, 0))


    # convert the jpeg type to binary data before sending it to the client side
    output = io.BytesIO()
    curr_img.save(output, format='JPEG')
    frame = output.getvalue()
            
    print("Full processing time: {} seconds\n".format(time.clock() - t0)) 

    yield frame



@app.route('/<path:path>/scoring_image', methods=["POST"])
def video_feed(path):

    r = request
    return Response(gen_detection(r.data), mimetype='image/jpg')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
