import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

APP_ROUTE = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = '/texts'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '53afee03b75e8fb022c88fba922bb22e'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # Max upload size 1MB


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/price')
def price():
    return render_template('price.html', title='Prices')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash('File successfully uploaded')
            return redirect(url_for('uploaded_file', filename=filename))

    return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form method=post enctype=text>
              <input type=file name=file>
              <input type=submit value=Upload>
            </form>
            '''


if __name__ == "__main__":
    app.debug = True
    app.run()
