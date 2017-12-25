import math
import time

import nuimo

from nuimo_menue import icons
from nuimo_menue.model import NuimoMenue
from nuimo_openhab.util import config
from util.button import *
import logging


class NuimoMenueControllerListener(nuimo.ControllerListener):
    def __init__(self, nuimoMenue: NuimoMenue):
        self.nuimoMenue = nuimoMenue
        self.connected = True
        self.isButtonHold = False
        self.menueWheelTurnWhileHold = False
        self.wheelReminder = 0
        self.rawEventHandler = ButtonRawEventHandler()

    def received_gesture_event(self, event):
        self.handle_gesture_event(event)
        self.handle_extra_events(event)

    def handle_extra_events(self, event):
        extra_event = self.rawEventHandler.get_highlevel_event(event.gesture)
        if(extra_event is not None):
            event = type('test', (object,), {})()
            event.gesture = extra_event
            self.handle_gesture_event(event)

    def handle_gesture_event(self, event):
        mappedCommands = config.get_mapped_commands(gesture=event.gesture, mode=self.nuimoMenue.currentMode, namespace="MENUE")
        if mappedCommands:
            mappedCommand = mappedCommands[0]

            logging.debug("Current Mode: " + str(self.nuimoMenue.currentMode))
            logging.debug("Mapped Command: " + str(mappedCommand))

            if "CHANGEMODE" in mappedCommand:
                self.nuimoMenue.currentMode = mappedCommand.split("=")[1]
            elif mappedCommand == "PARENT":
                self.nuimoMenue.navigateToParentMenue()
            elif mappedCommand == "CHILD":
                self.nuimoMenue.navigateToSubMenue()
            elif mappedCommand == "NEXT":
                self.nuimoMenue.navigateToNextApp()
            elif mappedCommand == "PREVIOUS":
                self.nuimoMenue.navigateToPreviousApp()
            elif mappedCommand == "SHOWAPP":
                logging.debug("Name: "+self.nuimoMenue.getCurrentApp().getName())
                self.nuimoMenue.showIcon()
            elif mappedCommand == "WHEELNAVIGATION":
                self.wheelNavigation(event)

            if mappedCommand != "WHEELNAVIGATION":
                self.wheelReminder = 0
        else:
            gestureResult = self.nuimoMenue.getCurrentApp().getListener().received_gesture_event(event)
            if gestureResult is not None:
                if event.gesture == nuimo.Gesture.ROTATION:
                    self.showRotationState(percent=gestureResult)
                else:
                    self.show_command_icon(fqCommand=gestureResult)

    def show_command_icon(self, fqCommand: str):
        if fqCommand in config["command_icon_mapping"]:
            if config["command_icon_mapping"][fqCommand] in icons:
                icon = icons[config["command_icon_mapping"][fqCommand]]
                self.nuimoMenue.controller.display_matrix(nuimo.LedMatrix(icon))
            else: logging.warning("Icon '"+config["command_icon_mapping"][fqCommand]+"' mapped to command '"+fqCommand+"' does not exist")
        else: logging.warning("No icon mapped to'"+fqCommand+"'")
        #if event.gesture == ButtonEvents.BUTTON_CLICK:
        #    "play"]))
        #if event.gesture == nuimo.Gesture.TOUCH_BOTTOM:
        #    self.nuimoMenue.controller.display_matrix(nuimo.LedMatrix(icons["pause"]))
        #if event.gesture == nuimo.Gesture.SWIPE_LEFT:
        #    self.nuimoMenue.controller.display_matrix(nuimo.LedMatrix(icons["previous"]))
        #if event.gesture == nuimo.Gesture.SWIPE_RIGHT:
        #    self.nuimoMenue.controller.display_matrix(nuimo.LedMatrix(icons["next"]))


    def started_connecting(self):
        logging.info("Connecting...")

    def connect_succeeded(self):
        self.connected = True
        logging.info("Connecting succeeded!")

    def connect_failed(self, error):
        logging.info("Connecting failed!")

    def started_disconnecting(self):
        logging.info("Disconnecting...")

    def disconnect_succeeded(self):
        self.connected = False
        self.attempt_reconnect()
        logging.info("Nuimo disconnected!")

    def attempt_reconnect(self):
        while (not self.connected):
            time.sleep(5)
            self.nuimoMenue.reconnect()


    def wheelNavigation(self, event):
        valueChange = event.value / 30
        self.wheelReminder += valueChange
        if (abs(self.wheelReminder) >= 10):
            if(self.wheelReminder < 0):
                self.nuimoMenue.navigateToPreviousApp()
            else:
                self.nuimoMenue.navigateToNextApp()
            self.wheelReminder = 0

    def showRotationState(self, percent):

        fullRotationString = icons[config.rotation_icon]
        fullRotationIsCircular = True

        ledCnt = int()
        for c in fullRotationString:
            if c == "*":
                ledCnt += 1

        if(percent != 0):
            ledsToShow = math.ceil(percent*ledCnt/100)
            currentRotationString = list()
            itCnt = 0
            for c in fullRotationString:
                column = itCnt%9
                row = itCnt // 9
                itCnt += 1
                if c == "*" and ledsToShow != 0 and (not fullRotationIsCircular or column > 4 or row == 0 and column == 4):
                    ledsToShow -= 1
                    currentRotationString.append("*")
                else:
                    currentRotationString.append(" ")

            if fullRotationIsCircular:
                itCnt = 80
                while(itCnt >= 0):
                    column = itCnt % 9
                    row = itCnt // 9
                    if fullRotationString[itCnt] == "*" and ledsToShow != 0 and column <= 4 and not (row == 0 and column == 4):
                        ledsToShow -= 1
                        currentRotationString[itCnt] = "*"
                    itCnt -= 1

            matrix = nuimo.LedMatrix("".join(currentRotationString))
            self.nuimoMenue.controller.display_matrix(matrix=matrix,fading=True, ignore_duplicates=True)
        pass
    pass
