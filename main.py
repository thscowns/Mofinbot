from flask import Flask, g, jsonify
from flask import request
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
# from flask_restx import Resource

# DB
# from models import User, CommuteRecord
# from database import db_session

from datetime import datetime, timedelta
import requests
import ssl
import json
from gen_jwt import get_access_token, refresh_access_token

app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


## model 
class User(db.Model):
    __tablename__ = 'Users'

    user_id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(32))
    commute_state = db.Column(db.String(32), default='work')
    commutes = db.relationship('CommuteRecord', backref='Users', lazy=True)
    

class CommuteRecord(db.Model):
    __tablename__ = 'CommuteRecords'
    commute_id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(32), db.ForeignKey('Users.user_id'))

    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)

db.init_app(app)
# with app.app_context():
#     db.create_all()

botId =5094423

user_commute_dict = {}

def commit_user(user_id, user_name, status):
    user = User(user_id=user_id, name=user_name, commute_state=status)
    db.session.add(user)
    db.session.commit()

def user_status_update(user_id, status):
    user = User.query.filter_by(user_id=user_id).first()
    user.commute_state = status
    db.session.commit()

def workoff_commute_update(user_id, t):
    commute = CommuteRecord.query.filter_by(userid=user_id).order_by(CommuteRecord.commute_id.desc()).first()
    print(commute)
    commute.end_time = t
    db.session.commit()

def commit_commute(user_id, t):
    # t - datetime 형식 .. ? 
    commute_record = CommuteRecord(
        userid=user_id,
        start_time=t
    )

    db.session.add(commute_record)
    db.session.commit()

def check_user_exists(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        return True
    else:
        return False

def query_user(userId):
     user = User.query.filter_by(user_id=userId).first()
     return user

def query_users():
    users = User.query.all()
    for user in users:
        print(user)
    return users

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
    if check_user_exists(userId):
        ...
    else:
        name = get_userName_by_userId(userId)
        commit_user(userId, name, status)
    # user_commute_dict[userId] = commute_record(name, status, t)
    user_status_update(userId, status)
    commit_commute(userId, t)
    
    # 완료 메시지 전송
    msg_to_user(userId, t.strftime('%Y-%m-%d %H: %M') + ': 출근 완료!')

def workoff_handler(userId, t):
    # global user_commute_dict

    modify_profile_status(userId, status='LEAVE_OFFICE')
    status = 'workoff'
    if check_user_exists(userId):
        ...
    else:
        name = get_userName_by_userId(userId)
        commit_user(userId, name, status)
    # user_commute_dict[userId] = commute_record(name, status, t)
    # commit_commute(userId, t, status)
    user_status_update(userId, status)
    workoff_commute_update(userId, t)

    msg_to_user(userId, t.strftime('%Y-%m-%d %H: %M') + ': 퇴근 완료!')

def inqall_handler(userId, t):
    # global user_commute_dict
    msg = ''
    # for key in user_commute_dict.keys():
    #     msg += user_commute_dict[key].make_msg()
    # user = User.query.all()
    # print(1)
    users = query_users()
    for user in users:
        msg += f'{user.name} - {user.commute_state} \n'
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
    elif data['content']['postback'] not in postback_handler_functions.keys():
        btnmessageToUser(botId, userId)
    else:
        postback_type = data['content']['postback']
        t = data['issuedTime']
        t = datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.%fZ')
        t += timedelta(hours=9)
    
        if check_user_exists(userId):
            user = query_user(userId)
            if user.commute_state == postback_type:
                msg_to_user(userId, '출퇴근 잘못찍음')
            else:
                postback_handler_functions[postback_type](userId, t)
        else:
            if postback_type == 'workoff':
                msg_to_user(userId, '출근 먼저 찍어주세요')
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
    'start' : join_handler,
    'left' : left_handler
}

access_token = None
@app.route('/', methods=['POST'])
async def home():
    
    # requests.get(api_url).json()  
    data = request.get_json()
    request_type = data['type']
    print(request_type)
    print('request data', data)
    userId = await functions[request_type](data)

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