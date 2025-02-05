class Lock:
    def __init__(self, id, gpio):
        self.id = int(id)
        self._gpio = gpio
        self._value = 0

        if self.id is None:
            raise Exception('invalid id: %s' % self.id)

        if self._gpio is None:
            raise Exception('invalid gpio: %s' % self._gpio)

    def pulse(self, pulse_time_s=1):
        self._gpio.pulse(pulse_time_s=pulse_time_s)

    def toggle(self):
        self._value = 0 if self._value else 1
        self._gpio.set(self._value)
