import base64
import json
import uuid

from authlib.jose import jwt

from ._database import db_getPublicKey, db_getWebAppIdAccountIdFromRegisterToken, db_getWebAppName, db_getWebAppIdAccountIdFromLoginToken



def getJWTHeaders(JWT):
    headersEncoded = JWT.decode('utf-8').split('.')[0]
    return json.loads(base64.b64decode(headersEncoded + "="*divmod(len(headersEncoded),4)[1]).decode('utf-8'))

def getJWTPayload(JWT):
    payloadEncoded = JWT.decode('utf-8').split('.')[1]
    return json.loads(base64.b64decode(payloadEncoded + "="*divmod(len(payloadEncoded),4)[1]).decode('utf-8'))

def test_createJWT(message, accountId):
    with open('keys/user2_prv.pem', 'rb') as fh:
        signing_key = fh.read()

    jwt_token = jwt.encode({"kid": accountId, "alg": "RS256"}, message, signing_key, check=False)

    return jwt_token

def verifyJWT(encodedJWT):
    headers = getJWTHeaders(encodedJWT)
    publicKey = db_getPublicKey(headers['kid'])
    try:
<<<<<<< HEAD
        # print(jwt.decode(encodedJWT, publicKey))
=======
        print(jwt.decode(encodedJWT, publicKey))
>>>>>>> f8d9003ba51d56533a3c250193e39f33046bff64
        return True
    except:
        return False

def createJWT(token, action):
    with open('keys/server_prv.pem', 'rb') as fh:
        signing_key = fh.read()
    if action == "login":
        webAppId = db_getWebAppIdAccountIdFromLoginToken(token)
        name = db_getWebAppName(webAppId)
        jwt_token = jwt.encode({"kid": "AuthServer", "alg": "RS256"}, {"action": action, "token": token, "name": name} , signing_key, check=False)
    elif action == "register":
        webAppId = db_getWebAppIdAccountIdFromRegisterToken(token)[0]
        name = db_getWebAppName(webAppId)
        jwt_token = jwt.encode({"kid": "AuthServer", "alg": "RS256"}, {"action": action, "token": token, "name": name} , signing_key, check=False)

    return jwt_token

def createJWTAuth(token, accountId, isAuthorized):
    with open('keys/server_prv.pem', 'rb') as fh:
        signing_key = fh.read()

    jwt_token = jwt.encode({"kid": "AuthServer", "alg": "RS256"}, {"action": "authorization", "token": token, "accountId": accountId, "isAuthorized": isAuthorized} , signing_key, check=False)

    return jwt_token

def verifyconnectionJWT(encodedJWT):
    headers = getJWTHeaders(encodedJWT)
    publicKey = db_getPublicKey(headers['kid'])
    try:
<<<<<<< HEAD
        # print(jwt.decode(encodedJWT, publicKey))
=======
        print(jwt.decode(encodedJWT, publicKey))
>>>>>>> f8d9003ba51d56533a3c250193e39f33046bff64
        return True
    except:
        return False

if __name__ == "__main__":
    print(verifyJWT('eyJhbGciOiJSUzI1NiIsInR5cGUiOiJKV1QiLCJraWQiOiI1MjM4MmJlYy1jMjQyLTQ3MTktYjIzYi1iYzAxMzUxMTgzNzkifQ.eyJhY3Rpb24iOiJyZWdpc3RlciIsInRva2VuIjoiNTJhZmM2YmEtMDdhYS00NzA2LWI5YWMtMDY2YjkxMzZlNjg4In0.TpBGO0EUdQvGhkoyVPDN5Nq0EPfxxzSBIDPb+scBPJIp32Ojwg8Ba2YQ+Lp5/gVL98WCQ9GEp1OusBOTF3kCh4UcHFxIhm3/TxfUGMtDNy2b7c6RT+sKhQL25CKfjfkVzs1VzAod+tsm6EvT04pF/pFZW3XXpYrsBk9DozRvT0E'.encode('utf-8')))
    # print(createQRCodeData_dict("register"))
    # verify('test', db_getPublicKey("test name"), b'\x1d\xa6\xbef\xac\xeb\xafK\xa0\x99J\x98\x1a\x10n\x7f>\x1e\xa1\x8cD8$\xa8\xa2\x18\xb1{\xaa\xb19\x05\x94\xc2\x13\xb8(\x13\xe3\xaa\x1cW?\x02\xb4_Vp\xb4Q\x80VI\xea\xee\xb7,* \xd62\x9a\xf1\xfe\xd7\xba\x14\x97\xdb\xd9\xa0\'\xd1q\x0e\x94\xb8\x80DR\x0b\x8a\xc2\xc9\x0e\xfdd\xeau\xe3TL\x90\x82\xf1.\xf9\xeb\x87\xd4\xbf"QpMJ\x83.6\xe2\x10\xc1\xcd\xcf\xaf\xde\r/\x07\xc3\x07%D\x04\xcd\x13\x00\xe1\xb1\xbe"5\xd5ez\x80\x95\xfd\xa6\xe9\xca\xd3\x8cS>\x8cp\x08\xf9*\xc3$N\xbcH\xe7\xd0gOR\x1f\xffW\xb4-7\x13\x0c\xc3\xb8kK\xa2\xbca\xc8I\xbd8Ba\x8f\x8au\xb0j\xcct\x9d\x9b\xee\xfa\xf2\x1c\xd1\xc8\xa6\x91\x85\xb41/\xbbY2{Z\x9ef\x05\xc6\x93\xe3\xf5\x9a]\xd8\x9b\xa7#@@gvH\xf66\x7fCT\x98\xd1\x9e9\xe3@CjQ`\xe1\x8dh\xfbbLx\xedPJ\x88\x84\xfb|>4')
    # print(test_createJWT({'action': 'register', 'token': '6697f022-84c0-4c72-9c18-4a7dd398ca19'}, "911aa442-d6b4-453e-973f-89af4a20f752"))
    # print(verifyJWT(test_createJWT(createQRCodeData_dict("login"), 'test')))
    # print(verifyJWT("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjkxMWFhNDQyLWQ2YjQtNDUzZS05NzNmLTg5YWY0YTIwZjc1MiJ9.eyJhY3Rpb24iOiJyZWdpc3RlciIsInRva2VuIjoiNjY5N2YwMjItODRjMC00YzcyLTljMTgtNGE3ZGQzOThjYTE5In0.LNZ9GmYfSf7mFipk5mkBnTtzLCvWLhe3nLfvfCIm5gOiMo7BN8qlP102iKHwe0mxp5OlMZCPgKcVy5klkl0z+iUvSC2hUAzbTxOb8LXL8OAUBFbnzyPc44ppWJ14rY5qulR9hI1piln92MCe2+DWPXplzw0kFIFLG9gjcnilQ7EHLqBRrUra051+gNLxBwZtwsy2KRXb5wJI2/zi/aTh/a3VciwvqE7eEZK4Z/bq3+QtAudknrkT33AzjGChDLM+pXdYd/lZYSAeZ1KaIH10wsZeuIs9I7gq0PrfbuljJrSB8wZNEgtYLNwvDJ+V/3/VHhV3c6eSXKlT6sMY01rsIw".encode('utf-8')))
    # print(createJWT(str(uuid.uuid4()), "login").decode('utf-8'))
    pass