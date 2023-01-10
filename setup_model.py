"""
    File to download a model and write it locally into the docker image
"""

from csuinf.model import Model
from csuinf.utils import *
import os.path

if __name__=="__main__":
    fdir = os.path.abspath(os.path.dirname(__file__))
    model_name = "best.pt"
    model_f = os.path.join(fdir, model_name)
    model = Model.load_from_checkpoint(model_f)
    print("Local imports are working. Model file downloaded.")