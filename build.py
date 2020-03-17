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

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QDialog, QGridLayout, QLineEdit,
							 QLabel, QPushButton, QSizePolicy)

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def build_new_plugin():
	room_name = roomNameInput.text().strip()
	applet = appletInput.text().replace(' ','').strip()
	props_name = propsNameInput.text().strip()
	props = propsInput.text().replace(' ','').strip().lower()
	broker = brokerInput.text().strip()
	pass


app = QApplication([])
app.setApplicationName("Build new plugin from skeleton")
dialog = QDialog()
dialog.setWindowIcon(QIcon('./room.png'))
dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
roomNameInput = QLineEdit()
appletInput = QLineEdit()
propsNameInput = QLineEdit()
propsInput = QLineEdit()
brokerInput = QLineEdit()
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
