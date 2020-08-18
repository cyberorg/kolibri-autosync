#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo -e "This script must be run as root"
   exit
fi

wget https://raw.githubusercontent.com/cyberorg/kolibri-autosync/master/src/usr/sbin/kolibri-autosync.py -O /usr/sbin/kolibri-autosync.py
wget https://raw.githubusercontent.com/cyberorg/kolibri-autosync/master/src/usr/sbin/kolibri-autosync -O /usr/sbin/kolibri-autosync
wget https://raw.githubusercontent.com/cyberorg/kolibri-autosync/master/src/lib/systemd/system/kolibri-autosync.service -O /lib/systemd/system/kolibri-autosync.service
chmod +x /usr/sbin/kolibri-autosync.py /usr/sbin/kolibri-autosync
systemctl enable kolibri-autosync.service
systemctl start kolibri-autosync.service

