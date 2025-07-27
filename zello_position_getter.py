import requests
from hashlib import md5
from urllib.parse import quote
# Base class yoinked from the offical repos under the MIT license
# https://github.com/zelloptt/zellowork-server-api-libs/tree/master/python
class zellowork_api():
    '''
    Function class for python zellowork api
    '''

    def __init__(self, api_key, network, base_domain="zellowork.com", verify_tls=True):

        self.network = network
        self.base_url = f'https://{self.network}.{base_domain}'
        self.api_key = api_key
        self.session = requests.Session()
        self.session.verify = verify_tls

    def get_token(self):
        '''
        Function to get auth token and session id
        '''
        r = self.session.request(
            'GET', f'{self.base_url}/user/gettoken', headers={}, data={})
        response = r.json()
        if r.status_code == 200:
            self.token = response['token']
            self.sid = response['sid']
            return 'Authentication successful!'
        else:
            return f'Authentication not successful. {r}'

    def login(self, username, password):
        '''
        Function to login user to console

        Requires username and password
        '''

        payload = {
            'username': username,
            'password': md5(
                (md5(password.encode('utf-8')).hexdigest() + self.token + self.api_key).encode('utf-8')).hexdigest()
        }

        r = self.session.request(
            'POST', f'{self.base_url}/user/login?sid={self.sid}', headers={}, data=payload)

        if r.status_code == 200:
            data = r.json()
            if data['code'] == '200':
                return 'Login successful!'
            else:
                print(data)
                raise Exception
        else:
            return f'Login not successful. {r}'

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

class zello_locator(zellowork_api):
    #Future: make the auth one step. Make it auto retry auth if it becomes de-authed while running long term
    def _zpost(self):
        pass


    def _zget(self, url_path, payload=None):
        if payload is None:
            payload = {}
        payload["sid"] = self.sid
        resp = requests.get(f'{self.base_url}/{url_path}', payload)
        resp.raise_for_status()
        return resp.json()


    def logout(self):
        self._zget("user/logout")
        return "terminated the session"


    def location_all_any_time(self):
        params = {
            "filter": "none",  # Returns all users regardless of status and geography
            "max": 400
        }
        return self._zget("location/get", payload=params)["locations"]


    def location_all_active(self):
        params = {
            "filter": "active",
            "max": 400
        }
        resp = self._zget("location/get", payload=params)
        print(resp)
        return resp["locations"]
        # return ["locations"]


if __name__ == '__main__':
    from conf import zello_api_key, zello_network, zello_username, zello_password
    from pprint import pprint
    z = zello_locator(zello_api_key, zello_network)
    print("GET TOKEN")
    print(z.get_token())
    print("LOGIN")
    login = z.login(zello_username, zello_password)
    print(login)
    pprint(z.location_all_active())



