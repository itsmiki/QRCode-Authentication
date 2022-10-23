import base64
import sqlite3
import time
import uuid

def db_checkWebApp(webAppId):
    con=sqlite3.connect("server.db")
    cur = con.cursor()
    try:
        res = cur.execute("SELECT appName FROM WebApplications WHERE appId = ?", (webAppId, ))
        appName = res.fetchone()
        if appName is None:
            con.close()
            return False
        con.close()
        return True
    except sqlite3.Error as error:
        return error

def db_checkAccount(accountId):
    con=sqlite3.connect("server.db")
    cur = con.cursor()
    try:
        res = cur.execute("SELECT accountId FROM Accounts WHERE accountId = ?", (accountId, ))
        accountId = res.fetchone()
        if accountId is None:
            con.close()
            return False
        con.close()
        return True
    except sqlite3.Error as error:
        return error

def db_checkAccountMatchesWebApp(accountId, webAppId):
    con=sqlite3.connect("server.db")
    cur = con.cursor()
    try:
        res = cur.execute("SELECT accountId FROM Accounts WHERE accountId = ? AND webAppId = ?", (accountId, webAppId))
        accountId = res.fetchone()
        if accountId is None:
            con.close()
            return False
        con.close()
        return True
    except sqlite3.Error as error:
        return error

def db_registerWebApp(webAppId, appName):
    con=sqlite3.connect("server.db")
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO WebApplications(appId, appName) values(?, ?)", (webAppId, appName))
        con.commit()
    except sqlite3.Error as error:
        return error
    con.close()
    return True

def db_registerMobileAppId(appId, timeCreated, timeAlive):
    con=sqlite3.connect("server.db")
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO MobileApplicationsTemp(appId, timeCreated, timeAlive) values(?, ?, ?)", (appId, timeCreated, timeAlive))
        con.commit()
    except sqlite3.Error as error:
        return error
    con.close()
    return True

def db_deleteMobileAppId(appId):
    con=sqlite3.connect("server.db")
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM MobileApplicationsTemp WHERE appId = ?", (appId, ))
        con.commit()
    except sqlite3.Error as error:
        return error
    con.close()
    return True

def db_registerMobileApp(mobileAppId, publicKey):
    con=sqlite3.connect("server.db")
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO MobileApplications(appId, publicKey) values(?, ?)", (mobileAppId, publicKey))
        con.commit()
    except sqlite3.Error as error:
        return error
    con.close()
    return True

def db_registerAccount(accountId, webAppId, mobileAppId):
    con=sqlite3.connect("server.db")
    con.execute("PRAGMA foreign_keys = 1")
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO Accounts(accountId, webAppId, mobileAppId) values(?, ?, ?)", (accountId, webAppId, mobileAppId))
        con.commit()
    except sqlite3.Error as error:
        return error
    con.close()
    return True

def db_createRegisterToken(webAppId, accountId, token, timeCreated, TimeAlive):
    con=sqlite3.connect("server.db")
    con.execute("PRAGMA foreign_keys = 1")
    cur = con.cursor()
    if db_checkAccount(accountId) == False:
        try:
            cur.execute("INSERT INTO RegisterTokens(webAppId, accountId, token, timeCreated, TimeAlive) values(?, ?, ?, ?, ?)", (webAppId, accountId, token, timeCreated, TimeAlive))
            con.commit()
            con.close()
            return True
        except sqlite3.Error as error:
            con.close()
            return error
    con.close()
    return False


def db_createLoginToken(webAppId, token, timeCreated, timeAlive):
    con=sqlite3.connect("server.db")
    con.execute("PRAGMA foreign_keys = 1")
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO LoginTokens(webAppId, token, timeCreated, timeAlive, authorized) values(?, ?, ?, ?, ?)", (webAppId, token, timeCreated, timeAlive, 0))
        con.commit()
    except sqlite3.Error as error:
        con.close()
        return error
    con.close()
    return True

def db_getPublicKey(mobileAppId):
    con=sqlite3.connect("server.db")
    cur = con.cursor()
    try:
        res = cur.execute("SELECT publicKey FROM MobileApplications WHERE appId = ?", (mobileAppId, ))
        publicKey = res.fetchone()
        if publicKey is None:
            con.close()
            return None
        con.close()
        return (base64.b64decode(publicKey[0]))
    except sqlite3.Error as error:
        return error

def db_checkLoginTokenAuthorization(token):
    con=sqlite3.connect("server.db")
    cur = con.cursor()
    try:
        res = cur.execute("SELECT authorized FROM LoginTokens WHERE token = ?", (token, ))
        isAuthorized = res.fetchone()
        if isAuthorized is None:
            con.close()
            return None
        con.close()
        if isAuthorized[0] == 1:
            return True
        elif isAuthorized[0] == 0:
            return False
    except sqlite3.Error as error:
        return error



if __name__ == "__main__":
    #print(db_registerMobileApp(str(uuid.uuid4()), "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklUQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FRNEFNSUlCQ1FLQ0FRQjhYeFVaekI3cnd4clpaaVJpVDNuegpxZldtc0Q3ZnFEUlg2VW15am1GalBSUytJK0lickhxQ1hlVTFvMXVxbTV0VHM5WkVaVGRRYTM1a2JVNG1ZSGg1ClBvTXZVKzdMRFAwbTFlZVpRSEJaMzR4c0JDK1RSZ05iTUlvMDRuOUN2UmpnMXNaTHE4b05vMkRuVlk2QUhMdksKZGNOdHQrUlVlZE1LZCtuL1JsUXkvTWVaMmlVUzR1ODRuako4aWVpUHlwNC92c29hSWhvNHhJcDVDQzg4YVM5cwpBa2VqYUVOK3FyMzNhZlZoZWFud2wyUDg0UndPUDQ2dllmSW1QeXFkV1NkSWdWQTBEWlpiNFErbEg1RGIvVmpZCmVoMVk0c1BYM29OU2FDMjJ3UldKR3o0U0REMkEvSDg4WWdJbEo3aHBreFpaVHhlNlcwR3pJdkFhU0xLSUxvajUKQWdNQkFBRT0KLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0t"))
    # print(db_registerAccount(str(uuid.uuid4()), "b2fd0695-47f4-4aa8-aa46-04f3a0218493", "f85b2235-9e87-4520-8af2-ed767fa08d15"))
    #print(db_registerWebApp(str(uuid.uuid4()), "Test Web Application"))
    # print(db_createLoginToken("b2fd0695-47f4-4aa8-aa46-04f3a0218493", str(uuid.uuid4()), 123, 120))
    # print(db_createRegisterToken('b2fd0695-47f4-4aa8-aa46-04f3a0218493', 'bc8fbb41-ba21-457d-b7e6-a83774ba8590', "wewe-f3refss9a", 123, 120))
    # id = str(uuid.uuid4())
    # print(db_registerMobileAppId(str(id), 123, 123))
    # time.sleep(10)
    # print(db_deleteMobileAppId(str(id)))
    # print(db_getPublicKey("test"))
    # print(db_checkWebApp("123"))
    # print(db_checkLoginTokenAuthorization("d0c02877-dd9b-46e6-85de-9f40933ca659"))
    pass