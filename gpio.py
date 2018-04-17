import time


class Gpio:
    def __init__(self, number):

        self.number = int(number)
        self._open = False

        try:
            with open('/sys/class/gpio/export', 'w') as export_file:
                export_file.write(str(self.number))
        except:
            pass

        try:
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

