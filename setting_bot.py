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