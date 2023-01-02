from flask import Flask, render_template
import os.path

fdir=os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.abspath(os.path.join(fdir, '..', 'templates'))
app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def hello():
	return "Hello World!"

@app.route('/home')
def render_home():
    return render_template('home.html')

@app.route('/index')
def render_index():
    return 'Hello World'

if __name__ == '__main__':
    port = 5000
    app.run(host='0.0.0.0', port=port)