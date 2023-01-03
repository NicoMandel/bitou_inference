from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
# import urllib.request
import os.path
# Pytorch stuff
import json
import albumentations as A
from albumentations.pytorch import ToTensorV2
from torchvision import models
import numpy as np
from PIL import Image

imagenet_class_idx = json.load(open('config/imagenet_class_index.json'))
model = models.densenet121(weights=models.DenseNet121_Weights.DEFAULT)
model.eval()
my_transforms = A.Compose([
        A.Resize(255, 255),
        A.CenterCrop(224, 224),
        A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
        ToTensorV2()
    ])

basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(basedir, 'images')
app = Flask(__name__, static_folder=UPLOAD_FOLDER, static_url_path=UPLOAD_FOLDER)
app.secret_key = "secrety key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def open_image(filename):
	loc = url_for('static', filename=filename)
	fptr = Image.open(loc)
	return np.asarray(fptr)

# Pytorch Functions
def transform_image(filename):
    image = open_image(filename)
    img_transformed = my_transforms(image=image)
    return img_transformed['image'].unsqueeze(0)

def get_prediction(filename):
    tensor = transform_image(filename)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return imagenet_class_idx[predicted_idx]

# Flask Functions
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
		# TODO: in here, perform inference and store the new image. Then send the the new filename out
		class_id, class_name = get_prediction(filename)
		
		flash('Image successfully uploaded and displayed below. Image is class {}, which is a {}'.format(
			class_id, class_name
		))
		return render_template('upload.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename=filename), code=301)


if __name__=="__main__":
    # port = 5000
    # app.run(host='0.0.0.0', port=port)
	pass