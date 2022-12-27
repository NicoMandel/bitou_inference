# Following [this tutorial](https://pytorch.org/tutorials/intermediate/flask_rest_api_tutorial.html)

from flask import Flask, jsonify, request
import albumentations as A
from albumentations.pytorch import ToTensorV2
from PIL import Image
import io
import numpy as np
from torchvision import models
import json

app = Flask(__name__)

model = models.densenet121(pretrained=True)
model.eval()
imagenet_class_idx = json.load(open('config/imagenet_class_index.json'))

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        class_id, class_name = get_prediction(image_bytes=img_bytes)
        return jsonify({'class_id' : class_id, 'class_name' : class_name})


def transform_image(image_bytes):
    my_transforms = A.Compose([
        A.Resize(255, 255),
        A.CenterCrop(224, 224),
        A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
        ToTensorV2()
    ])
    image = np.asarray(Image.open(io.BytesIO(image_bytes)))
    img_transformed = my_transforms(image=image)
    return img_transformed['image'].unsqueeze(0)

def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return imagenet_class_idx[predicted_idx]

with open("../data/birdies_fuji_crops/crops/positive/DSCF7099_0.png", 'rb') as f:
    image_bytes = f.read()
    print(get_prediction(image_bytes=image_bytes))