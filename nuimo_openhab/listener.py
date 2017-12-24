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
        self.widgets = []
        self.sliderWidgets = []

        # Reminds changes that are too little to directly expose them to OpenHab (if the wheel is turned very slow)
        self.reminder = 0.0

        # Caches the last dimmer item state, because the OpenHab REST API is too sluggish when the wheel is turned fast
        self.lastDimmerItemState = 0
        self.lastDimmerItemTimestamp = 0

    def addWidget(self, widget):
        if widget["type"] == "Slider":
            self.sliderWidgets.append(widget)
        else:
            self.widgets.append(widget)

    def received_gesture_event(self, event):
        if event.gesture == nuimo.Gesture.ROTATION:
            return self.handleRotation(event)
        else:
            return self.handleCommonGesture(event)

    def handleCommonGesture(self, event):
        gestureResult = None

        for widget in self.widgets:
            namespace = "OPENHAB." + widget["type"]
            mappedCommands = config.get_mapped_commands(gesture=event.gesture, namespace=namespace)
            print("Mapped command openHAB: " + str(mappedCommands) + "(requested namespace: "+namespace+")")

            for command in mappedCommands:

                # Special handling for mappings
                noMappingFound = False
                if widget["type"] == "CustomSwitch":
                    for mapping in widget["mappings"]:
                        noMappingFound = True
                        if mapping["label"] == command or mapping["label"] == event.gesture.name:
                            command = mapping["command"]
                            noMappingFound = False
                            break;
                        # Workaround for toggling players
                        elif mapping["label"] == ">" and command == "TOGGLEIFPLAYER":
                            command = "TOGGLE"
                            noMappingFound = False
                            break;

                # Special handling for TOGGLE
                if command == "TOGGLE":
                    state = requests.get(self.openhab.base_url + "/items/" + widget["item"]["name"] + "/state").text
                    if state in config["toggle_mapping"]:
                        command = config["toggle_mapping"][state]
                    else:
                        raise RuntimeWarning("There is no toggle counterpart known for state '"+state+"'. Skip TOGGLE command.")

                if not noMappingFound:
                    self.openhab.req_post("/items/" + widget["item"]["name"], command)
                    # Push back command executed, full qualified command for action icon
                    gestureResult = namespace + "." + command

            return gestureResult

    def handleRotation(self, event):
        for widget in self.sliderWidgets:
            valueChange = event.value / 30
            self.reminder += valueChange
            if (abs(self.reminder) >= 1):
                self.openhab.req_post("/items/" + widget["item"]["name"], "REFRESH")
                print(self.openhab.base_url + widget["item"]["name"] + "/state")
                try:
                    currentTimestamp = int(round(time.time() * 1000))
                    if (self.lastDimmerItemTimestamp < currentTimestamp-3000):
                        itemStateRaw = requests.get(self.openhab.base_url + "/items/" + widget["item"]["name"] + "/state").text
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

                    self.openhab.req_post("/items/" + widget["item"]["name"], str(newState))
                except Exception:
                    newState = 0
                    print(sys.exc_info())
                finally:
                    self.reminder = 0
        return self.lastDimmerItemState