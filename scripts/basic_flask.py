# Following [this tutorial](https://pytorch.org/tutorials/intermediate/flask_rest_api_tutorial.html)

from flask import Flask, jsonify
import albumentations as A
from albumentations.pytorch import ToTensorV2
from PIL import Image
import io
import numpy as np
from torchvision import models

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/predict')
def predict():
    return jsonify({'class_id' : 'IMAGE_NET_XXX', 'class_name' : 'Cat'})


def transform_image(image_bytes):
    my_transforms = A.Compose([
        A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
        ToTensorV2()
    ])
    image = np.asarray(Image.open(io.BytesIO(image_bytes)))
    img_transformed = my_transforms(image=image)
    return img_transformed['image'].unsqueeze(0)

with open("../data/birdies_fuji_crops/crops/positive/DSCF7099_0.png", 'rb') as f:
    image_bytes = f.read()
    tensor = transform_image(image_bytes=image_bytes)
    print(tensor)