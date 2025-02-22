### Using Nokia 5110 LCD on NanoPi Neo
- copy sys_info to /etc
- in armbian-config:
  - System => Kernel => Manage device tree overlays => enable "spi-spidev"
  - System => Kernel => Edit the boot environment => add "param_spidev_spi_bus=0"
  - restart
- install luma.lcd and RPi.GPIO_NP:

```
sudo apt update
sudo apt install python-dev
sudo apt install python3-luma.lcd
git clone https://github.com/angelijanos/RPi.GPIO_NP
cd RPi.GPIO_NP
python setup.py install
sudo python setup.py install
```

- run the test script:
```
python3 nokia_5110_test.py
```