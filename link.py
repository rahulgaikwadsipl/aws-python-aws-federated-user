import urllib, json
import requests 
import boto3 
import urllib.parse
import sys
import cgi
import json
import boto3.session
import urllib.request

try:

    response = {}
    arn = sys.argv[1]
    cli_profile = sys.argv[2]
    rolid=sys.argv[3]

    my_sesison = boto3.Session(profile_name=cli_profile)
    sts_connection = my_sesison.client('sts')
    assumed_role_object = sts_connection.assume_role(RoleArn=arn,
            RoleSessionName=str(rolid))
   

    json_string_with_temp_credentials = '{'
    json_string_with_temp_credentials += '"sessionId":"' \
        + assumed_role_object.get('Credentials').get('AccessKeyId') \
        + '",'
    json_string_with_temp_credentials += '"sessionKey":"' \
        + assumed_role_object.get('Credentials').get('SecretAccessKey') \
        + '",'
    json_string_with_temp_credentials += '"sessionToken":"' \
        + assumed_role_object.get('Credentials').get('SessionToken') \
        + '"'
    json_string_with_temp_credentials += '}'

    request_parameters = '?Action=getSigninToken'
    request_parameters += '&SessionDuration=7200'
    request_parameters += '&Session=' \
        + urllib.parse.quote(json_string_with_temp_credentials)
    request_url = 'https://signin.aws.amazon.com/federation' \
        + request_parameters
    r = requests.get(request_url)

    signin_token = json.loads(r.text)

    request_parameters = '?Action=login'
    request_parameters += '&Issuer=https://www.xxxxx.com/'
    request_parameters += '&Destination=' \
        + urllib.parse.quote('https://console.aws.amazon.com/')
    request_parameters += '&SigninToken=' + signin_token['SigninToken']
    request_url = 'https://signin.aws.amazon.com/federation' \
        + request_parameters

    conn = urllib.request.urlopen(request_url)  
    status_code=conn.getcode()
    if status_code==200:
        response = '{"response":"true","log":"' + request_url + '"}'
        print (response)
    else:
        response = '{"response":"false","log":"Error in genrate URL!"}'
        print (response)
except Exception as e:
    response = '{"response":"false","log":"' + str(e) + '"}'
    print (response)
