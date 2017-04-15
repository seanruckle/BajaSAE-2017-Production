#!/bin/bash

mkdir /home/$1/code
curl -o /home/$1/setup.sh https://gitub.com/seanruckle/BajaSae-2017-Production/raw/master/setup.sh
chmod a+rwx /home/$1/setup.sh
/home/$1/setup.sh $1

