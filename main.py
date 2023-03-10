from flask import Flask, g, jsonify
from flask import request
from flask_apscheduler import APScheduler
# from flask_restx import Resource

from datetime import datetime, timedelta
import ssl
import json
from gen_jwt import get_access_token, refresh_access_token

app = Flask(__name__)


import requests
botId =5094423

user_commute_dict = {}
class commute_record():
    def __init__(self, userName, status, t):
        self.userName = userName
        self.status = status
        self.t = t
    
    def make_msg(self):
        time_str = self.t.strftime('%Y-%m-%d %H: %M')
        msg = f'{self.userName} :  {self.status}, {time_str}\n'

        return msg

def add_user_profile_status(userId):
    global access_token
    url = f'https://www.worksapis.com/v1.0/users/{userId}/user-profile-statuses'
    headers = {
        'Authorization' : f'Bearer {access_token}',
        'content-Type':'application/json'
    }
    request_body = {
        "profileStatusId": "CUSTOM01",
        "statusMessage": "test",
        
    }
    response = requests.post(url, headers=headers, data=json.dumps(request_body))
    print('add user_profilestatus', response.json())
    userProfileStatusId = response.json()['userProfileStatusId']

    return userProfileStatusId

def get_user_profile_status(userId):
    global access_token
    url = f'https://www.worksapis.com/v1.0/users/{userId}/user-profile-statuses'
    headers = headers = {
        'Authorization' : f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)
    # status 설정 x 한 경우
    if not data['userProfileStatuses']:
        userProfileStatusId = add_user_profile_status(userId)
    else:
        userProfileStatusId = data['userProfileStatuses'][0]['userProfileStatusId']
    return userProfileStatusId

def modify_profile_status(userId, status):
    global access_token, botId

    userProfileStatusId = get_user_profile_status(userId)
    url = f'https://www.worksapis.com/v1.0/users/{userId}/user-profile-statuses/{userProfileStatusId}'
    headers = {
        'Authorization' : f'Bearer {access_token}',
        'content-Type':'application/json'
    }
    request_body = {
        "profileStatusId": status,
        "statusMessage": "status test",
        # "startTime": "2017-03-16T09:00:00+09:00",
        # "endTime": "2017-03-18T18:00:00+09:00",
        # "autoReplyMail": {
        #     "internal": {
        #     "content": "internal mail content",
        #     "sentDirectlyToMe": true
        #     },
        #     "external": {
        #     "content": "external mail content",
        #     "sentDirectlyToMe": false
        #     }
        # }
    }

    response = requests.put(url, headers=headers, data=json.dumps(request_body))
    print('change status', response.json())


def work_handler(userId, t):
    global user_commute_dict
    # status change
    modify_profile_status(userId, status='CUSTOM01')
    status = 'work'
    # 기록 - how?
    name = get_userName_by_userId(userId)
    user_commute_dict[userId] = commute_record(name, status, t)
    
    # 완료 메시지 전송
    msg_to_user(userId, t.strftime('%Y-%m-%d %H: %M') + ': 출근 완료!')

def workoff_handler(userId, t):
    global user_commute_dict

    modify_profile_status(userId, status='LEAVE_OFFICE')
    status = 'workoff'
    name = get_userName_by_userId(userId)
    user_commute_dict[userId] = commute_record(name, status, t)

    msg_to_user(userId, t.strftime('%Y-%m-%d %H: %M') + ': 퇴근 완료!')

def inqall_handler(userId, t):
    global user_commute_dict
    msg = ''
    for key in user_commute_dict.keys():
        msg += user_commute_dict[key].make_msg()

    msg_to_user(userId, msg)


def get_userName_by_userId(userId):
    global access_token
    url = f'https://www.worksapis.com/v1.0/users/{userId}'

    headers = headers = {
        'Authorization' : f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    name = data['userName']['lastName'] + data['userName']['firstName']
    return name

postback_handler_functions = {
    'work' : work_handler,
    'workoff' : workoff_handler,
    'inqall' : inqall_handler
}

def msg_to_user(userId, msg):
    global access_token, botId
    token_url = f'https://www.worksapis.com/v1.0/bots/{botId}/users/{userId}/messages'
    
    headers = {
        'Authorization' : f'Bearer {access_token}',
        'content-Type':'application/json'
    }
    request_body = {
        "content": {
            "type": "text",
            "text": f"{msg}"
        }
    }
    
    response = requests.post(token_url, headers=headers, data=json.dumps(request_body))

async def message_handler(data):

    # print(data['type'])
    userId = data['source']['userId']
    # print(data['source']['userId'])
    # print(data['content']['text'])
    # # userId = g.userId
    msg = data['content']['text']
    if 'postback' not in data['content'].keys():
        # get message
        # msg_to_user(userId, msg)
        btnmessageToUser(botId, userId)
    else:
        postback_type = data['content']['postback']
        t = data['issuedTime']
        t = datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.%fZ')
        t += timedelta(hours=9)

        # t = t.strftime('%Y-%m-%d %H: %M')
        if userId in user_commute_dict.keys():
            if user_commute_dict[userId].status == postback_type:
                msg_to_user(userId, '출퇴근 잘못찍음')
            else:
                postback_handler_functions[postback_type](userId, t)
        else:
            postback_handler_functions[postback_type](userId, t)
    

    # print(response.json())
    

    return userId



def btnmessageToUser(botId, userId):
    print('btnmessage')
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
                }, {
                "type": "message",
                "label": "조회",
                "postback" : "inqall"
                }
            ]
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(request_body))
    # print(response.json())


async def leave_handler():
    ...

async def join_handler(data):
    global botId
    userId = data['source']['userId']
    btnmessageToUser(botId, userId)

async def left_handler():
    ...

async def postback_handler(data):
    print('postback handler - request data', data)
    userId = data['source']['userId']
    # postback data어떻게 오는지 확인하고 처리하기
    issued_time = data['issuedTime']
    action = data['data']
    return userId

functions = {
    'message' : message_handler,
    'postback' : postback_handler,
    'leave' : leave_handler,
    'join' : join_handler,
    'left' : left_handler
}

access_token = None
@app.route('/', methods=['GET', 'POST'])
async def home():
    
    # requests.get(api_url).json()  
    data = request.get_json()
    request_type = data['type']
    print(request_type)
    print('request data', data)
    userId = await functions[request_type](data)


    botId = 5094423
    
    # register_persistent_menu()
    # userId = message_handler(data)
    

    # richmenuId = '914034'
    # get_rich_menu()
    # add_richmenu_bot(g.botId, richmenuId, userId)
    # register_rich_menu()
    # get_rich_menu()
    

    return 'hello world'

class Config:
    '''App configuration'''
    SCHEDULER_API_ENABLED = True


scheduler = APScheduler()
@scheduler.task('interval', id='do_job_1', seconds=86000, misfire_grace_time=100)
def do_refresh_token():
    global token_data
    print('refresh access token')
    data = refresh_access_token(token_data['refresh_token'])
    # print(token_data)
    access_token = data['access_token']
        

token_data = None
if access_token == None:
    print('before app start get access token ')
    token_data = get_access_token()
    access_token = token_data['access_token']

scheduler.init_app(app)
scheduler.start()
# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
# ssl_context.load_cert_chain(certfile='ssl/Certificate.crt', keyfile='privkey.pem', password='secret')
app.run(debug=True, port=5000)# ssl_context=ssl_context)