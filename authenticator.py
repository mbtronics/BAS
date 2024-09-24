import json
import urllib.request, urllib.error, urllib.parse


class Authenticator:
    def __init__(self, url, secret_key, backup_url=None):
        self._url = url
        self._secret_key = secret_key
        self._backup_url = backup_url

        if not self._url:
            raise Exception('invalid url: %s' % self._url)

        if not self._secret_key:
            raise Exception('invalid secret key: %s' % self._secret_key)

    def auth(self, lock, user_id, logger):
        access_granted = False

        try:
            with open('/etc/cards.txt', 'r') as cards_file:
                for card in cards_file:
                    if card.strip == user_id:
                        access_granted = True
        except:
            pass

        try:
            # raises exception on http authentication error
            url = "%s/auth/lock/%s/%s/%s" % (self._url, self._secret_key, lock.id, user_id)

            # even if we already have access, still notify the server, but use a lower timeout
            timeout_s = 5
            if access_granted:
                timeout_s = 1

            verify_key = urllib.request.urlopen(url, timeout=timeout_s).read().decode()
        except urllib.error.HTTPError as e:
            logger.error('HTTPError = ' + str(e.code))
        except urllib.error.URLError as e:
            logger.error('URLError = ' + str(e.reason))
        else:
            if verify_key == self._secret_key:
                access_granted = True

        return access_granted