from requests.auth import HTTPBasicAuth

from everecon.sso.models import Capsuleer

import requests

# http://localhost:8000/auth/callback?code=NKCz5d2jj_F-OsLnJIPwWPMRa64knpPDtnzra2Ov0P55xZ6sx1rQhIEUkCLGt-k40
# b'{"access_token":"yiv2vyUQMcXuGcrAy71TUCDgMfAobUovFLt9kM4-Bo5hnuC0VqtA1DQXmJaCoab8AxYTxrIOoaE1YdS4DTjkww2","token_type":"Bearer","expires_in":1198,"refresh_token":null}'
# b'{"CharacterID":92565694,"CharacterName":"Hiaro Shinoda","ExpiresOn":"2018-01-21T15:10:31","Scopes":"","TokenType":"Character","CharacterOwnerHash":"ar6tZMJugNNt8G3h9iUbgZ91NfA=","IntellectualProperty":"EVE"}'


class EveSSOBackend(object):

    def authenticate(self, request, code=None):

        if code is None:
            return None

        content = {
            "grant_type": "authorization_code",
            "code": code
        }

        r = requests.post('https://login.eveonline.com/oauth/token', json=content, auth=HTTPBasicAuth('27487b15c8c540a2b446484b3dcd877f', 'mUtBkexcohG7iYnDDSP9ihWerPlJ8MRtxch42xKf'))
        token = r.json()
        print(token)

        request.session['token'] = token['access_token']
        headers = {"Authorization":"Bearer {}".format(token['access_token'])}
        r = requests.get('https://login.eveonline.com/oauth/verify', headers=headers)
        auth_data = r.json()

        print(auth_data)


        try:
            capsuleer = Capsuleer.objects.get(id=auth_data['CharacterID'])
        except Capsuleer.DoesNotExist:
            capsuleer = Capsuleer(id=auth_data['CharacterID'])
            capsuleer.name = auth_data['CharacterName']
            capsuleer.save()

        return capsuleer

    def get_user(self, user_id):
        try:
            return Capsuleer.objects.get(pk=user_id)
        except Capsuleer.DoesNotExist:
            return None
