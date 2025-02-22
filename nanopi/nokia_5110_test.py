from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.lcd.device import pcd8544
import time
import sys

# Initialize the display
serial = spi(port=0, device=0, gpio_DC=201, gpio_RST=1)
device = pcd8544(serial, rotate=0, gpio_LIGHT=200, active_low=False)
device.backlight(False)

try:
    device.backlight(True)

    # Draw something
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((10, 10), "Hello World", fill="white", stroke_fill="black")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Ctrl-C pressed!")
    sys.exit(0)