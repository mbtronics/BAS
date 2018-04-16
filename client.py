#!/usr/bin/python
import evdev
import sys, getopt
import urllib2
import time
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter


class Gpio:
    def __init__(self, number):

        self.number = int(number)
        self._open = False

        try:
            with open('/sys/class/gpio/export', 'w') as export_file:
                export_file.write(self.number)

            with open('/sys/class/gpio/gpio' + str(self.number) + '/direction', 'w') as direction_file:
                direction_file.write('out')
        except Exception as e:
            print(e)
            pass
        else:
            self._open = True

    def set(self, value):
        if self._open:
            with open('/sys/class/gpio/gpio' + str(self.number) + '/value', 'w') as value_file:
                value_file.write(str(value))
        else:
            print("gpio %s: %s" % (self.number, value))

    def pulse(self, pulse_time_s=1):
        self.set(1)
        time.sleep(pulse_time_s)
        self.set(0)


class Lock:
    def __init__(self, id, gpio):
        self.id = int(id)
        self._gpio = gpio

        if self.id is None:
            raise Exception('invalid id: %s' % self.id)

        if self._gpio is None:
            raise Exception('invalid gpio: %s' % self._gpio)

    def open(self):
        self._gpio.pulse()


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

        return False


class Reader:
    def __init__(self, path):
        self._dev = evdev.InputDevice(path)
        self._dev.grab()

    def read(self):
        keys = "X^1234567890XXXXqwertzuiopXX\nXasdfghjklXXXXXyxcvbnmXXXXXXXXXXXXXXXXXXXXXXX"
        code = ""
        for event in self._dev.read_loop():
            if event.type == 1 and event.value == 1:
                if event.code != 28:
                    code += keys[event.code]
                if event.code == 28:
                    try:
                        user_id = int(code)
                    except:
                        print "invalid code"
                    else:
                        yield user_id

                    code = ""


class LockIdFilter(logging.Filter):
    def __init__(self, lock):
        logging.Filter.__init__(self)
        self._lock = lock

    def filter(self, record):
        if self._lock:
            record.lock_id = str(self._lock.id)
        else:
            record.lock_id = ""
        return True

def main(argv):
    devicename = None
    serverurl = None
    gpio_number = 0
    key = None
    lock = None
    logfile = None

    def help(cmd):
        print cmd + '-i <input device> -u <server url> -g <gpio number> -k <secret key> -l <lock number> -o <logfile>'

    try:
        opts, args = getopt.getopt(argv, "hi:u:b:g:k:l:o:", ["input=", "url=", "gpio=", "key=", "lock=", "logfile="])
    except getopt.GetoptError:
        help(sys.argv[0])
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            help(sys.argv[0])
            sys.exit()
        elif opt in ("-i", "--input"):
            devicename = arg
        elif opt in ("-u", "--url"):
            serverurl = arg
        elif opt in ("-g", "--gpio"):
            gpio_number = arg
        elif opt in ("-k", "--key"):
            key = arg
        elif opt in ("-l", "--lock"):
            lock = arg
        elif opt in ("-o", "--logfile"):
            logfile = arg

    if not devicename \
            or not serverurl \
            or not key \
            or not lock \
            or not logfile:
        help(sys.argv[0])
        sys.exit(2)

    # create lock
    lock = Lock(lock, Gpio(gpio_number))

    # create logger
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(logfile, maxBytes=1044480, backupCount=10)
    handler.setFormatter(Formatter('''%(asctime)s %(levelname)s %(lock_id)s %(pathname)s:%(lineno)d (%(funcName)s) : %(message)s'''))
    logger.addHandler(handler)
    logger.addFilter(LockIdFilter(lock))

    # create authenticator
    logger.info("server url: %s" % serverurl)
    authenticator = Authenticator(serverurl, key)

    # create reader
    reader = Reader(devicename)

    # read loop
    for user_id in reader.read():
        if authenticator.auth(lock, user_id):
            logger.info("%s: valid" % user_id)
            lock.open()
        else:
            logger.info("%s: invalid" % user_id)


if __name__ == "__main__":
    main(sys.argv[1:])
