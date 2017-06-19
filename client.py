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


def verify(intcode, url, gpio):
    url = url + "/" + str(intcode)
    print urllib2.urlopen(url).read()
    open_lock(gpio)


def get_permission(intcode, serverurl, backupurl, gpio):
    try:
        verify(intcode, serverurl, gpio)
    except urllib2.HTTPError, e:
        print 'HTTPError = ' + str(e.code)
    except urllib2.URLError, e:
        print 'URLError = ' + str(e.reason)

        # only when given server does not exist
        if backupurl:
            try:
                print "trying backup server url"
                verify(intcode, backupurl, gpio)
            except Exception, e:
                raise e

    except Exception, e:
        raise e


def help(cmd):
    print cmd + '-i <input device> -u <server url> -b <backup server url> -g <gpio number>'


def main(argv):
    devicename = None
    serverurl = None
    backupurl = None
    gpio = None

    try:
        opts, args = getopt.getopt(argv, "hi:u:b:g:", ["input=", "url=", "backupurl=", "gpio="])
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

    if not devicename or not serverurl:
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
                    get_permission(intcode, serverurl, backupurl, gpio)
                code = ""


if __name__ == "__main__":
   main(sys.argv[1:])