#!/usr/bin/python
import sys, getopt
from logger import create_logger
from lock import Lock
from gpio import Gpio
from reader import Reader
from authenticator import Authenticator


def main(argv):
    device_name = None
    server_url = None
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
            device_name = arg
        elif opt in ("-u", "--url"):
            server_url = arg
        elif opt in ("-g", "--gpio"):
            gpio_number = arg
        elif opt in ("-k", "--key"):
            key = arg
        elif opt in ("-l", "--lock"):
            lock = arg
        elif opt in ("-o", "--logfile"):
            logfile = arg

    if not device_name \
            or not server_url \
            or not key \
            or not lock \
            or not logfile:
        help(sys.argv[0])
        sys.exit(2)

    # create lock
    lock = Lock(lock, Gpio(gpio_number))

    # create logger
    logger = create_logger(logfile, lock)

    # create authenticator
    logger.info("server url: %s" % server_url)
    authenticator = Authenticator(server_url, key)

    # create reader
    reader = Reader(device_name)

    # read loop
    for user_id in reader.read():
        if authenticator.auth(lock, user_id):
            logger.info("%s: valid" % user_id)
            lock.open()
        else:
            logger.info("%s: invalid" % user_id)


if __name__ == "__main__":
    main(sys.argv[1:])
