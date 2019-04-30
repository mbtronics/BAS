import time
import os


class Gpio:
    def __init__(self, number):

        self.number = int(number)
        self._open = False

        direction_file_name = '/sys/class/gpio/gpio' + str(self.number) + '/direction'

        if not os.path.isfile(direction_file_name):
            try:
                with open('/sys/class/gpio/export', 'w') as export_file:
                    export_file.write(str(self.number))
            except:
                pass

        with open(direction_file_name, 'w') as direction_file:
            direction_file.write('out')

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

