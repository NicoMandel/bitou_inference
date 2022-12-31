"""
    File to submit images to the flask website run in basic_flask.py
"""

import requests
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(description="File for submitting an image to the webserver.")
    parser.add_argument("-i", "--input", type=str, help="Location of the Image", required=True)
    parser.add_argument("-p", "--port", type=int, help="Port on which to submit the image", default=8000)
    args = parser.parse_args()
    return vars(args)

if __name__=="__main__":
    args = parse_args()
    url = f"http://localhost:{args['port']}/predict"
    f = open(args['input'], 'rb')
    fdict = {"file": f}
    resp = requests.post(url, files=fdict)
    f.close()
    print(resp.json())
        

# resp = requests.post("http://localhost:5000/predict",files={"file": open('<PATH/TO/.jpg/FILE>/cat.jpg','rb')})