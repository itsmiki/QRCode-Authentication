import base64
import sqlite3
import time
import uuid

def db_checkWebApp(webAppId):
    con=sqlite3.connect("performance\server.db")
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

def db_getWebAppName(webAppId):
    con=sqlite3.connect("performance\server.db")
    cur = con.cursor()
    try:
        res = cur.execute("SELECT appName FROM WebApplications WHERE appId = ?", (webAppId, ))
        appName = res.fetchone()
        if appName is None:
            con.close()
            return None
        con.close()
        return appName[0]
    except sqlite3.Error as error:
        return error

def db_getWebAppId(webAppName):
    con=sqlite3.connect("performance\server.db")
    cur = con.cursor()
    try:
        res = cur.execute("SELECT appId FROM WebApplications WHERE appName = ?", (webAppName, ))
        appId = res.fetchone()
        if appId is None:
            con.close()
            return None
        con.close()
        return appId[0]
    except sqlite3.Error as error:
        return error

def db_checkAccount(accountId):
    con=sqlite3.connect("performance\server.db")
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

def db_checkMobileAppIdTemp(mobileAppId):
    con=sqlite3.connect("performance\server.db")
    cur = con.cursor()
    try:
        res = cur.execute("SELECT appId FROM MobileApplicationsTemp WHERE appId = ?", (mobileAppId, ))
        accountId = res.fetchone()
        if accountId is None:
            con.close()
            return False
        con.close()
        return True
    except sqlite3.Error as error:
        return error

def db_checkLoginToken(token):
    con=sqlite3.connect("performance\server.db")
    cur = con.cursor()
    try:
        res = cur.execute("SELECT token FROM LoginTokens WHERE token = ?", (token, ))
        accountId = res.fetchone()
        if accountId is None:
            con.close()
            return False
        con.close()
        return True
    except sqlite3.Error as error:
        return error

def db_checkAccountMatchesWebApp(accountId, webAppId):
    con=sqlite3.connect("performance\server.db")
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

def db_checkIfMobileAppHasAccountOnWebApp(mobileAppId, webAppId):
    con=sqlite3.connect("performance\server.db")
    cur = con.cursor()
    try:
        res = cur.execute("SELECT accountId FROM Accounts WHERE mobileAppId = ? AND webAppId = ?", (mobileAppId, webAppId))
        accountId = res.fetchone()
        if accountId is None:
            con.close()
            return False
        con.close()
        return True
    except sqlite3.Error as error:
        return error

def db_getAccount(mobileAppId, webAppId):
    con=sqlite3.connect("performance\server.db")
    cur = con.cursor()
    try:
        res = cur.execute("SELECT accountId FROM Accounts WHERE mobileAppId = ? AND webAppId = ?", (mobileAppId, webAppId))
        accountId = res.fetchone()
        con.close()
        return accountId[0]
    except sqlite3.Error as error:
        return error

def db_getWebAppFromToken(token):
    con=sqlite3.connect("performance\server.db")
    cur = con.cursor()
    try:
        res = cur.execute("SELECT webAppId FROM LoginTokens WHERE token = ?", (token, ))
        webAppId = res.fetchone()
        con.close()
        return webAppId[0]
    except sqlite3.Error as error:
        return error

def db_registerWebApp(webAppId, appName):
    con=sqlite3.connect("performance\server.db")
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO WebApplications(appId, appName) values(?, ?)", (webAppId, appName))
        con.commit()
    except sqlite3.Error as error:
        return error
    con.close()
    return True

def db_registerMobileAppIdTemp(appId, timeCreated, timeAlive):
    con=sqlite3.connect("performance\server.db")
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO MobileApplicationsTemp(appId, timeCreated, timeAlive) values(?, ?, ?)", (appId, timeCreated, timeAlive))
        con.commit()
    except sqlite3.Error as error:
        return error
    con.close()
    return True

def db_deleteMobileAppIdTemp(appId):
    con=sqlite3.connect("performance\server.db")
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM MobileApplicationsTemp WHERE appId = ?", (appId, ))
        con.commit()
    except sqlite3.Error as error:
        return error
    con.close()
    return True

def db_deleteAccount(webAppId, mobileAppId):
    con=sqlite3.connect("performance\server.db")
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM Accounts WHERE webAppId = ? AND mobileAppId = ?", (webAppId, mobileAppId))
        con.commit()
    except sqlite3.Error as error:
        return error
    con.close()
    return True

def db_registerMobileApp(mobileAppId, publicKey):
    con=sqlite3.connect("performance\server.db")
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO MobileApplications(appId, publicKey) values(?, ?)", (mobileAppId, publicKey))
        con.commit()
    except sqlite3.Error as error:
        return error
    con.close()
    return True

def db_registerAccount(accountId, webAppId, mobileAppId):
    con=sqlite3.connect("performance\server.db")
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
    con=sqlite3.connect("performance\server.db")
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
    con=sqlite3.connect("performance\server.db")
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
    con=sqlite3.connect("performance\server.db")
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
    con=sqlite3.connect("performance\server.db")
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

def db_authorizeLoginToken(token):
    con=sqlite3.connect("performance\server.db")
    cur = con.cursor()
    try:
        cur.execute("UPDATE LoginTokens SET authorized = ? WHERE token = ?", (1, token))
        con.commit()
    except sqlite3.Error as error:
        print(error)
        return error
    con.close()
    return True

def db_associateAccountWithLoginToken(mobileAppId, token):
    webAppId = db_getWebAppFromToken(token)
    accountId = db_getAccount(mobileAppId, webAppId)

    con=sqlite3.connect("performance\server.db")
    cur = con.cursor()
    try:
        cur.execute("UPDATE LoginTokens SET accountId = ? WHERE token = ?", (accountId, token))
        con.commit()
    except sqlite3.Error as error:
        print(error)
        return error
    con.close()
    return True

def db_getAccountIdFromLoginToken(token):
    con=sqlite3.connect("performance\server.db")
    cur = con.cursor()
    try:
        res = cur.execute("SELECT accountId FROM LoginTokens WHERE token = ?", (token, ))
        accountId = res.fetchone()
        con.close()
        return accountId[0]
    except sqlite3.Error as error:
        return error

def db_getWebAppIdAccountIdFromRegisterToken(token):
    con=sqlite3.connect("performance\server.db")
    cur = con.cursor()
    try:
        res = cur.execute("SELECT webAppId, accountId FROM RegisterTokens WHERE token = ?", (token, ))
        data = res.fetchone()
        con.close()
        if data is None:
            con.close()
            return None
        return data[0], data[1]
    except sqlite3.Error as error:
        return error

def db_getWebAppIdAccountIdFromLoginToken(token):
    con=sqlite3.connect("performance\server.db")
    cur = con.cursor()
    try:
        res = cur.execute("SELECT webAppId FROM LoginTokens WHERE token = ?", (token, ))
        data = res.fetchone()
        con.close()
        if data is None:
            con.close()
            return None
        return data[0]
    except sqlite3.Error as error:
        return error

def db_deleteRegisterToken(token):
    con=sqlite3.connect("performance\server.db")
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM RegisterTokens WHERE token = ?", (token, ))
        con.commit()
    except sqlite3.Error as error:
        return error
    con.close()
    return True

def db_getRegisterToken(accountId, webAppId):
    con=sqlite3.connect("performance\server.db")
    cur = con.cursor()
    try:
        res = cur.execute("SELECT token FROM RegisterTokens WHERE accountId = ? AND webAppId = ?", (accountId, webAppId))
        token = res.fetchone()
        con.close()
        if token is None:
            con.close()
            return None
        return token[0]
    except sqlite3.Error as error:
        return error

def db_deleteExpiredRegisterTokens():
    current_time = time.time()
    con=sqlite3.connect("performance\server.db")
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM RegisterTokens WHERE ? - timeCreated >= timeAlive", (current_time, ))
        con.commit()
    except sqlite3.Error as error:
        return error
    con.close()
    return True

def db_deleteExpiredLoginTokens():
    current_time = time.time()
    con=sqlite3.connect("performance\server.db")
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM LoginTokens WHERE ? - timeCreated >= timeAlive", (current_time, ))
        con.commit()
    except sqlite3.Error as error:
        return error
    con.close()
    return True

def fill(con, cur):
    webAppId = "b2fd0695-47f4-4aa8-aa46-04f3a0218493"
    accountId = str(uuid.uuid4())
    mobileAppId = str(uuid.uuid4())
    publicKey = "value"

    cur.execute("INSERT INTO MobileApplications(appId, publicKey) values(?, ?)", (mobileAppId, publicKey))
    con.commit()

    cur.execute("INSERT INTO Accounts(accountId, webAppId, mobileAppId) values(?, ?, ?)", (accountId, webAppId, mobileAppId))
    con.commit()

    





if __name__ == "__main__":
    mobileAppId = "4046f7aa-76bd-4982-8ab9-3e4d26d70e47"
    webAppId = "b2fd0695-47f4-4aa8-aa46-04f3a0218493"
    accountId = "f62bd482-ccd9-4368-8db2-2daeaa8d28f6"
    token = "0e97afa5-ad91-425f-93f9-f669b61371de"
    timeCreated = 1670359183
    timeAlive = 120

    start = time.time()
    db_createLoginToken(webAppId, token, timeCreated, timeAlive)
    db_associateAccountWithLoginToken(mobileAppId, token)
    db_authorizeLoginToken(token)
    db_checkLoginTokenAuthorization(token)
    end = time.time()
    print(start)
    print(end - start)
    
    
    # start = time.time()
    # con=sqlite3.connect("performance\server.db")
    # cur = con.cursor()
    # for i in range (404000):
    #     if i % 1000 == 0:
    #         print(str(i) + ": "+ str(time.time() - start))
    #         start = time.time()
    #     fill(con, cur)
    # con.close()


    
    # start = time.time()
    # con=sqlite3.connect("performance\server.db")
    # cur = con.cursor()
    # cur.execute("INSERT INTO LoginTokens(webAppId, token, timeCreated, timeAlive, authorized) values(?, ?, ?, ?, ?)", (webAppId, token, timeCreated, timeAlive, 0))
    # con.commit()
    
    # webAppId = db_getWebAppFromToken(token)
    # accountId = db_getAccount(mobileAppId, webAppId)
    # cur.execute("UPDATE LoginTokens SET accountId = ? WHERE token = ?", (accountId, token))
    # con.commit()

    # cur.execute("UPDATE LoginTokens SET authorized = ? WHERE token = ?", (1, token))
    # con.commit()

    # res = cur.execute("SELECT authorized FROM LoginTokens WHERE token = ?", (token, ))
    # isAuthorized = res.fetchone()
    # con.close()
    # end = time.time()
    

    # print(end - start)
    


    pass