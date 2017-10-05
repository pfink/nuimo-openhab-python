import sys
import time

import nuimo
import requests
from openhab import openHAB

import nuimo_menue
from nuimo_openhab.util import config


class OpenHabItemListener(nuimo_menue.model.AppListener):

    def __init__(self, openhab: openHAB):
        self.openhab = openhab

        # Reminds changes that are too little to directly expose them to OpenHab (if the wheel is turned very slow)
        self.reminder = 0.0

        # Caches the last dimmer item state, because the OpenHab REST API is too sluggish when the wheel is turned fast
        self.lastDimmerItemState = 0
        self.lastDimmerItemTimestamp = 0

    def received_gesture_event(self, event):
        if event.gesture == nuimo.Gesture.ROTATION:
            return self.handleRotation(event)
        else:
            return self.handleCommonGesture(event)

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
            try:
                currentTimestamp = int(round(time.time() * 1000))
                if (self.lastDimmerItemTimestamp < currentTimestamp-3000):
                    itemStateRaw = requests.get(self.openhab.base_url + "/items/" + self.app.getName() + "/state").text
                    currentState = float(itemStateRaw)
                    if (currentState < 0):
                        currentState = 0
                    if (currentState < 1):
                        currentState *= 100
                    currentState = int(currentState)
                    print("Raw item state: "+itemStateRaw)
                else:
                    currentState = self.lastDimmerItemState
                print("Old state: " + str(currentState))
                newState = currentState+round(self.reminder)
                if (newState < 0):
                    newState = 0
                if (newState > 100):
                    newState = 100

                print("New state: " + str(newState))

                self.lastDimmerItemState = newState
                self.lastDimmerItemTimestamp = currentTimestamp

                self.openhab.req_post("/items/" + self.app.getName(), str(newState))
            except Exception:
                newState = 0
                print(sys.exc_info())
            finally:
                self.reminder = 0
        return self.lastDimmerItemState