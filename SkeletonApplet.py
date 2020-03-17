#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SkeletonApplet.py
MIT License (c) Marie Faure <dev at faure dot systems>

SkeletonApplet application extends MqttApplet.
"""

from constants import *
from MqttApplet import MqttApplet
from SkeletonDialog import SkeletonDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot


class SkeletonApplet(MqttApplet):
    skeletonMessageReceived = pyqtSignal(str)

    # __________________________________________________________________
    def __init__(self, argv, client, debugging_mqtt=False):
        super().__init__(argv, client, debugging_mqtt)

        self.setApplicationDisplayName(APPDISPLAYNAME)

        # on_message per topic callbacks
        try:
            mqtt_sub_skeleton = self._definitions['mqtt-sub-%PROPS%']
            self._mqttClient.message_callback_add(mqtt_sub_skeleton, self.mqttOnMessageFromSkeletonProps)
        except Exception as e:
            self._logger.error(self.tr("Skeleton sub topic definition is missing"))
            self._logger.debug(e)

        # on_message default callback
        self._mqttClient.on_message = self.mqttOnMessage

        self._SkeletonDialog = SkeletonDialog(self.tr("Skeleton"), './room.png', self._logger)
        self._SkeletonDialog.aboutToClose.connect(self.exitOnClose)
        self.skeletonMessageReceived.connect(self._SkeletonDialog.skeletonMessage)
        self._SkeletonDialog.show()

    # __________________________________________________________________
    @pyqtSlot()
    def exitOnClose(self):
        self._logger.info(self.tr("exitOnClose "))
        self.quit()

    # __________________________________________________________________
    def mqttOnMessage(self, client, userdata, msg):
        message = None
        try:
            message = msg.payload.decode(encoding="utf-8", errors="strict")
        except:
            pass

        if message:
            self._logger.info(self.tr("Message received : '") + message + self.tr("' in ") + msg.topic)
        ##self.messageReceived.emit(msg.topic, message)
        else:
            self._logger.warning("{0} {1}".format(self.tr("MQTT message decoding failed on"), msg.topic))

    # __________________________________________________________________
    def mqttOnMessageFromSkeletonProps(self, client, userdata, msg):
        message = None
        try:
            message = msg.payload.decode(encoding="utf-8", errors="strict")
        except:
            pass

        if message:
            self._logger.info(
                self.tr("Message received from Skeleton props : '") + message + self.tr("' in ") + msg.topic)
            self.skeletonMessageReceived.emit(message)
        else:
            self._logger.warning(
                "{0} {1}".format(self.tr("Decoding MQTT message from Skeleton props failed on"), msg.topic))

    # __________________________________________________________________
    @pyqtSlot(str)
    def publishMessageToSkeleton(self, message):
        if self._definitions['mqtt-pub-%PROPS%']:
            self.publishMessage(self._definitions['mqtt-pub-%PROPS%'], message)
        else:
            self._logger.warning(
                "{0} : {1}".format(self.tr("SkeletonPlugin inbox is not defined, message ignored"), message))
