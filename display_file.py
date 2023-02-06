import rasterio
from rasterio.plot import show
from pathlib import Path
import os.path
from csuinf.geotiff_utils import PROCESSED_PREFIX, ALLOWED_EXTENSIONS

if __name__=="__main__":
    fdir = os.path.abspath(os.path.dirname(__file__))
    imgdir = os.path.join(fdir, 'images')
    imgp = Path(imgdir)
    dnn_tiffs = [[x for x in imgp.glob(".".join([PROCESSED_PREFIX+"*",fext]))] for fext in ALLOWED_EXTENSIONS]
    dnn_tiffs = [val for sublist in dnn_tiffs for val in sublist]
    for tif in dnn_tiffs:
        with rasterio.open(tif, 'r') as res:
            img = res.read()
            show(img)