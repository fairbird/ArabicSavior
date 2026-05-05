#!/bin/bash

######### Only These two lines to edit with new version #####
version=2.5
#############################################################
PLUGINPATH='/usr/lib/enigma2/python/Plugins/Extensions/ArabicSavior'

# Download and install plugin
cd /tmp
set -e
rm -rf *ArabicSavior* > /dev/null 2>&1
echo "Backup keymap.xml"
echo ""
cp -f $PLUGINPATH/keymap.xml /tmp > /dev/null 2>&1 || true
wget -O ArabicSavior-main.tar.gz https://github.com/fairbird/ArabicSavior/archive/refs/heads/main.tar.gz
if [ -f '/tmp/ArabicSavior-main.tar.gz' ]; then
   	opkg remove enigma2-plugin-extensions-arabicsavior > /dev/null 2>&1 || true
	rm -rf /usr/lib/enigma2/python/Plugins/Extensions/ArabicSavior > /dev/null 2>&1
fi
tar -xf ArabicSavior-main.tar.gz
cp -rf ArabicSavior-main/usr /
rm -rf *ArabicSavior* > /dev/null 2>&1
rm -rf *main* > /dev/null 2>&1
echo "Restore keymap.xml"
cp -f /tmp/keymap.xml $PLUGINPATH > /dev/null 2>&1 || true
echo ""
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
killall -9 enigma2 
exit 0
