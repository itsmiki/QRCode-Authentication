from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import authServerAddress, webAppId
import json
import requests
from flask_qrcode import QRcode

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        res = requests.get("http://{}/v1/register/get/qr/application-id/{}/account-id/{}".format(authServerAddress, webAppId, current_user.accountId))
        if res.status_code == 200:
            qrcode = QRcode.qrcode(res.text, box_size=5)
            # print(res.text)
            return render_template("home.html", user=current_user, qrcode=qrcode, username=current_user.username)
        else:
            flash(res.text, category='error')

    return render_template("home.html", user=current_user, username=current_user.username)