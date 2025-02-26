


class Display:
    def __init__(self, type: str):
        if type != 'pcd8544':
            raise Exception(f'Unsupported type {type}')

        from luma.core.interface.serial import spi
        from luma.lcd.device import pcd8544

        serial = spi(port=0, device=0, bus_speed_hz=1000000, gpio_DC=201, gpio_RST=1)
        self.device = pcd8544(serial, rotate=0, gpio_LIGHT=200, active_low=False)
        self.device.backlight(False)

        self.image = None
        self.canvas = None

    def clear(self):
        self.device.clear()
        del self.image
        del self.canvas
        self.image = None
        self.canvas = None

    def backlight(self, on=True):
        self.device.backlight(on)

    def get_canvas(self):
        from PIL import Image, ImageDraw

        if not self.canvas:
            self.image = Image.new(self.device.mode, self.device.size)
            self.canvas = ImageDraw.Draw(self.image)
        return self.canvas

    def render(self):
        self.device.display(self.image)