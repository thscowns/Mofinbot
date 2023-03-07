import time
import datetime
import jwt
import json
import requests

client_id = 'PXilJ4nxms_4dKdV7KkH'
client_secret = 'RA9bWLrUAA'

service_account = 'ukubw.serviceaccount@mofin.kr'
private_key_file = 'private_20230303103549.key'


def get_jwt_encode():
    iat = datetime.datetime.utcnow()
    exp = iat + datetime.timedelta(seconds=3600)
    print(client_id, client_secret, service_account, iat, exp)

    JSON_Claimset = {
        'iss' : client_id,
        'sub' : service_account,
        'iat' : iat,
        'exp' : exp
    }



    with open(private_key_file, mode='rb') as file: # b is important -> binary
        private_key = file.read()
    # print(private_key)
    header = {
        'alg' : 'RS256',
        'typ' : 'JWT'
    }
    jwt_encode = jwt.encode(JSON_Claimset, key=private_key, algorithm='RS256', headers=header)
    return jwt_encode

async def get_access_token():

    token_url = 'https://auth.worksmobile.com/oauth2/v2.0/token'
    headers = {
        'content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
    }
    jwt_encode = get_jwt_encode()
    request_body = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'client_id' : client_id,
        'client_secret' : client_secret,
        'assertion' : jwt_encode,
        'scope' : 'bot,user,calendar'
    }
    response = requests.post(token_url, headers=headers, data=request_body)
    # print(response.headers)
    # print(response.json())
    data = response.json()
    access_token = data['access_token']
    # print(access_token)
    return data

print(get_access_token())
