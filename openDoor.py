# Python script to Open the portal door
# EG. to integrate in homeassistant


from websocket import create_connection
import json
import sys
import ssl


if (len(sys.argv) != 4) :
    print("Usage : openDoor.py INTERCOM_ADDR USER PASSWORD")
    print("Script needd 3 arguments")
    exit()


INTERCOMM_ADDR = sys.argv[1]
INTERCOM_USER = sys.argv[2]
INTERCOM_PASSWORD = sys.argv[3]

ws = create_connection("wss://"+INTERCOMM_ADDR+":8081/wsock", sslopt={"cert_reqs": ssl.CERT_NONE}) #NO SSL Verification because Fibaro certificates is not recognized


# CONNECT AND GET TOKEN
jsonrpc = {
    "jsonrpc": "2.0",
    # Method name
    "method": "com.fibaro.intercom.account.login",
    # Parameters
    "params": {
        # Username for local account
        "user": INTERCOM_USER,
        # Password for local account
        "pass": INTERCOM_PASSWORD
    },
    "id": "1"
}

rpcStr = json.dumps(jsonrpc)
ws.send(rpcStr)

resp = ws.recv()

jsonToken = json.loads(resp)

token = jsonToken['result']['token']

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

ws.close()

