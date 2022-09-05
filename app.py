from flask import Flask, render_template, request, session, flash, redirect, url_for
import urllib
import hashlib
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from classes import Autorisatie

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_WEB_APP_KEY')

@app.route('/')
@app.route('/login')
def home():
    session.clear()
    return render_template('login.html', title="Login pagina", logged_in=False)

@app.route('/login', methods=['POST'])
def login():
    params = urllib.parse.quote_plus(os.environ.get('AutorisatieDatabaseConnection'))
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Autorisatie.Gebruiker).filter(Autorisatie.Gebruiker.Gebruikersnaam.in_([POST_USERNAME]))
    result = query.first()
    if result:
        passwordCheck = checkPassWord(POST_PASSWORD, result.SaltedHash)
        if passwordCheck == True:
            session['logged_in'] = True
        else:
            flash('Invalid Credentials')
    else:
        flash('Invalid Credentials')

    return redirect(url_for('index'))

def checkPassWord(provided_password, stored_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]

    pwdhash = hashlib.sha256(salt.encode('utf-8') + provided_password.encode('utf-8')).hexdigest()
    return pwdhash == stored_password


@app.route('/index')
def index():
    if (logged_in() == True):
        return render_template('index.html', title="Overzicht", logged_in=True)

    return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

def logged_in():
    if (session.get('logged_in')):
        if (session['logged_in'] == True):
            return True

    return False


if __name__ == '__main__':
    app.run()
