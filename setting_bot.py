# from gen_jwt import get_access_token
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
    return response.json()['fileId'], response.json()['uploadUrl']

def set_richmenu_image(botId, richmenuId, fileId):
    global access_token
    print(access_token)
    url = f'https://www.worksapis.com/v1.0/bots/{botId}/richmenus/{richmenuId}/image'

    headers = {
        'Authorization' : f'Bearer {access_token}',
        'content-Type':'application/json'
    }
    request_body = {
        "fileId": f'{fileId}'
    }
    response = requests.post(url, headers=headers, data=json.dumps(request_body))
    print(response)
    # print(response.json())

def get_botcontents(botId, fileId):
    url = f'https://www.worksapis.com/v1.0/bots/{botId}/attachments/{fileId}'
    headers = {
        'Authorization' : f'Bearer {access_token}'
        # 'content-Type':'application/json'
    }
    response = requests.get(url, headers=headers)

    print(response.json())

def fixdefaultRichmenu(richmenuId):
    global access_token
    botId = 5094423
    print(access_token)
    url = f'https://www.worksapis.com/v1.0/bots/{botId}'

    headers = {
        'Authorization' : f'Bearer {access_token}',
        'content-Type':'application/json'
    }
    request_body = {
        'defaultRichmenuId' : richmenuId,
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

def upload_contents(url, fileName):
    '''
    curl -XPOST 'http://apis-storage.worksmobile.com/k/emsg/r/kr1/1678279692875495483.1678366092.1.5094423.0.0.0/test.png'\
    -H 'Authorization: Bearer kr1AAABNAHZpjnOG0+/RWYINt9Fw6tRlA4MznIx6IUoKILWpsFdIqbewK7gCJosTNnI4NSPW1Rlav8cD8nLjWeXl733Q++uXwxeGZmHNNX1c8F2s6BPOOuf0f6vzmPsTuAO1uBp+pfqBU3gURZmXuBBAJ8tMJkmoYaYLR7xc2EJ9SX0EF9CsdFZFeY7x3VXy4NNh1XQcn23Gqed7U5VL5sCbGUj3UvkDoMgnonTq/NVbgXswQX0J5jC0LVdDqt6+ygBZXKFZB5WCVQM+hXcS6vvq4+HlN+X7wGX0jHCB7Cy/NLcuw3FNXZBs2mqN+LBFVnl97K3gq0tSw2xxeACxzMiDt6paMrYdaWRKm/AVx8s+5hAV2vvc+t+fftzfoqR6Mb1uBAQZXGZocUbiUZqaG3CCGCNjCwoJce0e7KHAPlWIOqN7d8U'\
    -H 'Content-Type: multipart/form-data'\
    -F 'resourceName=Untitled.png'\
    -F 'FileData=@Untitled.png
    '''
    global access_token
    headers = {
        'Authorization' : f'Bearer {access_token}',
        'Content-Type': 'multipart/form-data'
    }
    multiple_files = [
        ('images', (fileName, open(fileName, 'rb'), 'image/png'))
    ]
    response = requests.post(url, headers=headers, files=multiple_files)
    print(response.json())


# token_data = get_access_token()
# access_token = token_data['access_token']

botId = 5094423
# print(access_token)
access_token = 'kr1AAABM8NwRCxNER+AOmR0ASK4dYD0EkZRrh/oU3RVi807KVqCAZoxeo6R6QjhzRWZckyR6HY6Bv6bGDVNvDPuQv/+RRcZuj8iX3bE7ZQvDSV7YSI0wAep5n0vO9viKo0Ou7tCjV5w0JMsiUssAh1Ci/HU5W3iHcYYQnVbiRPYVGyi2x44H/ZnkxD9XaCPpNxp+Sk/xGt0Xg8e5Ogq7Kf6g7j7tYQmU7+1VgyTFI+8pgrRru+3cdPyosD8Jhywm9KELXQKY4Rl5niIgMAme+S1aKp9jA0rMAiiVhmAmqZ3q2R/7EwxKIdAtw97T8/F6iGGfQ/Wrh26HGsc35fMl62mtrjVAwOhAIIGczD8/fT5kF90p2DeUbn4CKjwq/cT3f7T6ImUOCNelx2LTi67v7PraUFxbTEXbuFGpDWWYCQsIhVzBlYD'
richmenus = get_rich_menu()
# fileId = 'kr1.1678279692875495483.1678366092.1.5094423.0.0.0'
# uploadUrl = 'http://apis-storage.worksmobile.com/k/emsg/r/kr1/1678279692875495483.1678366092.1.5094423.0.0.0/test.png'
richmenuId = '917357'
# fileId = upload_richmenu_image(botId)
fileName = 'test.png'
# fileId, uploadUrl = upload_richmenu_image(botId, fileName)
# fileId = 'kr1.1678280287172991665.1678366687.1.5094423.0.0.0'
# untitled -> image size error
fileId = "kr1.1678325771554234405.1678412171.1.5094423.0.0.0"
print(fileId)

fileId = 'kr1.1678326920841516667.1678413320.1.5094423.0.0.0'
# upload_contents(uploadUrl, fileName)
# 리치 메뉴 이미지 설정
set_richmenu_image(botId, richmenuId, fileId)

# default 리치메뉴 설정
# fixdefaultRichmenu(richmenuId)
# get_botcontents(botId, fileId)
# uploadUrl = 'http://apis-storage.worksmobile.com/k/emsg/r/kr1/1678280703295897496.1678367103.1.5094423.0.0.0/test1.png'

# richmenu들 삭제
# print(richmenus)
# print(len(richmenus))
# for i in range(len(richmenus)):
#     delete_richmenu(richmenus[i]['richmenuId'])

# richmenus = get_rich_menu()


