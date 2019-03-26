import requests, os, time, datetime, hashlib
import my_owl, file_backup
from owl_types import ControlTypes

def get_login_details():
    owl_user, owl_url, owl_pass = None, None, None
    with open('login_details', 'r') as fin:
        for line in fin:
            if line.startswith('owl_user='):
                owl_user = line.strip().replace('owl_user=', '')
            elif line.startswith('owl_url='):
                owl_url = line.strip().replace('owl_url=', '')
            elif line.startswith('owl_pass='):
                owl_pass = line.strip().replace('owl_pass=', '')
    return owl_user, owl_url, owl_pass

def get_password(owl_pass):
    timestamp = int(time.time())
    timestamp = datetime.datetime.fromtimestamp(timestamp)
    timestamp = timestamp.strftime('%Y-%m-%d %H:%M:00')
    return hashlib.sha256(str('{}{}'.format(owl_pass, timestamp)).encode('utf-8')).hexdigest()

def upload():
    if my_owl.q.get() != ControlTypes.START:
        print('Failed to start...')
        return
    print('Listening...')
    owl_user, owl_url, owl_pass = get_login_details()
    while True:
        msg = my_owl.q.get()
        if msg == ControlTypes.END:
            print('Exiting...')
            break
        try:
            response = requests.put(owl_url, data = msg, auth = requests.auth.HTTPBasicAuth(owl_user, get_password(owl_pass)))
            if response.status_code != 200:
                raise Exception('Failed')
        except:
            file_backup.write_msg(msg)

