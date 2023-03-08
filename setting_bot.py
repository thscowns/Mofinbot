from gen_jwt import get_access_token
import requests
import json
access_token = None

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
    return response.json()


def get_rich_menu():
    global access_token
    print(access_token)
    botId = 5094423
    headers = {
        'Authorization' : f'Bearer {access_token}',
        'content-Type':'application/json'
    }
    richmenu_url = f'https://www.worksapis.com/v1.0/bots/{botId}/richmenus'
    response = requests.get(richmenu_url, headers=headers)
    print('get rich response', response.json())
    return response.json()['richmenus']


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

def upload_richmenu_image(botId, fileName):
    global access_token
    url = f'https://www.worksapis.com/v1.0/bots/{botId}/attachments'

    headers = {
        'Authorization' : f'Bearer {access_token}',
        'content-Type':'application/json'
    }
    request_body = {
        'fileName' : fileName,
    }
    response = requests.post(url, headers=headers, data=json.dumps(request_body))

    print(response.json())
    return response.json()['fileId']

def set_richmenu_image(botId, richmenuId, fileId):
    url = f'https://www.worksapis.com/v1.0/bots/{botId}/richmenus/{richmenuId}/image'

    headers = {
        'Authorization' : f'Bearer {access_token}',
        'content-Type':'application/json'
    }
    request_body = {
        "fileId": fileId,
        "i18nFileIds": [
            {
            "language": "en_US",
            "fileId": fileId
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(request_body))

    print(response.json())
def get_botcontents(botId, fileId):
    url = f'https://www.worksapis.com/v1.0/bots/{botId}/attachments/{fileId}'
    headers = {
        'Authorization' : f'Bearer {access_token}'
        # 'content-Type':'application/json'
    }
    response = requests.get(url, headers=headers)

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

def delete_richmenu(richmenuId):
    botId = 5094423
    url =f'https://www.worksapis.com/v1.0/bots/{botId}/richmenus/{richmenuId}'

    headers = {
        'Authorization' : f'Bearer {access_token}'
        # 'content-Type':'application/json'
    }
    response = requests.delete(url, headers=headers)

token_data = get_access_token()
access_token = token_data['access_token']

botId = 5094423
print(access_token)
richmenus = get_rich_menu()
fileId = 'kr1.1678279692875495483.1678366092.1.5094423.0.0.0'
uploadUrl = 'http://apis-storage.worksmobile.com/k/emsg/r/kr1/1678279692875495483.1678366092.1.5094423.0.0.0/test.png'
richmenuId = '917357'
# fileId = upload_richmenu_image(botId)
fileName = 'test1.png'
# fileId = upload_richmenu_image(botId, fileName)
# fileId = 'kr1.1678280287172991665.1678366687.1.5094423.0.0.0'
fileId = 'kr1.1678280703295897496.1678367103.1.5094423.0.0.0'
print(fileId)
# set_richmenu_image(botId, richmenuId, fileId)
get_botcontents(botId, fileId)
uploadUrl = 'http://apis-storage.worksmobile.com/k/emsg/r/kr1/1678280703295897496.1678367103.1.5094423.0.0.0/test1.png'


# print(richmenus)
# print(len(richmenus))
# for i in range(len(richmenus)):
#     delete_richmenu(richmenus[i]['richmenuId'])

# richmenus = get_rich_menu()


