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

from PyQt5.QtCore import QUuid
from PyQt5.QtGui import QIcon

import os,  sys,  platform, signal

from BuildGuiApp import BuildGuiApp

os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = BuildGuiApp()

app.setApplicationDisplayName("Build new plugin")
app.setWindowIcon(QIcon('./room.png'));

# Assign handler for process exit (shows not effect on Windows in debug here)
signal.signal(signal.SIGTERM, app.quit)
signal.signal(signal.SIGINT, app.quit)
if platform.system() != 'Windows':
	signal.signal(signal.SIGHUP, app.quit)
	signal.signal(signal.SIGQUIT, app.quit)

app.start()

rc = app.exec_()

sys.exit(rc)
