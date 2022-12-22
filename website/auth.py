from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User, LoginTokens
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, webAppId, authServerAddress
from .functions import getJWTPayload
from flask_login import login_user, login_required, logout_user, current_user
import uuid
import requests
from flask_qrcode import QRcode

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/login-with-qr', methods=['GET', 'POST'])
def loginWithQR():
    if request.method == 'GET':
        session['session'] = str(uuid.uuid4())
        res = requests.get("http://{}/v1/login/get/qr/application-id/{}".format(authServerAddress, webAppId))
        if res.status_code == 200:
            new_user = LoginTokens(session=session['session'], loginToken_jwt=res.text)
            db.session.add(new_user)
            db.session.commit()
            # print(res.text)
            qrcode = QRcode.qrcode(res.text, box_size=5)
            return render_template("login_with_qr.html", user=current_user, qrcode=qrcode)
        else:
            flash(res.text, category='error')
            return render_template("login_with_qr.html", user=current_user)

    if request.method == 'POST':
        record = LoginTokens.query.filter_by(session=session['session']).first()
        try:
            loginToken = getJWTPayload(record.loginToken_jwt.encode('utf-8'))['token']
        except:
            loginToken = "error"

        res = requests.get("http://{}/v1/login/get/is-authorized/token/{}".format(authServerAddress, loginToken))
        response_decoded = getJWTPayload(res.text.encode('utf-8'))

        if response_decoded['isAuthorized'] is True:
            user = User.query.filter_by(accountId=response_decoded["accountId"]).first()
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
<<<<<<< HEAD
            flash('Token not authorized!', category='error')
=======
            flash(response_decoded, category='error')
>>>>>>> f8d9003ba51d56533a3c250193e39f33046bff64
            qrcode = QRcode.qrcode(record.loginToken_jwt, box_size=5)
            return render_template("login_with_qr.html", user=current_user, qrcode=qrcode)

    


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', category='error')
        elif len(username) < 4:
            flash('email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 1:
            flash('Password must be at least 1 characters.', category='error')
        else:
            new_user = User(accountId=str(uuid.uuid4()), username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
