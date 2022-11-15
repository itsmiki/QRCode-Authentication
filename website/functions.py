import base64
import json
import uuid

from authlib.jose import jwt

# from _database import db_getPublicKey



def getJWTHeaders(JWT):
    headersEncoded = JWT.decode('utf-8').split('.')[0]
    return json.loads(base64.b64decode(headersEncoded + "="*divmod(len(headersEncoded),4)[1]).decode('utf-8'))

def getJWTPayload(JWT):
    payloadEncoded = JWT.decode('utf-8').split('.')[1]
    return json.loads(base64.b64decode(payloadEncoded + "="*divmod(len(payloadEncoded),4)[1]).decode('utf-8'))

# def verifyJWT(encodedJWT):
#     headers = getJWTHeaders(encodedJWT)
#     publicKey = db_getPublicKey(headers['kid'])
#     try:
#         print(jwt.decode(encodedJWT, publicKey))
#         return True
#     except:
#         return False