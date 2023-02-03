import os.path
import torch
import numpy as np
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from csuinf.model import Model
from csuinf.utils import get_colour_decoder, overlay_images, extract_new_size, pad_image
from csuinf.geotiff_utils import is_not_empty, convert_idx
import albumentations as A
from albumentations.pytorch import ToTensorV2
from tqdm import tqdm
# from PIL import Image
import rasterio
from rasterio.windows import Window
from rasterio.plot import reshape_as_image, reshape_as_raster

fdir = os.path.abspath(os.path.dirname(__file__))

# Colour decoder
cdec_path = os.path.join(fdir, 'config', 'colour_code.json')
colour_decoder = get_colour_decoder(cdec_path)

# Model
model_f = os.path.join(fdir, 'best.pt')
model = Model.load_from_checkpoint(model_f)
model.eval()

# augmentations
window_height = window_width = 512
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
# app.config["MAX_CONTENT_LENGTH"] = 10 * 16 * 1024 * 1024

# File extensions check
ALLOWED_EXTENSIONS = set(['tif', 'tiff', 'geotif', 'geotiff'])

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
	outf_name = os.path.basename(filepath)
	outdir = os.path.dirname(filepath)
	outf = os.path.join(outdir, "_".join(["DNN", outf_name]))
	with rasterio.open(filepath, 'r') as src, rasterio.open(outf_name, 'w', **src.meta) as dst:
		cols = src.width // window_width
		rows = src.height // window_height
		
		tot_imgs = cols * rows
		for i in tqdm(range(tot_imgs)):
			start_x, start_y = convert_idx(window_width, window_height, cols, i)
			w = Window(start_y, start_x, window_width, window_height)
			blck = src.read(window = w)
			if is_not_empty(blck):
				img = reshape_as_image(blck)
				x = augmentations(image = img)['image'].unsqueeze(dim=0)
				with torch.no_grad():
					y_hat = model(x)
				labels = model.get_labels(y_hat)
				l = labels.cpu().numpy().astype(np.int8)
				mask = colour_decoder(l)
				overlay = overlay_images(img, mask)
				overlay = reshape_as_raster(overlay)
			else:
				overlay = blck
			
			dst.write(overlay, window = w)
	
	return outf_name

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
		# TODO: change here. Since it is a volume binding, it will not be required to save the input file
		masked_image_filename = run_inference(filepath=filename)
		flash('Image {} successfully uploaded:'.format(masked_image_filename))
		# return render_template('upload.html', filename=masked_image_filename)
		# TODO: save the output file and display the location where it ended up in "filename"
		return render_template('inference.html', name=masked_image_filename)
	else:
		flash('Allowed image types are -> {}'.format(ALLOWED_EXTENSIONS))
		return redirect(request.url)

if __name__ == "__main__":
	app.debug = True
	port = 5000
	app.run(host="0.0.0.0", debug=True, port=port)