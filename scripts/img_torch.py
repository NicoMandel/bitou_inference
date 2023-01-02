from flask import Flask, redirect, render_template, request
import os.path
import albumentations as A
from albumentations.pytorch import ToTensorV2
from PIL import Image
import io
import numpy as np
from torchvision import models
import json
import base64
from io import BytesIO
from werkzeug.utils import secure_filename


fdir=os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.abspath(os.path.join(fdir, '..', 'templates'))

allowed_exts = {'jpg', 'jpeg','png','JPG','JPEG','PNG'}
app = Flask(__name__, template_folder=template_dir)

imagenet_class_idx = json.load(open('config/imagenet_class_index.json'))
model = models.densenet121(weights=models.DenseNet121_Weights.DEFAULT)
model.eval()


def check_allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_exts

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

@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            print("No file attached to request")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print("No file Selected")
            return redirect(request.url)
        if file and check_allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("filename")
            # TODO: here is where it changes
            img = Image.open(file.stream)
            with BytesIO() as buf:
                img.save(buf, 'jpeg')
                image_bytes = buf.getvalue()
            encoded_string = base64.b64encode(image_bytes).decode() 
        img_bytes = file.read()
        class_id, class_name = get_prediction(image_bytes=img_bytes)
        return render_template('img.html', img_data=encoded_string, class_name = class_name, class_id = class_id), 200
    else:
        return render_template('img.html', img_data=""), 200

if __name__=="__main__":
    app.debug = True
    port = 5000
    app.run(host='0.0.0.0', port=port, debug=True)

