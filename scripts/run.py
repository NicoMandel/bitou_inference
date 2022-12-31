from flask import Flask, render_template
import os.path

template_dir = os.path.abspath('../templates')
app = Flask(__name__)

@app.route('/')
def hello():
	return "Hello World!"

@app.route('/home')
def render_home():
    return render_template('home.html')

if __name__ == '__main__':
    port = 5000
    app.run(host='0.0.0.0', port=port)