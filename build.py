#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py
MIT License (c) Marie Faure <dev at faure dot systems>

Build a new Room (xcape.io) plugin from the skeleton.

usage: python main.py [-h] [-s SERVER] [-p PORT] [-d] [-l LOGGER]

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
						change MQTT server host
  -p PORT, --port PORT  change MQTT server port
  -d, --debug           set DEBUG log level
  -l LOGGER, --logger LOGGER
						use logging config file

To switch MQTT broker, kill the program and start again with new arguments.
"""

import os
import sys
import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QDialog, QGridLayout, QLineEdit,
							 QLabel, QPushButton, QSizePolicy)

os.chdir(os.path.dirname(os.path.abspath(__file__)))


# __________________________________________________________________
def multiwordReplace(text, wordDic):
    """
    take a text and replace words that match a key in a dictionary with
    the associated value, return the changed text
    """
    rc = re.compile('|'.join(map(re.escape, wordDic)))
    def translate(match):
        return wordDic[match.group(0)]
    return rc.sub(translate, text)


# __________________________________________________________________
def build_new_plugin():
	room_name = roomNameInput.text().strip()
	applet = appletInput.text().replace(' ','').strip()
	props_name = propsNameInput.text().strip()
	props = propsInput.text().replace(' ','').strip().lower()
	broker = brokerInput.text().strip()
	replacements = {}
	replacements['%ROOM_NAME%'] = room_name
	replacements['%APPLET%'] = applet
	replacements['%PROPS_NAME%'] = props_name
	replacements['%PROPS%'] = props
	replacements['%BROKER%'] = broker
	replacements['Skeleton'] = applet
	files_to_hack = ['definitions.ini', 'constants.py', 'main.py', 'SkeletonApplet.py', 'SkeletonDialog.py', 'SkeletonSettingsDialog.py']
	files_to_rename = ['SkeletonApplet.py', 'SkeletonDialog.py', 'SkeletonSettingsDialog.py']
	for file_to_hack in files_to_hack:
		with open(file_to_hack, 'r') as fh:
			data = multiwordReplace(fh.read(), replacements)
		with open(file_to_hack, 'w') as fh:
			fh.write(data)
		print(file_to_hack, 'hacked for new plugin')
	for file_to_rename in files_to_rename:
		dest = file_to_rename.replace('Skeleton', applet)
		os.rename(file_to_rename, dest)
		print(file_to_rename, 'renamed to', dest)
	print('New', applet, 'plugin done for', room_name)
	app.quit()


# __________________________________________________________________
app = QApplication([])
app.setApplicationName("Build new plugin from skeleton")
folders = os.path.abspath(os.path.curdir).split(os.path.sep)
# C:\Users\jm_de\Documents\Xcape\Room\My room\Room\Plugins\PyEchoPlugin
# ['C:', 'Users', 'jm_de', 'Documents', 'Xcape', 'Room', 'My room', 'Room', 'Plugins', 'PyEchoPlugin']
room_name = ''
plugin_name = ''
props_name = ''
props = ''
if len(folders) >= 4 and folders[-3] == 'Room' and folders[-2] == 'Plugins':
	room_name = folders[-4]
if len(folders) >= 1:
	if folders[-1].startswith('Py') and folders[-1].endswith('Plugin'):
		plugin_name = folders[-1][2:-6].capitalize()
	else:
		plugin_name = folders[-1].capitalize()
if len(plugin_name):
	props_name = plugin_name + " Props"
	props = plugin_name.lower()
dialog = QDialog()
dialog.setWindowIcon(QIcon('./room.png'))
dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
roomNameInput = QLineEdit(room_name)
appletInput = QLineEdit(plugin_name)
propsNameInput = QLineEdit(props_name)
propsInput = QLineEdit(props)
brokerInput = QLineEdit('localhost')
applyButton = QPushButton('Apply')
applyButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.MinimumExpanding)
applyButton.clicked.connect(build_new_plugin)
layout = QGridLayout()
layout.setSpacing(12)
layout.addWidget(QLabel('Room name :'), 0, 0)
layout.addWidget(roomNameInput, 0, 1)
layout.addWidget(QLabel('<code>%ROOM_NAME% </code> i.e. <i>My room</i>'), 0, 2)
layout.addWidget(QLabel('Applet ID :'), 1, 0)
layout.addWidget(appletInput, 1, 1)
layout.addWidget(QLabel('<code>%APPLET% in file names </code> i.e. <i>Echo</i>'), 1, 2)
layout.addWidget(QLabel('Props name :'), 2, 0)
layout.addWidget(propsNameInput, 2, 1)
layout.addWidget(QLabel('<code>%PROPS_NAME% </code> i.e. <i>Echo Props</i>'), 2, 2)
layout.addWidget(QLabel('Props ID :'), 3, 0)
layout.addWidget(propsInput, 3, 1)
layout.addWidget(QLabel('<code>%PROPS% in code </code> i.e. <i>echo</i>'), 3, 2)
layout.addWidget(QLabel('Broker :'), 4, 0)
layout.addWidget(brokerInput, 4, 1)
layout.addWidget(QLabel('<code>%BROKER% </code> i.e. <i>localhost, 192.168.1.42</i>'), 4, 2)
layout.addWidget(applyButton, 5, 2, Qt.AlignRight)
dialog.setLayout(layout)
dialog.show()

rc = app.exec_()

sys.exit(rc)
