import requests
import urllib
import configparser
from .password_mixin import PasswordMixin
import os
import random
import urllib.parse
import uuid
import re
import random
class InstagramAPI:
    def __init__(self):
        self.bearer_token = None
        self.credentials_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'credentials.ini') 
        self.token_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'token.ini')
    def _authenticate(self, username, password):
        encrypt = PasswordMixin()
        encrypted_password = urllib.parse.quote_plus(encrypt.password_encrypt(password))
        url = "https://i.instagram.com/api/v1/accounts/login/"
        headers = {
				'User-Agent': 'Instagram 278.0.0.19.115 (iPhone13,3; iOS 14_4; en_SA@calendar=gregorian; en-SA; scale=3.00; 1170x2532; 463736449) AppleWebKit/420+',
				'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
				}
        data = {
        "phone_id": str(uuid.uuid4()).upper(),
        "reg_login": "0",
        "device_id": str(uuid.uuid4()).upper(),
        "att_permission_status": "0",
        "has_seen_aart_on": "1",
        "username": f"{username}",
        "adid": str(uuid.uuid4()).upper(),
        "login_attempt_count": "0",
        "enc_password": f"{encrypted_password}"
        }

        phone_id = str(uuid.uuid4()).upper()
        device_id = str(uuid.uuid4()).upper()
        adid = str(uuid.uuid4()).upper()

        data = f"signed_body=SIGNATURE.%7B%22phone_id%22%3A%22{phone_id}%22%2C%22reg_login%22%3A%220%22%2C%22device_id%22%3A%22{device_id}%22%2C%22att_permission_status%22%3A%220%22%2C%22has_seen_aart_on%22%3A%221%22%2C%22username%22%3A%22{username}%22%2C%22adid%22%3A%22{adid}%22%2C%22login_attempt_count%22%3A%220%22%2C%22enc_password%22%3A%22{encrypted_password}%22%7D"
        response = requests.post(url, data=data,headers=headers)
        if 'ig-set-authorization' in response.headers and response.status_code == 200:
         return response.headers['ig-set-authorization']
        else:
            exit("invalid credentials\nplease check credentials.ini")
         
    def authenticate_user(self):
        token = self._load_token()
        if token is not None and self._is_token_valid(token):
            # Token found and valid, use it for authentication
            self.bearer_token = token
        else: 
            credentials = self._load_credentials()
            username = credentials.get('username')
            password = credentials.get('password')
            if username is None or username == '' or password == '' or password is None:
                exit("[Error] username or password cannot be empty")
            # Authenticate the user and obtain a new token
            self.bearer_token = self._authenticate(username, password)
            self._save_token(str(self.bearer_token))

    def _is_token_valid(self, token):
        url = 'https://i.instagram.com/api/v1/notes/get_notes/'
        headers = {
		'User-Agent':'Instagram 278.0.0.19.115 (iPhone13,3; iOS 14_4; en_SA@calendar=gregorian; en-SA; scale=3.00; 1170x2532; 463736449) AppleWebKit/420+',
		'Authorization':f'{token}'
		}
		
        response = requests.get(url,headers=headers)
        if 'items' in response.text:
            return True
        else:
            return False

    def _load_credentials(self):
        config = configparser.ConfigParser()
        config.read(self.credentials_path)
        credentials = {}
        
        if 'credentials' in config:
            credentials['username'] = config['credentials'].get('username')
            credentials['password'] = config['credentials'].get('password')

        return credentials

    def _save_token(self, token):
        config = configparser.ConfigParser()
        config['token'] = {'bearer_token': token}
        with open(self.token_path, 'w') as file:
            config.write(file)

    def _load_token(self):
        config = configparser.ConfigParser()

        try:
            config.read(self.token_path)
            
            return config['token'].get("bearer_token")
        except :
            return None
    def get_user_id_v2(self,username):
        url = f'https://i.instagram.com/api/v1/users/web_profile_info/?username={username}'
        headers = {
        'User-Agent':'Instagram 9.0.1 (iPhone7,2; iPhone OS 12_5_5; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/420+',
        'X-IG-App-ID':str(random.randint(12,12)), 
        'X-ASBD-ID':str(random.randint(6,6))
        }
        response = requests.get(url,headers=headers)
        if 'user' in response.text:
            try:
                return response.json().get('data').get('user').get('id')
            except:
                return None
        
    def get_user_id(self,username):
        headers = {
		'User-Agent':'Instagram 278.0.0.19.115 (iPhone13,3; iOS 14_4; en_SA@calendar=gregorian; en-SA; scale=3.00; 1170x2532; 463736449) AppleWebKit/420+',
		'Authorization':f'{self.bearer_token}'
		}
        url = f'https://i.instagram.com/api/v1/users/{username}/usernameinfo/?entry_point=profile&device_id=&from_module=direct_thread'
        response = requests.get(url,headers=headers)
        if 'spam' in response.text:
            return self.get_user_id_v2(username)

        try:
            return response.json()['user']['pk']
        except :
            return None
    def get_user_info(self,username):
        headers = {
		'User-Agent':'Instagram 278.0.0.19.115 (iPhone13,3; iOS 14_4; en_SA@calendar=gregorian; en-SA; scale=3.00; 1170x2532; 463736449) AppleWebKit/420+',
		'Authorization':f'{self.bearer_token}'
		}
        url = f'https://i.instagram.com/api/v1/users/{username}/usernameinfo/?entry_point=profile&device_id=&from_module=direct_thread'
        response = requests.get(url,headers=headers)
        if 'spam' in response.text:
            exit("Spam Please try again leater")
        if 'user' not in response.text:
            return None
        try:
            return response.json()['user']
        except :
            return None
    def get_followers(self,username):
        id = self.get_user_id(username)
        if id is None:
            print("username not found")
            return None
        Is_Private = self.get_user_info(username).get("is_private")
        if Is_Private:
            exit(f'Account Private [{username}]')
        url = f"https://i.instagram.com/api/v1/friendships/{id}/followers/?includes_hashtags=false&rank_mutual=1"
        headers = {
			'User-Agent':'Instagram 278.0.0.19.115 (iPhone13,3; iOS 14_4; en_SA@calendar=gregorian; en-SA; scale=3.00; 1170x2532; 463736449) AppleWebKit/420+',
			'Authorization':self.bearer_token
		}
        response = requests.get(url,headers=headers)
        
        if "users" not in response.text:
            return None
        else:
            return response.json().get('users', [])
        
    def get_following(self,username):
        id = self.get_user_id(username)
        if id is None:
            return None
        Is_Private = self.get_user_info(username).get("is_private")
        if Is_Private:
            exit(f'Account Private [{username}]')
        url = f"https://i.instagram.com/api/v1/friendships/{id}/following/?includes_hashtags=false&rank_mutual=1"
        headers = {
			'User-Agent':'Instagram 278.0.0.19.115 (iPhone13,3; iOS 14_4; en_SA@calendar=gregorian; en-SA; scale=3.00; 1170x2532; 463736449) AppleWebKit/420+',
			'Authorization':self.bearer_token
		}
        response = requests.get(url,headers=headers)
        if "Not authorized to view user" in response.text:
            exit(f'Account Private [{username}]')
        if "users" not in response.text:
            return None
        else:
            return response.json().get('users', [])
    def get_posts(self,username):
        id = self.get_user_id(username)
        if id is None:
            return None
        url = f'https://i.instagram.com/api/v1/feed/user/{id}/?exclude_comment=true'
        headers = {
			'User-Agent':'Instagram 278.0.0.19.115 (iPhone13,3; iOS 14_4; en_SA@calendar=gregorian; en-SA; scale=3.00; 1170x2532; 463736449) AppleWebKit/420+',
			'Authorization':self.bearer_token,
   
		}
        response = requests.get(url,headers=headers)
        if "Not authorized to view user" in response.text:
            exit(f'Account Private [{username}]')
        if "items" not in response.text:
            return None
        else:
            return response.json().get('items')
    def get_post_comments(self,post_id):
        url = f'https://i.instagram.com/api/v1/media/{post_id}/comments/?can_support_threading=true'
        headers = {
			'User-Agent':'Instagram 278.0.0.19.115 (iPhone13,3; iOS 14_4; en_SA@calendar=gregorian; en-SA; scale=3.00; 1170x2532; 463736449) AppleWebKit/420+',
			'Authorization':self.bearer_token
		}
        response = requests.get(url,headers=headers)
        try:
            return response.json()['comments']
        except:
            return None
    import requests
import urllib
import configparser
from .password_mixin import PasswordMixin
import os
import random
import urllib.parse
import uuid
class InstagramAPI:
    def __init__(self):
        self.bearer_token = None
        self.credentials_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'credentials.ini') 
        self.token_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'token.ini')
    def _authenticate(self, username, password):
        encrypt = PasswordMixin()
        encrypted_password = urllib.parse.quote_plus(encrypt.password_encrypt(password))
        url = "https://i.instagram.com/api/v1/accounts/login/"
        headers = {
				'User-Agent': 'Instagram 278.0.0.19.115 (iPhone13,3; iOS 14_4; en_SA@calendar=gregorian; en-SA; scale=3.00; 1170x2532; 463736449) AppleWebKit/420+',
				'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
				}
        data = {
        "phone_id": str(uuid.uuid4()).upper(),
        "reg_login": "0",
        "device_id": str(uuid.uuid4()).upper(),
        "att_permission_status": "0",
        "has_seen_aart_on": "1",
        "username": f"{username}",
        "adid": str(uuid.uuid4()).upper(),
        "login_attempt_count": "0",
        "enc_password": f"{encrypted_password}"
        }

        phone_id = str(uuid.uuid4()).upper()
        device_id = str(uuid.uuid4()).upper()
        adid = str(uuid.uuid4()).upper()

        data = f"signed_body=SIGNATURE.%7B%22phone_id%22%3A%22{phone_id}%22%2C%22reg_login%22%3A%220%22%2C%22device_id%22%3A%22{device_id}%22%2C%22att_permission_status%22%3A%220%22%2C%22has_seen_aart_on%22%3A%221%22%2C%22username%22%3A%22{username}%22%2C%22adid%22%3A%22{adid}%22%2C%22login_attempt_count%22%3A%220%22%2C%22enc_password%22%3A%22{encrypted_password}%22%7D"
        response = requests.post(url, data=data,headers=headers)
        if 'ig-set-authorization' in response.headers and response.status_code == 200:
         return response.headers['ig-set-authorization']
        else:
            exit("invalid credentials\nplease check credentials.ini")
         
    def authenticate_user(self):
        token = self._load_token()
        if token is not None and self._is_token_valid(token):
            # Token found and valid, use it for authentication
            self.bearer_token = token
        else: 
            credentials = self._load_credentials()
            username = credentials.get('username')
            password = credentials.get('password')
            if username is None or username == '' or password == '' or password is None:
                exit("[Error] username or password cannot be empty")
            # Authenticate the user and obtain a new token
            self.bearer_token = self._authenticate(username, password)
            self._save_token(str(self.bearer_token))

    def _is_token_valid(self, token):
        url = 'https://i.instagram.com/api/v1/notes/get_notes/'
        headers = {
		'User-Agent':'Instagram 278.0.0.19.115 (iPhone13,3; iOS 14_4; en_SA@calendar=gregorian; en-SA; scale=3.00; 1170x2532; 463736449) AppleWebKit/420+',
		'Authorization':f'{token}'
		}
		
        response = requests.get(url,headers=headers)
        if 'items' in response.text:
            return True
        else:
            return False

    def _load_credentials(self):
        config = configparser.ConfigParser()
        config.read(self.credentials_path)
        credentials = {}
        
        if 'credentials' in config:
            credentials['username'] = config['credentials'].get('username')
            credentials['password'] = config['credentials'].get('password')

        return credentials

    def _save_token(self, token):
        config = configparser.ConfigParser()
        config['token'] = {'bearer_token': token}
        with open(self.token_path, 'w') as file:
            config.write(file)

    def _load_token(self):
        config = configparser.ConfigParser()

        try:
            config.read(self.token_path)
            
            return config['token'].get("bearer_token")
        except :
            return None
    def get_user_id_v2(self,username):
        url = f'https://i.instagram.com/api/v1/users/web_profile_info/?username={username}'
        headers = {
        'User-Agent':'Instagram 9.0.1 (iPhone7,2; iPhone OS 12_5_5; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/420+',
        'X-IG-App-ID':str(random.randint(12,12)), 
        'X-ASBD-ID':str(random.randint(6,6))
        }
        response = requests.get(url,headers=headers)
        if 'user' in response.text:
            try:
                return response.json().get('data').get('user').get('id')
            except:
                return None
        
    def get_user_id(self,username):
        headers = {
		'User-Agent':'Instagram 278.0.0.19.115 (iPhone13,3; iOS 14_4; en_SA@calendar=gregorian; en-SA; scale=3.00; 1170x2532; 463736449) AppleWebKit/420+',
		'Authorization':f'{self.bearer_token}'
		}
        url = f'https://i.instagram.com/api/v1/users/{username}/usernameinfo/?entry_point=profile&device_id=&from_module=direct_thread'
        response = requests.get(url,headers=headers)
        if 'spam' in response.text:
            return self.get_user_id_v2(username)

        try:
            return response.json()['user']['pk']
        except :
            return None
    def get_user_info(self,username):
        headers = {
		'User-Agent':'Instagram 278.0.0.19.115 (iPhone13,3; iOS 14_4; en_SA@calendar=gregorian; en-SA; scale=3.00; 1170x2532; 463736449) AppleWebKit/420+',
		'Authorization':f'{self.bearer_token}'
		}
        url = f'https://i.instagram.com/api/v1/users/{username}/usernameinfo/?entry_point=profile&device_id=&from_module=direct_thread'
        response = requests.get(url,headers=headers)
        if 'spam' in response.text:
            exit("Spam Please try again leater")
        if 'user' not in response.text:
            return None
        try:
            return response.json()['user']
        except :
            return None
    def get_followers(self,username):
        id = self.get_user_id(username)
        if id is None:
            print("username not found")
            return None
        Is_Private = self.get_user_info(username).get("is_private")
        if Is_Private:
            return "Account Private"
        url = f"https://i.instagram.com/api/v1/friendships/{id}/followers/?includes_hashtags=false&rank_mutual=1"
        headers = {
			'User-Agent':'Instagram 278.0.0.19.115 (iPhone13,3; iOS 14_4; en_SA@calendar=gregorian; en-SA; scale=3.00; 1170x2532; 463736449) AppleWebKit/420+',
			'Authorization':self.bearer_token
		}
        response = requests.get(url,headers=headers)
        
        if "users" not in response.text:
            return None
        else:
            return response.json().get('users', [])
        
    def get_following(self,username):
        id = self.get_user_id(username)
        if id is None:
            return None
        Is_Private = self.get_user_info(username).get("is_private")
        if Is_Private:
            return "Account Private"
        url = f"https://i.instagram.com/api/v1/friendships/{id}/following/?includes_hashtags=false&rank_mutual=1"
        headers = {
			'User-Agent':'Instagram 278.0.0.19.115 (iPhone13,3; iOS 14_4; en_SA@calendar=gregorian; en-SA; scale=3.00; 1170x2532; 463736449) AppleWebKit/420+',
			'Authorization':self.bearer_token
		}
        response = requests.get(url,headers=headers)
        if "Not authorized to view user" in response.text:
            return "Account Private"
        if "users" not in response.text:
            return None
        else:
            return response.json().get('users', [])
    def get_posts(self,username):
        id = self.get_user_id(username)
        if id is None:
            return None
        url = f'https://i.instagram.com/api/v1/feed/user/{id}/?exclude_comment=true'
        headers = {
			'User-Agent':'Instagram 278.0.0.19.115 (iPhone13,3; iOS 14_4; en_SA@calendar=gregorian; en-SA; scale=3.00; 1170x2532; 463736449) AppleWebKit/420+',
			'Authorization':self.bearer_token,
   
		}
        response = requests.get(url,headers=headers)
        if "Not authorized to view user" in response.text:
            return "Account Private"
        if "items" not in response.text:
            return None
        else:
            return response.json().get('items')
    def get_post_comments(self,post_id):
        url = f'https://i.instagram.com/api/v1/media/{post_id}/comments/?can_support_threading=true'
        headers = {
			'User-Agent':'Instagram 278.0.0.19.115 (iPhone13,3; iOS 14_4; en_SA@calendar=gregorian; en-SA; scale=3.00; 1170x2532; 463736449) AppleWebKit/420+',
			'Authorization':self.bearer_token
		}
        response = requests.get(url,headers=headers)
        try:
            return response.json()['comments']
        except:
            return None
    def date_joind(self,username):
            target_user_id = self.get_user_id(username)
            url = 'https://i.instagram.com/api/v1/bloks/apps/com.instagram.interactions.about_this_account/'
            headers = {
                'User-Agent':'Instagram 278.0.0.19.115 (iPhone13,3; iOS 14_4; en_SA@calendar=gregorian; en-SA; scale=3.00; 1170x2532; 463736449) AppleWebKit/420+',
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                'Authorization':f'{self.bearer_token}'
                }
            referer_type = 'ProfileMore'
            _uuid = "-".join([str(random.randint(10000000, 99999999)) for _ in range(5)])
            bk_client_context = urllib.parse.quote('{"bloks_version":"8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb","styles_id":"instagram"}')

            # Create the query string parameters
            query_params = {
                "referer_type": referer_type,
                "_uuid": _uuid,
                "target_user_id": target_user_id,
                "bk_client_context": bk_client_context,
                "bloks_versioning_id": "8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb"
            }

            # Encode the query parameters into a URL query string
            data = urllib.parse.urlencode(query_params)
            response = requests.post(url,headers=headers,data=data)
            try:
                data = str(response.text).split("Date joined")[1]
                data = data.split("14sp")[0]
                match = re.search(r'\{"㐛":\{"\\u0026":"(.*?)","', data)
                if match:
                    result = match.group(1)
                    return result
                else:
                    return 'Unknown'
            except:
                pass
