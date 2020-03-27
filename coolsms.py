from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

from config.settings._base import SECRETS

api_key = SECRETS['API_KEY']
api_secret = SECRETS['API_SECRET']

params = dict()
params['type'] = 'sms'
params['to'] = ''
params['from'] = ''
params['text'] = 'Test Message'

cool = Message(api_key, api_secret)
try:
    response = cool.send(params)
    print("Success Count: %s" % response['success_count'])
    print("Error Count: %s" % response['error_count'])
    print("Group ID: %s" % response['group_id'])

    if "error_list" in response:
        print("Error List: %s" % response['error_list'])

except CoolsmsException as e:
    print("Error Code: %s" % e.code)
    print("Error Message: %s" % e.msg)
