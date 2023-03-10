import os.path
import torch
import numpy as np
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from csuinf.model import Model
from csuinf.utils import get_colour_decoder, overlay_images, load_image, extract_new_size, pad_image
import albumentations as A
from albumentations.pytorch import ToTensorV2
from PIL import Image

fdir = os.path.abspath(os.path.dirname(__file__))

# Colour decoder
cdec_path = os.path.join(fdir, 'config', 'colour_code.json')
colour_decoder = get_colour_decoder(cdec_path)

# Model
model_f = os.path.join(fdir, 'best.pt')
model = Model.load_from_checkpoint(model_f)
model.eval()
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

# augmentations
preprocess_params = model.get_preprocessing_parameters()
mean = tuple(preprocess_params["mean"])
std = tuple(preprocess_params['std'])
augmentations = A.Compose([
	A.Normalize(mean=mean, std=std),
	ToTensorV2(transpose_mask=True)
])

# Setting up Flask
UPLOAD_FOLDER = os.path.join(fdir, 'images')
app = Flask(__name__, static_url_path=UPLOAD_FOLDER, static_folder=UPLOAD_FOLDER)
app.secret_key = "secret_key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 16 * 1024 * 1024

# File extensions check
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	

# Functions to perform inference
def rescale_image(img : torch.Tensor, msg: str) -> torch.Tensor:
    """
        function to pad the image if necessary by the architecture
    """
    nshape = extract_new_size(msg)
    nimg = pad_image(img, nshape)
    return nimg

def run_inference(filepath : str) -> str:
	"""
		Function to run the actual inference.
		Gets a filepath
		Returns a filepath to the overlaid image
	"""
	img = load_image(filepath)
	x = img.copy()
	x = augmentations(image=x)['image'].unsqueeze(dim=0).to(device)
	with torch.no_grad():
		try:
			y_hat = model(x)
		except RuntimeError as e:
			nx = rescale_image(x, e)
			y_hat = model(nx)
			
	labels = model.get_labels(y_hat)
	l = labels.detach().cpu().numpy().astype(np.int8)
	mask = colour_decoder(l)
	overlay = overlay_images(img, mask)
	img_name = "mask.jpg"
	out_img = Image.fromarray(overlay)
	out_img.save(url_for('static', filename=img_name))
	return img_name

# Functions that perform display
# @app.route('/')
# def upload_form():
# 	return render_template('upload.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/infer', methods=['POST'])
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
		masked_image_filename = run_inference(url_for('static', filename=filename))
		# os.remove(filename)
		#print('upload_image filename: ' + filename)
		flash('Image {} successfully uploaded:'.format(filename))
		# return render_template('upload.html', filename=masked_image_filename)
		return render_template('inference.html', name=filename, filename=masked_image_filename)
	else:
		flash('Allowed image types are -> {}'.format(ALLOWED_EXTENSIONS))
		return redirect(request.url)

if __name__ == "__main__":
	app.debug = True
	port = 5000
	app.run(host="0.0.0.0", debug=True, port=port)