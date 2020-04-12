import os
from flask import Flask, flash, request, redirect, url_for, render_template
from config import Config
from forms import TextForm, LoginForm
from werkzeug.utils import secure_filename

APP_ROUTE = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = '/texts'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config.from_object(Config)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/',     methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        source = request.form['text']
        result = source.upper()
        return render_template('bodyleft.html', source=source, result=result)
    else:
        return render_template('bodyleft.html')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/price')
def price():
    return render_template('price.html', title='Prices')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register')
def register():
    return render_template('about.html', title='Register')


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


if __name__ == "__main__":
    app.debug = True
    app.run()
