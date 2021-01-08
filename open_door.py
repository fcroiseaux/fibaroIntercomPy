# Python script to Open the portal door
# Version to integrate into homeassistant


from websocket import create_connection
import json
import sys
import ssl
import configparser


@service
def open_portal():
    parser = configparser.ConfigParser()   
    parser.read('intercom.ini')
    log.info(parser.sections())
    addr = parser.get('INTERCOM', 'intercom_addr')
    user = parser.get('INTERCOM', 'user')
    password = parser.get('INTERCOM', 'password')
    open_intercom_door(addr, user, password)


def open_intercom_door(intercom_addr=None, user=None, password=None):

    if ((intercom_addr == "") or (user == "") or (password == "")) :
        log.error("Error missing argument to open the FIBARO INTERCOM DOOR")
        exit()

    ws = create_connection("wss://"+intercom_addr+":8081/wsock", sslopt={"cert_reqs": ssl.CERT_NONE}) #NO SSL Verification because Fibaro certificates is not recognized


    # CONNECT AND GET TOKEN
    jsonrpc = {
        "jsonrpc": "2.0",
        # Method name
        "method": "com.fibaro.intercom.account.login",
        # Parameters
        "params": {
            # Username for local account
            "user": user,
            # Password for local account
            "pass": password
        },
        "id": "1"
    }

    rpcStr = json.dumps(jsonrpc)
    ws.send(rpcStr)

    resp = ws.recv()
    log.info("Connected to FIBARO INTERCOMM " + resp)

    jsonToken = json.loads(resp)

    token = jsonToken['result']['token']

    #Open the Door
    openDoorJson = {
        "jsonrpc": "2.0",
        # Method name
        "method": "com.fibaro.intercom.relay.open",
        # Parameters
        "params": {
            "token": token,
            "relay": 0
        },
        "id": "1"
    }

    openReqStr = json.dumps(openDoorJson)
    ws.send(openReqStr)

    result = ws.recv()
    log.info("Request sent to open the door : " + result)

    #Logout
    logoutJson = {
        "jsonrpc": "2.0",
        # Method name
        "method": "com.fibaro.intercom.account.logout",
        # Parameters
        "params": {
            "token": token
        },
        "id": "1"
    }

    logoutReqStr = json.dumps(logoutJson)
    ws.send(logoutReqStr)

    result = ws.recv()
    log.info("Logout performed")

    ws.close()

