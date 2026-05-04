# -*- coding: utf-8 -*-
from keyids import KEYIDS
from Components.ConfigList import ConfigListScreen
from Components.config import config, ConfigSubsection, ConfigEnableDisable, ConfigSelection, ConfigYesNo, getConfigListEntry, configfile, ConfigText
from Components.Label import Label
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Components.Pixmap import Pixmap
from enigma import getDesktop, addFont, eActionMap, eRCInput
from Components.Sources.StaticText import StaticText
from Components.ActionMap import ActionMap
from GlobalActions import globalActionMap
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from os import path as os_path, remove as os_remove, listdir as os_listdir
from twisted.web.client import getPage, error
from .compat import PY3
from .Console import Console

try:
	from keymapparser import readKeymap
except:
	from Components.ActionMap import loadKeymap as readKeymap

PLUGINPATH = resolveFilename(SCOPE_PLUGINS, "Extensions/ArabicSavior")

def trace_error():
	import sys
	import traceback
	try:
		traceback.print_exc(file=sys.stdout)
		traceback.print_exc(file=open("/tmp/ArabicSavior.log", "a"))
	except:
		pass

def logdata(label_name = "", data = None):
	try:
		data=str(data)
		fp = open("/tmp/ArabicSavior.log", "a")
		fp.write( str(label_name) + " : " + data+"\n")
		fp.close()
	except:
		trace_error()    
		pass

def dellog(label_name = "", data = None):
	try:
		if os_path.exists("/tmp/ArabicSavior.log"):
			os_remove("/tmp/ArabicSavior.log")
	except:
		pass

def DreamOS():
	if os_path.exists("/var/lib/dpkg/status"):
		return DreamOS

def getversioninfo():
	currversion = "1.0"
	version_file = resolveFilename(SCOPE_PLUGINS, "Extensions/ArabicSavior/version")
	if os_path.exists(version_file):
		try:
			fp = open(version_file, "r").readlines()
			for line in fp:
				if "version" in line:
					currversion = line.split("=")[1].strip()
		except:
			pass
	return (currversion)

VER = getversioninfo()

GETPath = os_path.join(PLUGINPATH + "/fonts")

if os_path.exists(PLUGINPATH + "/fonts/font_default.otf"):
	try:
		DEFAULTFont = PLUGINPATH + "/fonts/font_default.otf"
	except Exception as error:
		trace_error()
else:
	logdata("ArabicSavior:  Missing DEFAULT Font")

fonts = []
try:
	if os_path.exists(GETPath):
		for fontName in os_listdir(GETPath):
			fontNamePath = os_path.join(GETPath, fontName)
			if fontName.endswith(".ttf") or fontName.endswith(".otf"):
				fontName = fontName[:-4]
				fonts.append((fontNamePath, fontName))
except Exception as error:
	trace_error()

fonts = sorted(fonts, key=lambda x: x[1])

config.ArabicSavior = ConfigSubsection()
config.ArabicSavior.active = ConfigEnableDisable(default=True)
config.ArabicSavior.updateonline = ConfigYesNo(default=True)
config.ArabicSavior.fonts = ConfigSelection(default=DEFAULTFont, choices=fonts)
config.ArabicSavior.keyname_enable = ConfigYesNo(default=False)
config.ArabicSavior.keyname = ConfigText(default="KEY_TEXT")

FONTSTYPE = config.ArabicSavior.fonts.value

sz_w = getDesktop(0).size().width()


class KeyCaptureScreen(Screen):
	skin = """<screen position="center,center" size="500,100" title="اضغط الزر المراد تعيينه" flags="wfNoBorder">
	<widget name="label" position="10,10" size="480,80" font="Regular;28" halign="center" valign="center"/>
	</screen>"""
	def __init__(self, session):
		Screen.__init__(self, session)
		self["label"] = Label(_("اضغط أي زر من الريموت ..."))
		self.key_caught = False
		self["actions"] = ActionMap(["SetupActions", "WizardActions", "MenuActions"], 
			{
				"cancel": self.close,
				"ok": self.dummy,
				"up": self.dummy,
				"down": self.dummy,
				"left": self.dummy,
				"right": self.dummy
			}, -100)
		self.onFirstExecBegin.append(self.startHook)
		self.onClose.append(self.stopHook)

	def dummy(self):
		return 1

	def startHook(self):
		try:
			self.hook_slot = eActionMap.getInstance().bindAction('', -2147483648, self.keyPressed)
		except:
			pass

	def stopHook(self):
		try:
			if hasattr(self, 'hook_slot'):
				self.hook_slot = None
				eActionMap.getInstance().unbindAction('', self.keyPressed)
		except:
			pass

	def keyPressed(self, key, flag):
		if flag == 1:
			keyname = self.resolveKeyName(key)
			if keyname:
				if keyname in ("KEY_EXIT", "KEY_ESC"):
					self.close(None)
					return 1
				if not self.key_caught:
					self.key_caught = True
					self.close(keyname)
					return 1
		return 1

	def resolveKeyName(self, key):
		try:
			from keyids import KEYIDS
			for name, k_id in KEYIDS.items():
				if k_id == key:
					return name
		except:
			pass
		try:
			rc = eRCInput.getInstance()
			if hasattr(rc, 'getLabel'): return rc.getLabel(key)
			if hasattr(rc, 'getKeyName'): return rc.getKeyName(key)
		except:
			pass
		return None


class ArabicSaviorSetup(ConfigListScreen, Screen):
	if sz_w == 1280:
		skin="""
<screen name="ArabicSaviorSetup" position="center,center" size="620,398" title="  RAED منقذ اللغه العربيه د.محمود فرج - تحديث   " flags="wfNoBorder" >
<widget source="Title" position="5,5" size="610,30" render="Label" font="Regular;25" foregroundColor="#00ffa500" backgroundColor="#16000000" transparent="1" halign="center"/>
<widget name="config" position="13,45" size="584,119" scrollbarMode="showOnDemand"/>
<eLabel text="" foregroundColor="#00ff2525" backgroundColor="#00ff2525" size="150,3" position="8,394" zPosition="-10"/>
<eLabel text="" foregroundColor="#00389416" backgroundColor="#00389416" size="150,3" position="163,394" zPosition="-10"/>
<eLabel text="" foregroundColor="#00bab329" backgroundColor="#00bab329" size="150,3" position="318,394" zPosition="-10"/>
<eLabel text="" foregroundColor="#000000ff" backgroundColor="#000000ff" size="150,3" position="473,394" zPosition="-10"/>
<widget render="Label" source="key_red" position="8,360" size="150,35" zPosition="5" valign="center" halign="left" backgroundColor="#16000000" font="Regular;28" transparent="1" foregroundColor="#00ffffff" shadowColor="black" shadowOffset="-1,-1"/>
<widget render="Label" source="key_green" position="163,360" size="150,35" zPosition="5" valign="center" halign="left" backgroundColor="#16000000" font="Regular;28" transparent="1" foregroundColor="#00ffffff" shadowColor="black" shadowOffset="-1,-1"/>
<widget render="Label" source="key_yellow" position="318,360" size="150,35" zPosition="5" valign="center" halign="left" backgroundColor="#16000000" font="Regular;28" transparent="1" foregroundColor="#00ffffff" shadowColor="black" shadowOffset="-1,-1"/>
<widget render="Label" source="key_blue" position="473,360" size="150,35" zPosition="5" valign="center" halign="left" backgroundColor="#16000000" font="Regular;28" transparent="1" foregroundColor="#00ffffff" shadowColor="black" shadowOffset="-1,-1"/>
<widget name="Picture" position="23,174" size="570,150" zPosition="5" alphatest="on"/>
</screen>"""
	else:
		if DreamOS():
			skin="""
<screen name="ArabicSaviorSetup" position="center,center" size="840,560" title="  RAED منقذ اللغه العربيه  د.محمود فرج - تحديث   " flags="wfNoBorder" >
<widget source="Title" position="5,5" size="826,50" render="Label" font="Regular;28" foregroundColor="#00ffa500" backgroundColor="#16000000" transparent="1" halign="center"/>
<widget name="config" position="28,70" size="780,250" scrollbarMode="showOnDemand"/>
<eLabel text="" foregroundColor="#00ff2525" backgroundColor="#00ff2525" size="200,5" position="8,550" zPosition="-10"/>
<eLabel text="" foregroundColor="#00389416" backgroundColor="#00389416" size="200,5" position="213,550" zPosition="-10"/>
<eLabel text="" foregroundColor="#00bab329" backgroundColor="#00bab329" size="200,5" position="418,550" zPosition="-10"/>
<eLabel text="" foregroundColor="#000000ff" backgroundColor="#000000ff" size="200,5" position="623,550" zPosition="-10"/>
<widget render="Label" source="key_red" position="8,515" size="200,40" zPosition="5" valign="center" halign="center" backgroundColor="#16000000" font="Regular;28" transparent="1" foregroundColor="#00ffffff" shadowColor="black" shadowOffset="-1,-1"/>
<widget render="Label" source="key_green" position="213,515" size="200,40" zPosition="5" valign="center" halign="center" backgroundColor="#16000000" font="Regular;28" transparent="1" foregroundColor="#00ffffff" shadowColor="black" shadowOffset="-1,-1"/>
<widget render="Label" source="key_yellow" position="418,515" size="200,40" zPosition="5" valign="center" halign="center" backgroundColor="#16000000" font="Regular;28" transparent="1" foregroundColor="#00ffffff" shadowColor="black" shadowOffset="-1,-1"/>
<widget render="Label" source="key_blue" position="623,515" size="200,40" zPosition="5" valign="center" halign="center" backgroundColor="#16000000" font="Regular;28" transparent="1" foregroundColor="#00ffffff" shadowColor="black" shadowOffset="-1,-1"/>
<widget name="Picture" position="126,311" size="570,150" zPosition="5" alphatest="on"/>
</screen>"""
		else:
			skin="""
<screen name="ArabicSaviorSetup" position="center,center" size="840,560" title="  RAED منقذ اللغه العربيه  د.محمود فرج - تحديث   " flags="wfNoBorder" >
<widget source="Title" position="5,5" size="826,50" render="Label" font="Regular;28" foregroundColor="#00ffa500" backgroundColor="#16000000" transparent="1" halign="center"/>
<widget name="config" font="Regular;28" secondfont="Regular;26" itemHeight="45" position="28,80" size="780,250" scrollbarMode="showOnDemand"/>
<eLabel text="" foregroundColor="#00ff2525" backgroundColor="#00ff2525" size="200,5" position="8,550" zPosition="-10"/>
<eLabel text="" foregroundColor="#00389416" backgroundColor="#00389416" size="200,5" position="213,550" zPosition="-10"/>
<eLabel text="" foregroundColor="#00bab329" backgroundColor="#00bab329" size="200,5" position="418,550" zPosition="-10"/>
<eLabel text="" foregroundColor="#000000ff" backgroundColor="#000000ff" size="200,5" position="623,550" zPosition="-10"/>
<widget render="Label" source="key_red" position="8,515" size="200,40" zPosition="5" valign="center" halign="center" backgroundColor="#16000000" font="Regular;28" transparent="1" foregroundColor="#00ffffff" shadowColor="black" shadowOffset="-1,-1"/>
<widget render="Label" source="key_green" position="213,515" size="200,40" zPosition="5" valign="center" halign="center" backgroundColor="#16000000" font="Regular;28" transparent="1" foregroundColor="#00ffffff" shadowColor="black" shadowOffset="-1,-1"/>
<widget render="Label" source="key_yellow" position="418,515" size="200,40" zPosition="5" valign="center" halign="center" backgroundColor="#16000000" font="Regular;28" transparent="1" foregroundColor="#00ffffff" shadowColor="black" shadowOffset="-1,-1"/>
<widget render="Label" source="key_blue" position="623,515" size="200,40" zPosition="5" valign="center" halign="center" backgroundColor="#16000000" font="Regular;28" transparent="1" foregroundColor="#00ffffff" shadowColor="black" shadowOffset="-1,-1"/>
<widget name="Picture" position="126,311" size="570,150" zPosition="5" alphatest="on"/>
</screen>"""

	def __init__(self, session):
		dellog()
		Screen.__init__(self, session)
		self.session = session
		self.skin = ArabicSaviorSetup.skin
		self.configChanged = False
		list = []
		ConfigListScreen.__init__(self, list)
		self["config"].list = list
		self["key_red"] = StaticText(_("الغاء"))
		self["key_green"] = StaticText(_("حفظ"))
		self["key_yellow"] = StaticText(_("تفعيل اللغة"))
		self["key_blue"] = StaticText("")
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"], 
			{
				"cancel": self.keyClose,
				"green": self.keySave,
				"yellow": self.activate,
				"blue": self.captureKey,
			}, -1)

		self.set_active_value = config.ArabicSavior.active.value
		self.set_keyname_value = config.ArabicSavior.keyname.value
		self.set_fonts_value = config.ArabicSavior.fonts.value

		self.new_version = VER

		self["Picture"] = Pixmap()
		self.createConfigList()
		self.onLayoutFinish.append(self.setWindowTitle)

	def setWindowTitle(self):
		self.setTitle("منقذ اللغة العربية إصدار %s" % VER)
		updateOnline = config.ArabicSavior.updateonline.value
		if updateOnline:
			 self.checkupdates()

	def createConfigList(self):
		self.configChanged = True
		self.set_active = getConfigListEntry(_(":تفعيل وتعطيل المنقذ العربي"), config.ArabicSavior.active)
		self.set_updateonline = getConfigListEntry(_(":تفعيل وتعطيل خاصية التحديث المباشر"), config.ArabicSavior.updateonline)
		self.set_keyname_enable = getConfigListEntry(_(":تفعيل وتعطيل خاصية الزر السريع"), config.ArabicSavior.keyname_enable)
		self.set_fonts = getConfigListEntry(_(":اختيار نوع الخط"), config.ArabicSavior.fonts)

		list = []
		list.append(self.set_active)
		list.append(self.set_updateonline)
		list.append(self.set_keyname_enable)
		if config.ArabicSavior.keyname_enable.value:
			self["key_blue"].setText(_("تعيين زر السريع"))
		else:
			self["key_blue"] = StaticText("")
		list.append(self.set_fonts)

		self["config"].list = list
		self["config"].l.setList(list)
		self["config"].onSelectionChanged.append(self.Picture)

	def Picture(self):
		try:
			cur = self["config"].getCurrent()
			if cur == self.set_fonts:
				preview = PLUGINPATH + "/images/preview/%s.png" % config.ArabicSavior.fonts.value
				preview = preview.replace(PLUGINPATH + "/fonts", "")
				if os_path.exists(preview):
					self["Picture"].instance.setPixmapFromFile(preview)
					self["Picture"].show()
				else:
					logdata("Picture preview: No preview image")
			else:
				self["Picture"].hide()
		except Exception as error:
			logdata("Picture preview:", error)

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.Picture()
		self.createConfigList()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.createConfigList()
		self.Picture()

	def captureKey(self):
		if config.ArabicSavior.keyname_enable.value:
			self.session.openWithCallback(self.keyCaptured, KeyCaptureScreen)

	def keyCaptured(self, keyname=None):
		if keyname:
			config.ArabicSavior.keyname.value = keyname
			config.ArabicSavior.keyname.save()
			self.keySave()
			self.createConfigList()

	def activate(self):
		try:
			addFont(FONTSTYPE, "ArabicFont", 100, 1)
			logdata("activate: arabic font added successfully")
		except Exception as error:
			logdata("activate:", error)
		self["key_red"].setText(_("الغاء"))
		self["key_green"].setText(_("حفظ"))
		self.setTitle("منقذ اللغة العربية إصدار %s" % VER)

	def keySave(self):
		for x in self["config"].list:
			x[1].save()
		configfile.save()
		try:
			addFont(FONTSTYPE, "ArabicFont", 100, 1)
			logdata("activate: arabic font added successfully")
		except Exception as error:
			logdata("activate:", error)
		try:
			if os_path.exists("/usr/lib64/enigma2/python/Plugins/Extensions/ArabicSavior/keymap.xml"):
				keymap_path = "/usr/lib64/enigma2/python/Plugins/Extensions/ArabicSavior/keymap.xml"
			else:
				keymap_path = "/usr/lib/enigma2/python/Plugins/Extensions/ArabicSavior/keymap.xml"
			keyfile = open(keymap_path, "w")
			keyfile.write('<keymap>\n\t<map context="GlobalActions">\n\t\t<key id="%s" mapto="ArabicSavior" flags="m" />\n\t</map>\n\_n</keymap>' % config.ArabicSavior.keyname.value)
			keyfile.close()
		except Exception as error:
			logdata("keySave keymap error:", error)
		if self.set_active_value != config.ArabicSavior.active.value or \
			self.set_fonts_value != config.ArabicSavior.fonts.value or \
			self.set_keyname_value != config.ArabicSavior.keyname.value:
			self.session.openWithCallback(self.restart, MessageBox, _("تم تغيير الإعدادات \n\n هل تريد إعادة تشغيل الانجيما الآن؟"))
		else:
			self.close(True)

	def restart(self, answer = None):
		if answer:
			restartEnigma(self.session, answer)
			return
		self.close(True)

	def keyClose(self):
		for x in self["config"].list:
			x[1].cancel()
		self.close()

	def checkupdates(self):
		try:
			url = b"https://raw.githubusercontent.com/fairbird/ArabicSavior/main/installer.sh"
			getPage(url, timeout = 10).addCallback(self.parseData).addErrback(self.errBack)
		except Exception as error:
			trace_error()

	def errBack(self, error = None):
		logdata("errBack-error",error)

	def parseData(self, data):
		if PY3:
			data = data.decode("utf-8")
		else:
			data = data.encode("utf-8")
		if data:
			lines = data.split("\n")
			for line in lines:
				if line.startswith("version"):
					self.new_version = line.split("=")[1]
		logdata("Current VER", VER)
		logdata("New VER", self.new_version)
		if float(VER) == float(self.new_version) or float(VER)>float(self.new_version):
			logdata("Updates","No new version available")
		else :
			new_version = self.new_version
			self.session.openWithCallback(self.install, MessageBox, _("New version %s is available.\n\nDo want ot install now." % new_version), MessageBox.TYPE_YESNO)

	def install(self, answer = False):
		try:
			if answer:
				cmdlist = []
				cmd="wget https://raw.githubusercontent.com/fairbird/ArabicSavior/main/installer.sh -O - | /bin/sh"
				cmdlist.append(cmd)
				self.session.open(Console, title = "Installing last update, enigma will be started after install", cmdlist = cmdlist, finishedCallback = self.myCallback, closeOnSuccess=False)
		except:
				trace_error()
	
	def myCallback(self, result = None):
		return


def restartEnigma(session, answer=None):
	if answer:
		session.open(TryQuitMainloop, 3)


def panic(session, **kwargs):
	global FONTSTYPE
	try:
		FONTSTYPE = config.ArabicSavior.fonts.value
		if FONTSTYPE not in [x[0] for x in fonts]:
			FONTSTYPE = DEFAULTFont
		config.ArabicSavior.active.value = True
		config.ArabicSavior.active.save()
		config.ArabicSavior.fonts.value = FONTSTYPE
		config.ArabicSavior.fonts.save()
		configfile.save()
		addFont(FONTSTYPE, "ArabicFont", 100, 1)
		logdata("panic: quick activation applied")
		session.openWithCallback(lambda answer: restartEnigma(session, answer), MessageBox, _("تم تفعيل الإعدادات السريعة بنجاح\n\n هل تريد إعادة تشغيل الانجيما الآن؟"), MessageBox.TYPE_YESNO)

	except Exception as error:
		logdata("panic:", error)
		session.open(MessageBox, _("حدث خطأ أثناء التفعيل السريع"), MessageBox.TYPE_ERROR, timeout=4)


def main(session, **kwargs):
	session.open(ArabicSaviorSetup)


def sessionstart(reason, session=None, **kwargs):
	if reason == 0:
		if session is not None:
			if config.ArabicSavior.keyname_enable.value:
				keymap = resolveFilename(SCOPE_PLUGINS, "Extensions/ArabicSavior/keymap.xml")
				readKeymap(keymap)
				globalActionMap.actions['ArabicSavior'] = lambda: panic(session)
		if config.ArabicSavior.active.value:
			try:
				addFont(FONTSTYPE, "ArabicFont", 100, 1)
				logdata("activate: arabic font added successfully")
			except Exception as error:
				logdata("activate:", error)

def Plugins(**kwargs):
	list = []
	list.append(PluginDescriptor(where = [PluginDescriptor.WHERE_SESSIONSTART], fnc=sessionstart))
	list.append(PluginDescriptor(icon = "icon.png", name = "المنقذ العربي", description = "إصلاح اللغة العربية", where = PluginDescriptor.WHERE_PLUGINMENU, fnc = main))
	list.append(PluginDescriptor(name = "ArabicSavior تفعيل سريع المنقذ العربي", description = "ArabicSavior تفعيل آخر إعدادات الخط بسرعة", where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc = panic))
	return list
