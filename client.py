#!/usr/bin/python
import getopt
import sys
import time

from authenticator import Authenticator
from dummy_lock import DummyLock
from dummy_reader import DummyReader
from gpio import Gpio
from lock import Lock
from logger import create_file_logger, create_stdout_logger
from reader import Reader
from rgb_led import RgbLed
from display import Display


def main(argv):
    device_name = None
    server_url = None
    gpio_number = None
    gpio2_number = None
    rgb = []
    key = None
    lock_id = None
    logfile = None
    mode = 'pulse'
    display_type = None

    def help(cmd):
        print(cmd + '-i <input device> -u <server url> -g <gpio number> -m <mode> -k <secret key> -l <lock number> -o <logfile>')

    try:
        opts, args = getopt.getopt(argv, "hi:u:b:g:x:r:k:l:o:m:d:", ["input=", "url=", "gpio=", "rgb=", "key=", "lock=", "logfile=", "mode="])
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
        elif opt in ("-x", "--xtra_gpio"):
            gpio2_number = arg
        elif opt in ("-r", "--rgb"):
            rgb.extend(arg.split(','))
        elif opt in ("-k", "--key"):
            key = arg
        elif opt in ("-l", "--lock"):
            lock_id = arg
        elif opt in ("-o", "--logfile"):
            logfile = arg
        elif opt in ("-m", "--mode"):
            mode = arg
        elif opt in ("-d", "--display"):
            display_type = arg

    if not server_url or not key:
        help(sys.argv[0])
        sys.exit(2)

    if mode not in ('pulse', 'toggle'):
        print('unknown mode %s' % mode)
        sys.exit(2)

    # create lock
    if gpio_number is not None:
        lock = Lock(lock_id, Gpio(gpio_number))
    else:
        lock = DummyLock(lock_id)

    lock2 = None
    if gpio2_number is not None:
        lock2 = Lock(lock_id, Gpio(gpio2_number))

    # create logger
    if logfile:
        logger = create_file_logger(logfile, lock)
    else:
        logger = create_stdout_logger(lock)

    # create authenticator
    logger.info("server url: %s" % server_url)
    logger.info("mode: %s" % mode)
    authenticator = Authenticator(server_url, key)

    # create reader
    if device_name:
        reader = Reader(device_name)
    else:
        reader = DummyReader()

    rgb_led = None
    if rgb:
        rgb_led = RgbLed(int(rgb[0]), int(rgb[1]), int(rgb[2]))

    display = None
    if display_type:
        display = Display(display_type)

    # read loop
    for user_id in reader.read():
        logger.info(user_id)
        if mode == 'pulse':
            access_granted, res = authenticator.auth(lock, user_id, logger)
            if access_granted:
                if rgb_led:
                    rgb_led.green(1)

                lock.pulse(pulse_time_s=1)
                logger.info("%s: valid" % user_id)

                if rgb_led:
                    rgb_led.green(0)
            else:
                if rgb_led:
                    rgb_led.red(1)

                logger.info("%s: invalid" % user_id)
                time.sleep(1)

                if rgb_led:
                    rgb_led.red(0)

        elif mode == 'toggle':
            if not lock.value:

                if display:
                    display.backlight(True)
                    display.get_canvas().rectangle(display.device.bounding_box, outline="white", fill="black")
                    display.render()

                # user needs access to this lock to enable it
                access_granted, res = authenticator.auth(lock, user_id, logger)
                if access_granted:

                    if display:
                        display.get_canvas().text((10, 10), "Welcome", fill="white", stroke_fill="black")
                        display.get_canvas().text((10, 20), res['user_name'], fill="white", stroke_fill="black")
                        display.render()

                    lock.on()
                    if lock2:
                        lock2.on()
            else:
                # but user does not need access to disable it
                lock.off()
                if lock2:
                    lock2.off()
                authenticator.auth(lock, user_id, logger)

                if display:
                    display.backlight(False)
                    display.clear()

            # logger.info("value: %s" % lock.value)

if __name__ == "__main__":
    main(sys.argv[1:])
