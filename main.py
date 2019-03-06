import json
import config
from requests_oauthlib import OAuth1Session

target_user = 'shqru_mix'

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

follow_url = "https://api.twitter.com/1.1/friends/ids.json"

id_params = {
    'count': 2500,
    'screen_name': target_user,
    'stringify_ids':'true'
}

req = twitter.get(follow_url, params=id_params)

if req.status_code == 200:
    ids_str = ','.join(json.loads(req.text)['ids'])
else:
    print("ERROR: %d" % req.status_code)

lookup_url = "https://api.twitter.com/1.1/friendships/lookup.json"

lk_params = {
    'user_id': ids_str
}

req = twitter.get(lookup_url, params=lk_params)
lookups = None
if req.status_code == 200:
    lookups = json.loads(req.text)
else:
    print("ERROR: %d" % req.status_code)

remove_list = []

for lookup in lookups:
    connections = lookup['connections']
    if (not 'followed_by' in connections) and ('following' in connections):
        remove_list.append(lookup['id_str'])

remove_url = "https://api.twitter.com/1.1/friendships/destroy.json"

for rem_id in remove_list[:1]:
    rem_params = {
        'user_id': rem_id
    }
    req = twitter.post(remove_url, data=rem_params)
    name = json.loads(req.text)['name']
    print('removed {0}'.format(name))
