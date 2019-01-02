import argparse
import json
from datetime import datetime
from requests_hawk import HawkAuth

import requests

user_id = '<user_id>'
key = '<api_key>'
timezoneName = 'CET'
timezone = '+0100'


def get_time():
    (dt, micro) = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f').split('.')
    return '%s.%03dZ' % (dt, int(micro) / 1000)


def do_start():
    payload = {
        'userId': user_id,
        'start': get_time(),
        'end': None,
        'timezoneName': timezoneName,
        'timezone': timezone,
        'type': 'work'
    }

    url = 'https://app.absence.io/api/v2/timespans/create'
    data = json.dumps(payload)
    hawk_auth = HawkAuth(id=user_id, key=key, server_url=url)

    request_response = requests.post(url, auth=hawk_auth, data=data, headers={'Content-Type': 'application/json'})

    return request_response


def do_stop():
    payload = {
        'filter': {
            'userId': user_id,
            'end': {'$eq': None}
        },
        'limit': 10,
        'skip': 0
    }

    url = 'https://app.absence.io/api/v2/timespans'
    data = json.dumps(payload)
    hawk_auth = HawkAuth(id=user_id, key=key, server_url=url)

    request_response = requests.post(url, auth=hawk_auth, data=data, headers={'Content-Type': 'application/json'})
    if request_response.ok:
        request_response = json.loads(request_response.text)
        entry = request_response['data'][0]
    else:
        return False

    payload = {
        'start': entry['start'],
        'end': get_time(),
        'timezoneName': timezoneName,
        'timezone': timezone
    }

    url = 'https://app.absence.io/api/v2/timespans/{}'.format(entry['_id'])
    data = json.dumps(payload)

    hawk_auth = HawkAuth(id=user_id, key=key, server_url=url)
    request_response = requests.put(url, auth=hawk_auth, data=data, headers={'Content-Type': 'application/json'})
    return request_response


parser = argparse.ArgumentParser()
parser.add_argument('do', help='start/stop')
args = parser.parse_args()

if args.do == 'start':
    response = do_start()
else:
    response = do_stop()

if response is not False and response.ok:
    print('Done.')
else:
    print('Error: ' + response.text)
