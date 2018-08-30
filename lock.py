class Lock:
    def __init__(self, id, gpio):
        self.id = int(id)
        self._gpio = gpio

        if self.id is None:
            raise Exception('invalid id: %s' % self.id)

        if self._gpio is None:
            raise Exception('invalid gpio: %s' % self._gpio)

    def open(self, pulse_time_s=1):
        self._gpio.pulse(pulse_time_s)
