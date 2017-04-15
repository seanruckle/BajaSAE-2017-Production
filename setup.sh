#!/bin/bash

apt-get purge scratch brasero libreoffice* sense-emu-tools shotwell thunderbird -y
apt-get autoremove -y
apt-get update
apt-get upgrade -y
apt-get install -y mumble mumble-server git-all arduino arduino-core witty witty-examples nmap
 mkdir /home/pit/code
git clone https://github.com/seanruckle/BajaSAE-2017-Production.git /home/pit/code

ifdown wlan0

if[! -e /usr/local/lib/processing] 
then
# This script installs the latest version of Processing for ARM into /usr/local/lib
# Run it like this: "curl https://processing.org/download/install-arm.sh | sudo sh"

# this assumes that newer releases are at the top
TAR="$(curl -sL https://api.github.com/repos/processing/processing/releases | grep -oh -m 1 'https.*linux-armv6hf.tgz')"

echo "\nDownloading $TAR..."
curl -L $TAR > processing-linux-armv6hf-latest.tgz

echo "Installing in /usr/local..."
tar fx processing-linux-armv6hf-latest.tgz -C /usr/local/lib
rm -f processing-linux-armv6hf-latest.tgz

# this returns the highest version installed
VER="$(basename $(ls -dvr /usr/local/lib/processing-* | head -1))"

# symlink target might be a directory, replace
rm -rf /usr/local/lib/processing
ln -s $VER /usr/local/lib/processing

# this assumes that /usr/local/bin is in $PATH
ln -sf ../lib/processing/processing /usr/local/bin/processing
ln -sf ../lib/processing/processing-java /usr/local/bin/processing-java

# this assumes that the desktop manager picks up .desktop files in /usr/local/share/applications
mkdir -p /usr/local/share/applications
curl -sL https://raw.githubusercontent.com/processing/processing/master/build/linux/processing.desktop > /usr/local/share/applications/processing.desktop
sed -i "s/@version@/$VER/" /usr/local/share/applications/processing.desktop
sed -i 's|/opt/processing|/usr/local/lib/processing|' /usr/local/share/applications/processing.desktop

# silence validation errors
desktop-file-install /usr/local/share/applications/processing.desktop >/dev/null 2>&1

echo "Done! You can start Processing by running \"processing\" in the terminal, or through the applications menu (might require a restart).\n"
else echo "\nProcessing already installed\n"
fi

