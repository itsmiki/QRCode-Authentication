import base64
from codecs import EncodedFile
from email import header
import json
import uuid
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

from database import db_getPublicKey

from authlib.jose import jwt



def getJWTHeaders(JWT):
    headersEncoded = JWT.decode('utf-8').split('.')[0]
    return json.loads(base64.b64decode(headersEncoded + "="*divmod(len(headersEncoded),4)[1]).decode('utf-8'))


def createQRCodeData_base64(action):
    qr_content = {}
    qr_content['action'] = action
    qr_content['token'] = str(uuid.uuid4())
    qr = json.dumps(qr_content)
    encoded = base64.b64encode(str(qr).encode('utf-8')).decode('utf-8')
    return encoded

def createQRCodeData_dict(action):
    qr_content = {}
    qr_content['action'] = action
    qr_content['token'] = str(uuid.uuid4())
    return qr_content

def verify(data, publicKey, signature):
    verifier = PKCS1_v1_5.new(RSA.importKey(publicKey))
    hasher = SHA256.new(bytes(data, encoding='utf-8'))
    decrypted = verifier.verify(hasher, signature)
    print(decrypted)

    return decrypted

def test_createJWT(message, accountId):
    with open('user1.prv', 'rb') as fh:
        signing_key = fh.read()

    jwt_token = jwt.encode({"kid": accountId, "alg": "RS256"}, message, signing_key, check=False)

    return jwt_token

def verifyJWT(encodedJWT):
    headers = getJWTHeaders(encodedJWT)
    print(headers)
    publicKey = db_getPublicKey(headers['kid'])
    try:
        print(jwt.decode(encodedJWT, publicKey))
        return True
    except:
        return False

def createJWT(token, action):
    with open('server.prv', 'rb') as fh:
        signing_key = fh.read()

    jwt_token = jwt.encode({"kid": "AuthServer", "alg": "RS256"}, {"action": action, "token": token} , signing_key, check=False)

    return jwt_token

def createJWTAuth(token, isAuthorized):
    with open('server.prv', 'rb') as fh:
        signing_key = fh.read()

    jwt_token = jwt.encode({"kid": "AuthServer", "alg": "RS256"}, {"action": "authorization", "token": token, "isAuthorized": isAuthorized} , signing_key, check=False)

    return jwt_token

if __name__ == "__main__":
    # print(createQRCodeData("login"))
    # verify('test', db_getPublicKey("test name"), b'\x1d\xa6\xbef\xac\xeb\xafK\xa0\x99J\x98\x1a\x10n\x7f>\x1e\xa1\x8cD8$\xa8\xa2\x18\xb1{\xaa\xb19\x05\x94\xc2\x13\xb8(\x13\xe3\xaa\x1cW?\x02\xb4_Vp\xb4Q\x80VI\xea\xee\xb7,* \xd62\x9a\xf1\xfe\xd7\xba\x14\x97\xdb\xd9\xa0\'\xd1q\x0e\x94\xb8\x80DR\x0b\x8a\xc2\xc9\x0e\xfdd\xeau\xe3TL\x90\x82\xf1.\xf9\xeb\x87\xd4\xbf"QpMJ\x83.6\xe2\x10\xc1\xcd\xcf\xaf\xde\r/\x07\xc3\x07%D\x04\xcd\x13\x00\xe1\xb1\xbe"5\xd5ez\x80\x95\xfd\xa6\xe9\xca\xd3\x8cS>\x8cp\x08\xf9*\xc3$N\xbcH\xe7\xd0gOR\x1f\xffW\xb4-7\x13\x0c\xc3\xb8kK\xa2\xbca\xc8I\xbd8Ba\x8f\x8au\xb0j\xcct\x9d\x9b\xee\xfa\xf2\x1c\xd1\xc8\xa6\x91\x85\xb41/\xbbY2{Z\x9ef\x05\xc6\x93\xe3\xf5\x9a]\xd8\x9b\xa7#@@gvH\xf66\x7fCT\x98\xd1\x9e9\xe3@CjQ`\xe1\x8dh\xfbbLx\xedPJ\x88\x84\xfb|>4')
    # print(test_createJWT(createQRCodeData_dict("login"), "438822fc-8b82-429c-baf7-d38a9fc4e974"))
    # print(verifyJWT(test_createJWT(createQRCodeData_dict("login"), 'test')))
    # print(createJWT(str(uuid.uuid4()), "login").decode('utf-8'))
    pass