from flask import Flask, g, jsonify
from flask import request

# from flask_restx import Resource

import ssl
import json
from gen_jwt import get_access_token

app = Flask(__name__)


import requests



def message_handler(data):
    global access_token
    botId = 5094423
    # print(data['type'])
    userId = data['source']['userId']
    # print(data['source']['userId'])
    # print(data['content']['text'])
    # # userId = g.userId
    msg = data['content']['text']
    token_url = f'https://www.worksapis.com/v1.0/bots/{botId}/users/{userId}/messages'
    
    headers = {
        'Authorization' : f'Bearer {access_token}',
        'content-Type':'application/json'
    }
    request_body = {
        "content": {
            "type": "text",
            "text": "msg"
        }
    }
    

    response = requests.post(token_url, headers=headers, data=json.dumps(request_body))

    # print(response.json())

    return userId

def form_handler(data):
    ...


def register_rich_menu():
    global access_token
    botId = 5094423

    rich_url = f'https://www.worksapis.com/v1.0/bots/{botId}/richmenus'
    headers = {
        'Authorization' : f'Bearer {access_token}',
        'content-Type':'application/json'
    }
    request_body = {
        "richmenuName": "Example Richmenu",
        "areas": [
            {
            "action": {
                "type": "postback",
                "label": "Example label",
                "data": "Example data",
                "displayText": "Example displayText",
                "i18nDisplayTexts": [
                {
                    "language": "en_US",
                    "displayText": "Example display text"
                }
                ],
                "i18nLabels": [
                {
                    "language": "en_US",
                    "label": "Example label"
                }
                ]
            },
            "bounds": {
                "x": 0,
                "y": 0,
                "width": 2500,
                "height": 843
            }
            }
        ],
        "size": {
            "width": 2500,
            "height": 843
        }
    }
    response = requests.post(rich_url, headers=headers, data=json.dumps(request_body))
    print('rich response', response.json())


def get_rich_menu():
    global access_token
    botId = 5094423
    headers = {
        'Authorization' : f'Bearer {access_token}',
        'content-Type':'application/json'
    }
    richmenu_url = f'https://www.worksapis.com/v1.0/bots/{botId}/richmenus'
    response = requests.get(richmenu_url, headers=headers)
    print('get rich response', response.json())


def register_persistent_menu():
    global access_token
    botId = 5094423

    persistent_url = f'https://www.worksapis.com/v1.0/bots/{botId}/persistentmenu'
    headers = {
        'Authorization' : f'Bearer {access_token}',
        'content-Type':'application/json'
    }
    request_body = {
        "content": {
            "actions": [
            {
                "type": "message",
                "label": "Example label",
                "text": "Example text",
                "postback": "Example postback",
                "i18nLabels": [
                {
                    "language": "en_US",
                    "label": "Example label"
                }
                ],
                "i18nTexts": [
                {
                    "language": "en_US",
                    "text": "Example text"
                }
                ]
            },
            {
                "type": "uri",
                "label": "Example Homepage",
                "uri": "https://example.com",
                "i18nLabels": [
                {
                    "language": "en_US",
                    "label": "Example label"
                }
                ]
            }
            ]
        }
    }
    

    response = requests.post(persistent_url, headers=headers, data=json.dumps(request_body))
    print('persistent menu', response.json())

def add_richmenu_bot(botId, richmenuId, userId):
    global access_token
    url = f'https://www.worksapis.com/v1.0/bots/{botId}/richmenus/{richmenuId}/users/{userId}'
    
    headers = {
        'Authorization' : f'Bearer {access_token}',
        'content-Type':'application/json'
    }
    requests.post(url, headers=headers)

def btnmessageToUser(botId, userId):
    url = f'https://www.worksapis.com/v1.0/bots/{botId}/users/{userId}/messages'

    headers = {
        'Authorization' : f'Bearer {access_token}',
        'content-Type':'application/json'
    }
    request_body = {
        "content": {
            "type": "button_template",
            "contentText": "출퇴근시간 기록",
            "actions": [{
                "type": "message",
                "label": "출근",
                "postback" : "work"
                }, {
                "type": "message",
                "label": "퇴근",
                "postback": "workoff"
                }
            ]
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(request_body))

functions = {
    'message' : message_handler,
    'postback' : postback_handler,
    'leave' : leave_handler,
    'join' : join_handler,
    'left' : left_handler

}

def postback_handler(data):

    userId = data['source']['userId']
    # postback data어떻게 오는지 확인하고 처리하기
    issued_time = data['issuedTime']
    action = data['data']
    return userId


access_token = None
@app.route('/', methods=['GET', 'POST'])
def home():
    global access_token
    if access_token == None:
        token_data = get_access_token()
        access_token = token_data['access_token']
    # requests.get(api_url).json()  

    data = request.get_json()
    request_type = data['type']

    userId = functions[request_type](data)


    botId = 5094423
    
    # register_persistent_menu()
    # userId = message_handler(data)
    btnmessageToUser(botId, userId)

    # richmenuId = '914034'
    # get_rich_menu()
    # add_richmenu_bot(botId, richmenuId, userId)
    # register_rich_menu()
    # get_rich_menu()
    

    return 'hello world'

def upload_richmenu_image(botId):
    url = f'https://www.worksapis.com/v1.0/bots/{botId}/attachments'

    headers = {
        'Authorization' : f'Bearer {access_token}',
        'content-Type':'application/json'
    }
    request_body = {
        'fileName' : 'Untitled.png',
    }
    response = requests.post(url, headers=headers, data=json.dumps(request_body))

    print(response.json())

def set_richmenu_image(botId, richmenuId, imageId):
    url = f'https://www.worksapis.com/v1.0/bots/{botId}/richmenus/{richmenuId}/image'

    headers = {
        'Authorization' : f'Bearer {access_token}',
        'content-Type':'application/json'
    }
    request_body = {
        'fileName' : imageId,
    }
    response = requests.post(url, headers=headers, data=json.dumps(request_body))

    print(response.json())

def fixdefaultRichmenu():
    global access_token
    botId = 5094423
    print(access_token)
    url = f'https://www.worksapis.com/v1.0/bots/{botId}'

    headers = {
        'Authorization' : f'Bearer {access_token}',
        'content-Type':'application/json'
    }
    request_body = {
        'defaultRichmenuId' : '914034',
    }
    response = requests.patch(url, headers=headers, data=json.dumps(request_body))

    print(response.json())
if __name__== '__main__':
    # access_token
    # botId = 5094423
    # richmenuId = '914034'
    # if access_token == None:
    #     token_data = get_access_token()
    #     access_token = token_data['access_token']

    # # fixdefaultRichmenu()
    # imageId = 'kr1.1678085096499435088.1678171496.1.5094423.0.0.0'
    # set_richmenu_image(botId, richmenuId, imageId)
    # upload_richmenu_image(botId)
    
    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    # ssl_context.load_cert_chain(certfile='ssl/Certificate.crt', keyfile='privkey.pem', password='secret')
    app.run(debug=True, port=5000)# ssl_context=ssl_context)