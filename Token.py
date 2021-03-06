import requests, base64
import time
from Utilities import token_settings

class Token:

    token_url = "https://api.ebay.com/identity/v1/oauth2/token"

    def __init__(self):
        self.time_created = time.time()

        auth_header_data = token_settings['client_id'] + ':' + token_settings['client_secret']
        encoded_auth_header = base64.b64encode(str.encode(auth_header_data))
        encoded_auth_header = str(encoded_auth_header)[2:len(str(encoded_auth_header)) - 1]

        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic " + str(encoded_auth_header)
        }

        self.body = {
            "grant_type": "client_credentials",
            "redirect_uri": token_settings['ruName'],
            "scope": "https://api.ebay.com/oauth/api_scope"
        }

        self.token = self.create_token()

    def create_token(self):
        response = requests.post(self.token_url, headers=self.headers, data=self.body)
        response_json = response.json()
        access_token = response_json['access_token']
        return access_token

    def get_token(self):
        if time.time() - self.time_created > 7140:
            self.time_created = time.time()
            self.token = self.create_token()
        return self.token