# imports
# to activate virtual environment in windows & f:/allora/venv/Scripts/Activate.ps1
import os
import img2pdf
import tempfile
from os import name
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import magic
from werkzeug.utils import secure_filename
import boxDetection

app = Flask(__name__)


ALLOWED_EXTENSIONS = {'pdf', 'txt'}
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/tmp/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST' and 'file-2' in request.files:
        file = request.files['file-2']
        print("Upload font file: ",file.filename)
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)

        global isTempfontuploaded
        isTempfontuploaded=True
        filename = file.filename
        fn=filename.rsplit('.', 1)[0].lower()+' FONT SELECTED'
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file.save(os.path.join(tempfile.gettempdir(), filename))
        boxDetection.box_activator(os.path.join(tempfile.gettempdir(), filename))
        return render_template("index.html",test=fn) 

    if request.method == 'POST' and 'file' in request.files:     
        file = request.files['file']
        print(file.filename)
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(tempfile.gettempdir(), filename))
            activator(os.path.join(tempfile.gettempdir(), filename),
                      filename.rsplit('.', 1)[1].lower())
            #activator(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename.rsplit('.', 1)[1].lower())
            createPDF()
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template("index.html",test="Default font")

isTempfontuploaded=False


@app.route('/'+str(tempfile.gettempdir())+'<filename>')
def uploaded_file(filename):
    return send_from_directory(tempfile.gettempdir(), "output.pdf", as_attachment=True)


def createPDF():
    path = os.path.join(tempfile.gettempdir(), "output.pdf")
    #path = str(tempfile.gettempdir())+"\output.pdf"
    #oPath = str(tempfile.gettempdir())
    # lit="\\"
    #oPath = "".join([oPath,lit])
    #path = os.path.join(tempfile.gettempdir(), "output.pdf")
    # with open("tmp/output.pdf", "wb") as f:
    # with open(path, "wb") as f:
    # f.write(img2pdf.convert(
    # [i for i in os.listdir(str(tempfile.gettempdir())) if i.endswith(".png")]))

    dirname = str(tempfile.gettempdir())
    imgs = []
    for fname in os.listdir(dirname):
        if not fname.endswith(".png"):
            continue
        pat = os.path.join(dirname, fname)
        if os.path.isdir(pat):
            continue
        imgs.append(pat)
    with open(path, "wb") as f:
        f.write(img2pdf.convert(imgs))

    # deleting png files created
    for f in imgs:
        os.remove(os.path.join("", f))

    # deleting png files created
    # filelist = [f for f in os.listdir(
    # str(tempfile.gettempdir())+"\\") if f.endswith(".png")]
    # for f in filelist:
    #os.remove(os.path.join(tempfile.gettempdir(), f))


def activator(filePath, extension):
    magic.magicWand(filePath, extension,isTempfontuploaded)
    # os.remove(filePath)


if __name__ == "__main__":
    app.run(debug=True)
    #val = input("Enter file with extension:  ")
    #activator(val, val.rsplit('.', 1)[1].lower())
