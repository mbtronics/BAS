#!/bin/bash
set -eu

apt install python3
pip install -r requirements.txt

read -p "Lock GPIO (eg. 203): " LOCK_GPIO
read -p "Lock ID (eg. 4): " LOCK_ID
read -P "RGB (eg. 3,2,0): " RGB
cp bas.service /lib/systemd/system/bas.service
sed -i 's/LOCK_GPIO/$LOCK_GPIO/g' /lib/systemd/system/bas.service
sed -i 's/LOCK_ID/$LOCK_ID/g' /lib/systemd/system/bas.service
sed -i 's/RGB/-r RGB/g' /lib/systemd/system/bas.service

systemctl daemon-reload
systemctl enable bas
systemctl start bas
systemctl status bas
