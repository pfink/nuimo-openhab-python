import sys

import nuimo
import requests
from openhab import openHAB

import nuimo_menue
from nuimo_openhab.util import config


class OpenHabItemListener(nuimo_menue.model.AppListener):

    def __init__(self, openhab: openHAB):
        # Reminds changes that are too small to directly expose them
        self.reminder = 0.0
        self.openhab = openhab

    def received_gesture_event(self, event):
        print(event.gesture)
        if event.gesture == nuimo.Gesture.ROTATION:
            self.handleRotation(event)
        else:
            self.handleCommonGesture(event)

    def handleCommonGesture(self, event):
        gestureCommandMapping = config["default_gesture_command_mapping"]
        currentGestureName = nuimo.Gesture(event.gesture).name

        if(currentGestureName in gestureCommandMapping):
            self.openhab.req_post("/items/" + self.app.getName(), gestureCommandMapping[currentGestureName])

    def handleRotation(self, event):
        valueChange = event.value / 30
        self.reminder += valueChange
        if (abs(self.reminder) >= 1):
            self.openhab.req_post("/items/" + self.app.getName(), "REFRESH")
            print("http://192.168.0.31:8080/rest/items/" + self.app.getName() + "/state")
            itemStateRaw = requests.get(self.openhab.base_url + "/items/" + self.app.getName() + "/state").text
            try:
                print(itemStateRaw)
                state = float(itemStateRaw)
                if (state < 0):
                    state = 0
                if (state < 1):
                    state *= 100
                state = int(state)
                print("Old state: " + str(state))
                state += round(self.reminder)
                if (state > 100):
                    state = 100
                self.reminder = 0
                print("New state: " + str(state))
            except Exception:
                print(sys.exc_info()[0])
                state = 0
            self.openhab.req_post("/items/" + self.app.getName(), str(state))
            self.app.showRotationState(state)
