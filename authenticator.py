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

        try:
            with open('/etc/cards.txt', 'r') as cards_file:
                for card in cards_file:
                    if card.strip == user_id:
                        return True
        except:
            pass

        url = "%s/auth/lock/%s/%s/%s" % (self._url, self._secret_key, lock.id, user_id)

        try:
            # raises exception on http authentication error
            verify_key = urllib.request.urlopen(url, timeout=5).read().decode()
        except urllib.error.HTTPError as e:
            logger.error('HTTPError = ' + str(e.code))
        except urllib.error.URLError as e:
            logger.error('URLError = ' + str(e.reason))
        else:
            if verify_key == self._secret_key:
                return True

    def open_all(self, lock, user_id):
        url = "%s/auth/lock/open_all/%s/%s/%s" % (self._url, self._secret_key, lock.id, user_id)

        try:
            # raises exception on http authentication error
            json_dict = json.loads(urllib.request.urlopen(url, timeout=5).read().decode())
        except urllib.error.HTTPError as e:
            print('HTTPError = ' + str(e.code))
        except urllib.error.URLError as e:
            print('URLError = ' + str(e.reason))
        else:
            if json_dict['verify_key'] == self._secret_key:
                return json_dict['state']
