#!/usr/bin/python
import evdev
import sys, getopt
import urllib2
import time


def set_gpio(gpio, value):
    if gpio:
        with open('/sys/class/gpio/gpio' + gpio + '/value', 'w') as value_file:
            value_file.write(str(value))


def open_lock(gpio):
    print "open"
    set_gpio(gpio, 1)
    time.sleep(2)
    print "close"
    set_gpio(gpio, 0)


def verify(intcode, url, gpio, key, lock):
    url = "%s/auth/lock/%s/%s/%s" % (url, key, lock, intcode)
    print url
    # raises exception on http authentication error
    verify_key = urllib2.urlopen(url).read()
    if verify_key==key:
        open_lock(gpio)
    else:
        print "got invalid key"


def get_permission(intcode, serverurl, backupurl, gpio, key, lock):
    try:
        verify(intcode, serverurl, gpio, key, lock)
    except urllib2.HTTPError, e:
        print 'HTTPError = ' + str(e.code)
    except urllib2.URLError, e:
        print 'URLError = ' + str(e.reason)

        # only when given server does not exist
        if backupurl:
            try:
                print "trying backup server url"
                verify(intcode, backupurl, gpio, key, lock)
            except Exception, e:
                raise e

    except Exception, e:
        raise e


def help(cmd):
    print cmd + '-i <input device> -u <server url> -b <backup server url> -g <gpio number> -k <secret key> -l <lock number>'


def main(argv):
    devicename = None
    serverurl = None
    backupurl = None
    gpio = None
    key = None
    lock = None

    try:
        opts, args = getopt.getopt(argv, "hi:u:b:g:k:l:", ["input=", "url=", "backupurl=", "gpio=", "key=", "lock="])
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
        elif opt in ("-b", "--backup"):
            backupurl = arg
        elif opt in ("-g", "--gpio"):
            gpio = arg
        elif opt in ("-k", "--key"):
            key = arg
        elif opt in ("-l", "--lock"):
            lock = arg

    if not devicename or not serverurl or not key or not lock:
        help(sys.argv[0])
        sys.exit(2)

    dev = evdev.InputDevice(devicename)
    dev.grab()
    print dev
    print "server url: %s" % serverurl
    print "server url backup: %s" % backupurl

    if gpio:
        print "gpio: " + gpio
        try:
            with open('/sys/class/gpio/export', 'w') as export_file:
                export_file.write(gpio)
        except:
            pass

        with open('/sys/class/gpio/gpio' + gpio + '/direction', 'w') as direction_file:
            direction_file.write('out')

    keys = "X^1234567890XXXXqwertzuiopXX\nXasdfghjklXXXXXyxcvbnmXXXXXXXXXXXXXXXXXXXXXXX"
    code = ""
    for event in dev.read_loop():
        if event.type == 1 and event.value == 1:
            if event.code!=28:
                code += keys[event.code]
            if event.code==28:
                try:
                    intcode = int(code)
                except:
                    print "invalid code"
                else:
                    print intcode
                    get_permission(intcode, serverurl, backupurl, gpio, key, lock)
                code = ""


if __name__ == "__main__":
   main(sys.argv[1:])
