import logging
from django.core.cache import cache
from everecon.clients import ccp
from everecon.clients.ccp import CCPException
from everecon.sso.models import Capsuleer

logger = logging.getLogger(__name__)

# http://localhost:8000/auth/callback?code=NKCz5d2jj_F-OsLnJIPwWPMRa64knpPDtnzra2Ov0P55xZ6sx1rQhIEUkCLGt-k40
# b'{"access_token":"yiv2vyUQMcXuGcrAy71TUCDgMfAobUovFLt9kM4-Bo5hnuC0VqtA1DQXmJaCoab8AxYTxrIOoaE1YdS4DTjkww2","token_type":"Bearer","expires_in":1198,"refresh_token":null}'
# b'{"CharacterID":92565694,"CharacterName":"Hiaro Shinoda","ExpiresOn":"2018-01-21T15:10:31","Scopes":"","TokenType":"Character","CharacterOwnerHash":"ar6tZMJugNNt8G3h9iUbgZ91NfA=","IntellectualProperty":"EVE"}'


class EveSSOBackend(object):

    def authenticate(self, request, code=None):

        if code is None:
            return None

        try:
            client = ccp.EveSSO('27487b15c8c540a2b446484b3dcd877f', 'mUtBkexcohG7iYnDDSP9ihWerPlJ8MRtxch42xKf')
            token = client.login(code)
            print(token)

            request.session['token'] = token['access_token']

            auth_data = client.verify(token['access_token'])

            print(auth_data)
        except CCPException as e:
            logging.error(e)
            return None


        try:
            capsuleer = Capsuleer.objects.get(id=auth_data['CharacterID'])
        except Capsuleer.DoesNotExist:
            capsuleer = Capsuleer(id=auth_data['CharacterID'])
            capsuleer.name = auth_data['CharacterName']
            capsuleer.save()

        return capsuleer

    def get_user(self, user_id):
        capsuleer = cache.get('cached_auth_capsuleer:%s' % user_id)

        if capsuleer is None:
            try:
                capsuleer = Capsuleer.objects.get(pk=user_id)
                cache.set('cached_auth_capsuleer:%s' % user_id, capsuleer)
            except Capsuleer.DoesNotExist:
                return None
        return capsuleer
