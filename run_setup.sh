#!/bin/bash

mkdir /home/$1/code
git clone https://github.com/seanruckle/BajaSAE-2017-Production.git /home/$1/code
chmod a+rwx /home/$1/code/setup.sh
/home/$1/code/setup.sh
chown -R $1 /home/$1/code
