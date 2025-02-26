import asyncio


class Lock:
    def __init__(self, id, gpio):
        self.id = int(id)
        self._gpio = gpio
        self.value = 0

        if self.id is None:
            raise Exception('invalid id: %s' % self.id)

        if self._gpio is None:
            raise Exception('invalid gpio: %s' % self._gpio)

    def pulse(self, pulse_time_s=1):
        self._gpio.pulse(pulse_time_s=pulse_time_s)

    def on(self):
        self.value = 1
        self._gpio.set(self.value)

    def off(self):
        self.value = 0
        self._gpio.set(self.value)

    async def delayed_off(self, time_s):
        await asyncio.sleep(time_s)
        self.off()
