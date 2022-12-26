# Following [this tutorial](https://pytorch.org/tutorials/intermediate/flask_rest_api_tutorial.html)

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

