import os.path
import torch
import numpy as np
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from csuinf.model import Model
from csuinf.utils import get_colour_decoder, overlay_images, extract_new_size, pad_image
from csuinf.geotiff_utils import is_not_empty, convert_idx, get_tiff_files, ALLOWED_EXTENSIONS, PROCESSED_PREFIX, JOIN_CHAR
import albumentations as A
from albumentations.pytorch import ToTensorV2
from tqdm import tqdm
# from PIL import Image
import rasterio
from rasterio.windows import Window
from rasterio.plot import reshape_as_image, reshape_as_raster

# Filenames
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
	# Use url_for('static', filename) here
	inf_name = os.path.basename(filepath)
	outf_name = JOIN_CHAR.join([PROCESSED_PREFIX, inf_name])
	outf = url_for('static', filename = outf_name)
	with rasterio.open(filepath, 'r') as src, rasterio.open(outf, 'w', **src.meta) as dst:
		cols = src.width // window_width
		rows = src.height // window_height
		
		tot_imgs = cols * rows
		for i in tqdm(range(tot_imgs)):
			start_x, start_y = convert_idx(window_width, window_height, cols, i)
			w = Window(start_y, start_x, window_width, window_height)
			blck = src.read(window = w)
			if is_not_empty(blck):
				img = reshape_as_image(blck)
				x = augmentations(image = img)['image'].unsqueeze(dim=0).to(device)
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
    return render_template('index.html', directory = app.static_folder)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/infer')
def upload_image():
	static_folder = app.static_folder
	gt_files = get_tiff_files(static_folder)
	if not gt_files:
		flash("No files in directory")
		return redirect(request.url)
	else:
		out_l = []
		for gt_fname in gt_files:
			gt_f = gt_fname.parts[-1]
			gt = url_for('static', filename=gt_f)
			outf_name = run_inference(gt)
			out_l.append(outf_name)
		return render_template('inference.html', names=out_l)


if __name__ == "__main__":
	app.debug = True
	port = 5000
	app.run(host="0.0.0.0", debug=True, port=port)