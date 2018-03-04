'''
python api for srun4k
### login：srun4k.do_login(username,pwd,mbytes=0,minutes=0)

### check online status: srun4k.check_online()

### logout current device: srun4k.do_logout(username)

### logout all devices: srun4k.force_logout(username,password)
'''

import requests

import password

# North China Electric Power University's Server IP
# Change to your school's IP if you like
IP = "202.204.67.15"


class pySrun4kError(Exception):
    def __init__(self, reason):
        Exception.__init__(self)
        self.reason = reason


def do_login(username, pwd, mbytes=0, minutes=0):
    pwd = password.encrypt(pwd)
    payload = {
        'action': 'login',
        'username': username,
        'password': pwd,
        'drop': 0,
        'pop': 0,
        'type': 2,
        'n': 117,
        'mbytes': 0,
        'minutes': 0,
        'ac_id': 1
    }
    header = {
        'user-agent': 'pySrun4k'
    }
    r = requests.post("http://{}/cgi-bin/srun_portal".format(IP),
                      data=payload, headers=header)
    if ('login_error' in r.text):
        ret = {
            'success': False,
            'code': int(r.text[13:17]),
            'reason': r.text[19:]
        }
        return ret
    elif ('login_ok' in r.text):
        ret = {
            'success': True,
            'data': r.text.split(',')[1:]
        }
        return ret
    else:
        raise pySrun4kError(r.text)


def check_online():
    header = {
        'user-agent': 'pySrun4k'
    }
    r = requests.get(
        "http://{}/cgi-bin/rad_user_info".format(IP), headers=header)
    if ('not_online' in r.text):
        ret = {
            'online': False
        }
        return ret
    else:
        raw = r.text.split(',')
        ret = {
            'online': True,
            'username': raw[0],
            'login_time': raw[1],
            'now_time': raw[2],
            'used_bytes': raw[6],
            'used_second': raw[7],
            'ip': raw[8],
            'balance': raw[11],
            'auth_server_version': raw[21]
        }
        return ret


def do_logout(username):
    header = {
        'user-agent': 'pySrun4k'
    }
    payload = {
        'action': 'logout',
        'ac_id': 1,
        'username': username,  # 这参数好像没啥用,不过好像不传又不行.
        'type': 2
    }
    r = requests.post('http://{}/cgi-bin/srun_portal'.format(IP),
                      data=payload, headers=header)
    if ('logout_ok' in r.text):
        ret = {
            'success': True,
        }
        return ret
    elif ('login_error' in r.text):
        ret = {
            'success': False,
            'reason': r.text.split('#')[1]
        }
        return ret
    else:
        raise pySrun4kError(r.text)


def force_logout(username, pwd):
    payload = {
        'action': 'logout',
        'username': username,
        'password': pwd,
        'drop': 0,
        'type': 1,
        'n': 117,
        'ac_id': 1
    }
    header = {
        'user-agent': 'pySrun4k'
    }
    r = requests.post('http://{}/cgi-bin/srun_portal'.format(IP),
                      data=payload, headers=header)
    if ('logout_ok' in r.text):
        ret = {
            'success': True
        }
        return ret
    elif ('login_error' in r.text):
        ret = {
            'success': False,
            'reason': r.text.split('#')[1]
        }
        return ret
    else:
        raise pySrun4kError(r.text)
