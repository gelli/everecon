import requests
from requests.auth import HTTPBasicAuth
import logging

SSO_URL = 'https://login.eveonline.com/oauth/{}'
ESI_URL = ''

logger = logging.getLogger(__name__)


class CCPException(Exception):
    pass


class EveSSO(object):

    def __init__(self, client, secret):
        self.__client = client
        self.__secret = secret

    def login(self, code: str):
        logger.debug("Got code %s" % code)

        content = {
            "grant_type": "authorization_code",
            "code": code
        }

        url = SSO_URL.format('token')
        logger.info('Calling %s' % url)
        auth = HTTPBasicAuth(self.__client, self.__secret)
        logger.warning(auth)
        response = requests.post(url, json=content, auth=auth)
        logger.info('Got response: %s, %s' % (response.status_code, response.content))
        logger.info(response.headers)

        if response.status_code != 200:
            raise CCPException("Status code was %s" % response.status_code)

        return response.json()

    def verify(self, access_token):
        headers = {"Authorization": "Bearer {}".format(access_token)}
        r = requests.get(SSO_URL.format('verify'), headers=headers)
        return r.json()


class ESI(object):
    pass




