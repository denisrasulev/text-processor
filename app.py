import os

from flask import Flask, flash, redirect, render_template, request, url_for

from config import Config
from forms import ContactForm, LoginForm

APP_ROUTE = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = '/texts'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config.from_object(Config)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['get', 'post'])
@app.route('/home', methods=['get', 'post'])
def index():
    if request.method == "post":
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


@app.route('/login', methods=['get', 'post'])
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


@app.route('/contact', methods=['get', 'post'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        mail = form.mail.data
        gdpr = form.gdpr.data
        mark = form.mark.data
        flash('Contact saved for user {}, with mail {}; GDPR={}, Marketing={}. Thank you '
              'for registering!'.format(name, mail, gdpr, mark))
        # TODO: save data to database
        return redirect(url_for('index'))
    return render_template('contact.html', form=form, title='Contact')


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", title='Page Not Found')


if __name__ == "__main__":
    app.debug = True
    app.run()
