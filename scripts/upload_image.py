from flask import Flask, render_template
import os.path

fdir=os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.abspath(os.path.join(fdir, '..', 'templates'))
app = Flask(__name__, template_folder=template_dir)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)