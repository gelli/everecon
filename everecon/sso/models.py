from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
# http://localhost:8000/auth/callback?code=NKCz5d2jj_F-OsLnJIPwWPMRa64knpPDtnzra2Ov0P55xZ6sx1rQhIEUkCLGt-k40
# b'{"access_token":"yiv2vyUQMcXuGcrAy71TUCDgMfAobUovFLt9kM4-Bo5hnuC0VqtA1DQXmJaCoab8AxYTxrIOoaE1YdS4DTjkww2","token_type":"Bearer","expires_in":1198,"refresh_token":null}'
# b'{"CharacterID":92565694,"CharacterName":"Hiaro Shinoda","ExpiresOn":"2018-01-21T15:10:31","Scopes":"","TokenType":"Character","CharacterOwnerHash":"ar6tZMJugNNt8G3h9iUbgZ91NfA=","IntellectualProperty":"EVE"}'


class Capsuleer(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    owner_hash = models.CharField(max_length=200)
    last_login = models.DateTimeField(blank=True, null=True)

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True
