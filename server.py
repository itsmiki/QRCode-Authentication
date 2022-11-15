import uuid
import json
import time

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_api import status

from functions._jwt import createJWT, createJWTAuth, getJWTHeaders, getJWTPayload, verifyJWT
from functions._database import *
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
CORS(app)
# run_with_ngrok(app)

ACTIVE_CODES = {}
with open("config.json") as file: 
    config = json.load(file)


@app.route("/v1/connect/get/mobile-id", methods= ['GET'])
def giveMobileId():
    id = uuid.uuid4()
    print(id)
    try:
        if db_registerMobileAppIdTemp(str(id), int(time.time()), config["mobileAppTemp"]["timeAlive"]) is False:
            return "INTERNAL SERVER ERROR", status.HTTP_500_INTERNAL_SERVER_ERROR
    except:
        return "INTERNAL SERVER ERROR", status.HTTP_500_INTERNAL_SERVER_ERROR

    return jsonify(id) , status.HTTP_200_OK


@app.route("/v1/connect/get/mobile-app/<mobileAppId>/key/<key>", methods= ['GET'])
def connectMobileApp(mobileAppId, key):
    try:
        if db_checkMobileAppIdTemp(mobileAppId):
            db_deleteMobileAppIdTemp(mobileAppId)
            if not db_registerMobileApp(mobileAppId, key):
                return "WRONG PUBLIC KEY", status.HTTP_500_INTERNAL_SERVER_ERROR # włączyć unique key
        else:
            return "WRONG OR EXPIRED MOBILE APP ID", status.HTTP_500_INTERNAL_SERVER_ERROR
    except:
        return "INTERNAL SERVER ERROR", status.HTTP_500_INTERNAL_SERVER_ERROR
    return "OK", status.HTTP_200_OK


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
            existingToken = db_getRegisterToken(accountId, appId)
            if existingToken is not None:
                JWTToken = createJWT(existingToken, "register")
                return JWTToken, status.HTTP_200_OK
            return "INTERNAL SERVER ERROR", status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        return "UNAUTHORIZED", status.HTTP_401_UNAUTHORIZED

@app.route("/v1/login/get/is-authorized/token/<token>", methods = ['GET'])
def giveAuthorizationStatus(token):
    db_deleteExpiredLoginTokens()
    auth = db_checkLoginTokenAuthorization(token)
    if auth is True:
        accountId = db_getAccountIdFromLoginToken(token)
        return createJWTAuth(token, accountId, True), status.HTTP_200_OK
    elif auth is False:
        return createJWTAuth(token, None, False), status.HTTP_200_OK
    else:
        return "TOKEN DOES NOT EXIST", status.HTTP_500_INTERNAL_SERVER_ERROR


@app.route("/v1/login/get/authorize", methods = ['GET'])
def authorizeLoginToken():
    db_deleteExpiredLoginTokens()
    authorization = request.headers.get('Authorization')
    try:
        is_verified = verifyJWT(authorization.encode('utf-8'))
    except:
        return "MALFORMED JWT", status.HTTP_500_INTERNAL_SERVER_ERROR
    
    if is_verified is True:
        token = getJWTPayload(authorization.encode('utf-8'))['token']
        mobileAppId = getJWTHeaders(authorization.encode('utf-8'))['kid']
        if db_checkLoginToken(token):
            db_associateAccountWithLoginToken(mobileAppId, token)
            db_authorizeLoginToken(token)
            return "AUTHENTICATED LOGIN", status.HTTP_200_OK
        return "TOKEN EXPIRED DOES NOT EXIST", status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        return "UNAUTHORIZED", status.HTTP_401_UNAUTHORIZED


@app.route("/v1/register/get/authorize", methods = ['GET'])
def authorizeRegisterToken():
    db_deleteExpiredRegisterTokens()
    authorization = request.headers.get('Authorization')
    try:
        is_verified = verifyJWT(authorization.encode('utf-8'))
    except:
        return "MALFORMED JWT", status.HTTP_500_INTERNAL_SERVER_ERROR
    
    if is_verified is True:
        token = getJWTPayload(authorization.encode('utf-8'))['token']
        mobileAppId = getJWTHeaders(authorization.encode('utf-8'))['kid']
        try:
            webAppId, accountId = db_getWebAppIdAccountIdFromRegisterToken(token)
            db_registerAccount(accountId, webAppId, mobileAppId)
            db_deleteRegisterToken(token)
            return "ACCOUNT REGISTERED", status.HTTP_200_OK
        except:
            return "TOKEN EXPIRED OR DOES NOT EXIST", status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        return "UNAUTHORIZED", status.HTTP_401_UNAUTHORIZED


@app.errorhandler(404)
def page_not_found(error):
    return "NOT FOUND", status.HTTP_404_NOT_FOUND


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
    # app.run()