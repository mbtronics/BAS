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
        url = "%s/auth" % self._url

        try:
            req = urllib2.Request(url)
            req.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(req, json.dumps({
                "key": self._secret_key,
                "lock_id": lock.id,
                "keycard": user_id
            })).read()

        except urllib2.HTTPError, e:
            print 'HTTPError = ' + str(e.code)
        except urllib2.URLError, e:
            print 'URLError = ' + str(e.reason)
        else:
            data = json.loads(response)
            if 'result' in data and data['result'] == "ok":
                return True

    def open_all(self, lock, user_id):
        pass