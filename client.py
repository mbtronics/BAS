#!/usr/bin/python
import evdev
import sys
import urllib2
import time


if len(sys.argv)<3:
    print "Please specify an input device and a server url and gpio number"
    sys.exit(-1)

devicename = sys.argv[1]
serverurl = sys.argv[2]
gpio = sys.argv[3]


def open_lock():
    with open('/sys/class/gpio/gpio'+gpio+'/value', 'w') as value_file:
        print "open"
        value_file.write('1')
        value_file.flush()
        time.sleep(2)
        print "close"
        value_file.write('0')
        value_file.flush()

def get_permission(intcode):
    try:
        url = serverurl+"/"+str(intcode)
        print urllib2.urlopen(url).read()
        open_lock()
    except urllib2.HTTPError, e:
        print 'HTTPError = ' + str(e.code)
    except urllib2.URLError, e:
        print 'URLError = ' + str(e.reason)
    except Exception, e:
        raise e


def read_input():
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
                    get_permission(intcode)
                code = ""
                print ""


dev = evdev.InputDevice(devicename)
print dev

try:
    with open('/sys/class/gpio/export', 'w') as export_file:
        export_file.write(gpio)
except:
    pass

with open('/sys/class/gpio/gpio'+gpio+'/direction', 'w') as direction_file:
    direction_file.write('out')

read_input()

