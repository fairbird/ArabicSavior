#!/bin/bash
##setup command=wget -q "--no-check-certificate" https://raw.githubusercontent.com/fairbird/ArabicSavior/main/installer.sh -O - | /bin/sh

######### Only These two lines to edit with new version ######
version=1.9
##############################################################

# remove old version
if [ -f /var/lib/dpkg/status ]; then
   apt-ger -r enigma2-plugin-extensions-arabicsavior
else
   opkg remove enigma2-plugin-extensions-arabicsavior
fi

# Download and install plugin
cd /tmp
set -e
rm -rf *ArabicSavior* > /dev/null 2>&1
wget -q "--no-check-certificate" https://github.com/fairbird/ArabicSavior/archive/refs/heads/main.tar.gz
if [ -f '/tmp/ArabicSavior-main.tar.gz' ]; then
	if [ -f /var/lib/dpkg/status ]; then
   		apt-ger -r enigma2-plugin-extensions-arabicsavior
	else
   		opkg remove enigma2-plugin-extensions-arabicsavior
	fi
	rm -rf /usr/lib/enigma2/python/Plugins/Extensions/ArabicSavior > /dev/null 2>&1
fi
tar -xf main.tar.gz
cp -r ArabicSavior-main/usr /
rm -rf *ArabicSavior* > /dev/null 2>&1
rm -rf *main* > /dev/null 2>&1
set +e
cd ..
sync

### Check if plugin installed correctly
if [ ! -d '/usr/lib/enigma2/python/Plugins/Extensions/ArabicSavior' ]; then
	echo "Some thing wrong .. Plugin not installed"
	exit 1
fi

sync
echo "#########################################################"
echo "#      ArabicSavior INSTALLED SUCCESSFULLY              #"
echo "#                 mfaraj57  &  RAED                     #"              
echo "#                     support                           #"
echo "#   https://www.tunisia-sat.com/forums/threads/3896466/ #"
echo "#########################################################"
echo "#           your Device will RESTART Now                #"
echo "#########################################################"
sleep 3
killall enigma2
exit 0
