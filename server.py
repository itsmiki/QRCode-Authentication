import uuid
from flask import Flask, jsonify
from flask import request
from flask_cors import CORS
from threading import Timer
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from database import *
import json
import time
from flask_api import status

from qr_code import createJWT, createJWTAuth, verifyJWT

app = Flask(__name__)
CORS(app)

ACTIVE_CODES = {}
with open("config.json") as file: 
    config = json.load(file)


@app.route("/v1/connect/get/mobile-id", methods= ['GET'])
def giveMobileId():
    id = uuid.uuid4()
    try:
        if db_registerMobileAppId(str(id), int(time.time()), config["mobileAppTemp"]["timeAlive"]) is False:
            return "INTERNAL SERVER ERROR", status.HTTP_500_INTERNAL_SERVER_ERROR
    except:
        return "INTERNAL_SERVER_ERROR", status.HTTP_500_INTERNAL_SERVER_ERROR

    return str(id) , status.HTTP_200_OK


@app.route("/v1/login/get/qr/application-id/<appId>", methods = ['GET'])
def giveLoginQr(appId):
    if db_checkWebApp(appId) == False:
        return "UNAUTHORIZED", status.HTTP_401_UNAUTHORIZED
    else:
        token = str(uuid.uuid4())
        if db_createLoginToken(appId, token, int(time.time()), config["loginToken"]["timeAlive"]) is True:
            JWTToken = createJWT(token, "login")
            return JWTToken, status.HTTP_200_OK
        else:
            return "INTERNAL_SERVER_ERROR", status.HTTP_500_INTERNAL_SERVER_ERROR


@app.route("/v1/register/get/qr/application-id/<appId>/account-id/<accountId>", methods = ['GET'])
def giveRegisterQr(appId, accountId):
    if db_checkWebApp(appId) is True and db_checkAccount(accountId) is False:
        token = str(uuid.uuid4())
        if db_createRegisterToken(appId, accountId, token, int(time.time()), config["loginToken"]["timeAlive"]) is True:
            JWTToken = createJWT(token, "register")
            return JWTToken, status.HTTP_200_OK
        else:
            return "INTERNAL_SERVER_ERROR", status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        return "UNAUTHORIZED", status.HTTP_401_UNAUTHORIZED

@app.route("/v1/login/get/is-authorized/token/<token>", methods = ['GET'])
def giveAuthorizationStatus(token):
    auth = db_checkLoginTokenAuthorization(token)
    if auth is True:
        return createJWTAuth(token, True), status.HTTP_200_OK
    elif auth is False:
        return createJWTAuth(token, False), status.HTTP_200_OK
    else:
        return "TOKEN DOES NOT EXIST", status.HTTP_500_INTERNAL_SERVER_ERROR


@app.route("/v1/login/get/authorize", methods = ['GET']) # DOPISAĆ AKTUALIZACJE BAZY
def authorizeLoginToken():
    # request.headers.get('Authorization')
    authorization = "eyJraWQiOiI0Mzg4MjJmYy04YjgyLTQyOWMtYmFmNy1kMzhhOWZjNGU5NzQiLCJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY3Rpb24iOiJsb2dpbiIsInRva2VuIjoiZTA2YjdiMWItZDdmNS00MmIxLTkyYTgtODVjOTY1YTViYzA0In0.PLtkFKslWzWjsEdlX6LBhDwloLQHr8q5lFc7PMHqpNlTO3CYduukKMHHqoxgigwWmICmFG1jo_n6zLn0iQ3_2I0FNzYu5PKeHVsdSt_0AcgY6yTaL_g3MvGXj3675f9mnQvJhFZneGUbay3tbCUu2zxsAIZ5AjJ3UI18T9TZwxDo6LPP6hNfLQYADrHgV8_ERCc2-b4bRq0dESLGcTlbYKfFQlkfC4LXe3k4HPJhhsT_v1FSM0lGI4r0n1boZ9X70dmKM93-ivr7j_YQ6075losWQZfpKkVqtUSyqyqzXy43SfqteNisQ09UpuMDUI7AzBoWcPBM5NJ91171c216gw"
    try:
        is_verified = verifyJWT(authorization.encode('utf-8'))
    except:
        return "MALFORMED JWT", status.HTTP_500_INTERNAL_SERVER_ERROR
    
    if is_verified is True:
        return "AUTHENTICATED LOGIN", status.HTTP_200_OK
    else:
        return "UNAUTHORIZED", status.HTTP_401_UNAUTHORIZED


@app.route("/v1/register/get/authorize", methods = ['GET']) # DOPISAĆ AKTUALIZACJE BAZY
def authorizeRegisterToken():
    # request.headers.get('Authorization')
    authorization = "eyJraWQiOiI0Mzg4MjJmYy04YjgyLTQyOWMtYmFmNy1kMzhhOWZjNGU5NzQiLCJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY3Rpb24iOiJsb2dpbiIsInRva2VuIjoiZTA2YjdiMWItZDdmNS00MmIxLTkyYTgtODVjOTY1YTViYzA0In0.PLtkFKslWzWjsEdlX6LBhDwloLQHr8q5lFc7PMHqpNlTO3CYduukKMHHqoxgigwWmICmFG1jo_n6zLn0iQ3_2I0FNzYu5PKeHVsdSt_0AcgY6yTaL_g3MvGXj3675f9mnQvJhFZneGUbay3tbCUu2zxsAIZ5AjJ3UI18T9TZwxDo6LPP6hNfLQYADrHgV8_ERCc2-b4bRq0dESLGcTlbYKfFQlkfC4LXe3k4HPJhhsT_v1FSM0lGI4r0n1boZ9X70dmKM93-ivr7j_YQ6075losWQZfpKkVqtUSyqyqzXy43SfqteNisQ09UpuMDUI7AzBoWcPBM5NJ91171c216gw"
    try:
        is_verified = verifyJWT(authorization.encode('utf-8'))
    except:
        return "MALFORMED JWT", status.HTTP_500_INTERNAL_SERVER_ERROR
    
    if is_verified is True:
        return "ACCOUNT REGISTERED", status.HTTP_200_OK
    else:
        return "UNAUTHORIZED", status.HTTP_401_UNAUTHORIZED


@app.errorhandler(404)
def page_not_found(error):
    return "NOT FOUND", status.HTTP_404_NOT_FOUND


if __name__ == "__main__":
    app.run(debug=True)