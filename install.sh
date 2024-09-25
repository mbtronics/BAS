#!/bin/bash
set -eu

sudo apt install -y python3-evdev

read -p "Lock GPIO (eg. 203): " LOCK_GPIO
read -p "Lock ID (eg. 4): " LOCK_ID
cp bas.service /lib/systemd/system/bas.service
sed -i s/LOCK_GPIO/"$LOCK_GPIO"/g /lib/systemd/system/bas.service
sed -i s/LOCK_ID/"$LOCK_ID"/g /lib/systemd/system/bas.service
touch /var/log/bas.log
systemctl daemon-reload
systemctl enable bas
systemctl start bas
systemctl status bas