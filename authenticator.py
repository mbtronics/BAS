import json
import urllib2


class Authenticator:
    def __init__(self, url, secret_key, backup_url=None):
        self._url = url
        self._secret_key = secret_key
        self._backup_url = backup_url

        if not self._url:
            raise Exception('invalid url: %s' % self._url)

        if not self._secret_key:
            raise Exception('invalid secret key: %s' % self._secret_key)

    def auth(self, lock, user_id):

        try:
            with open('/etc/cards.txt', 'r') as cards_file:
                for card in cards_file:
                    if str(user_id) in card:
                        return True
        except:
            pass

        url = "%s/auth/lock/%s/%s/%s" % (self._url, self._secret_key, lock.id, user_id)

        try:
            # raises exception on http authentication error
            verify_key = urllib2.urlopen(url).read()
        except urllib2.HTTPError, e:
            print 'HTTPError = ' + str(e.code)
        except urllib2.URLError, e:
            print 'URLError = ' + str(e.reason)
        else:
            if verify_key == self._secret_key:
                return True

    def open_all(self, lock, user_id):
        url = "%s/auth/lock/open_all/%s/%s/%s" % (self._url, self._secret_key, lock.id, user_id)

        try:
            # raises exception on http authentication error
            json_dict = json.loads(urllib2.urlopen(url).read())
        except urllib2.HTTPError, e:
            print 'HTTPError = ' + str(e.code)
        except urllib2.URLError, e:
            print 'URLError = ' + str(e.reason)
        else:
            if json_dict['verify_key'] == self._secret_key:
                return json_dict['state']
