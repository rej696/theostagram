import os
import urllib.request

from flask import Flask, render_template, url_for, flash, request, redirect
from werkzeug.utils import secure_filename
app = Flask(__name__)

# setup image uploads ------------------------------------------------
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# get static web page urls ------------------------------------------
def get_urls(*args):
    output = {}
    for arg in args:
        if arg == "style":
             output[arg] = url_for('static', filename='style.css')
    return output

# -------------------------------------------------------------------
@app.route("/")
def home():
    url_kwargs = get_urls("style")
    return render_template('home.html', **url_kwargs)

# Theostagram -------------------------------------------------------
@app.route("/theostagram/")
def theostagram_home():
    url_kwargs = get_urls("style")
    return render_template('theostagram-home.html', **url_kwargs)

@app.route("/theostagram/upload/")
def theostagram_upload_form():
    url_kwargs = get_urls("style")
    return render_template('theostagram-upload.html', **url_kwargs)

@app.route("/theostagram/upload/", methods=['POST'])
def theostagram_upload_image():
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
        # print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed')
        url_kwargs = get_urls("style")
        return render_template('theostagram-upload.html', filename=filename, **url_kwargs)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route("/theostagram/upload/display/<filename>/")
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for("static", filename="uploads/" + filename), code=301)

# -------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0")
