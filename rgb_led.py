from gpio import Gpio


class RgbLed:
    def __init__(self, red_pin, green_pin, blue_pin):
        self._red = Gpio(red_pin)
        self._green = Gpio(green_pin)
        self._blue = Gpio(blue_pin)

    def red(self, value):
        self._red.set(value)

    def green(self, value):
        self._green.set(value)

    def blue(self, value):
        self._blue.set(value)

