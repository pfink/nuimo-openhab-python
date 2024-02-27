import sys
import logging
import time
import threading
from nuimo_openhab.util.threading import synchronized

import nuimo
import requests
from openhab import OpenHAB

import nuimo_menue
from nuimo_openhab.util import config


class OpenHabItemListener(nuimo_menue.model.AppListener):

    def __init__(self, openhab: OpenHAB):
        self.openhab = openhab
        self.widgets = []
        self.sliderWidgets = []

        # Reminds changes that are too little to directly expose them to OpenHab (if the wheel is turned very slow)
        self.reminder = 0.0

        # Caches the last dimmer item state, because the OpenHab REST API is too sluggish when the wheel is turned fast
        self.lastSliderState = 0
        self.lastSliderSentTimestamp = 0
        self.lastSliderEventTimestamp = 0
        self.maxNewRotationActionWait = 3000

    def addWidget(self, widget):
        if widget["type"] == "Slider":
            self.sliderWidgets.append(widget)
            for widget in self.sliderWidgets:
                self.maxNewRotationActionWait = max(widget["sendFrequency"], self.maxNewRotationActionWait)
        else:
            self.widgets.append(widget)

    def received_gesture_event(self, event):
        if event.gesture == nuimo.Gesture.ROTATION and len(self.sliderWidgets) != 0:
            return self.handleRotation(event)
        elif event.gesture == nuimo.Gesture.BATTERY_LEVEL:
            return self.handleBatteryLevel(event.value)
        else:
            return self.handleCommonGesture(event)

    def handleCommonGesture(self, event):
        gestureResult = None

        for widget in self.widgets:
            logging.debug("Handle gesture '%s' for widget: %s", event.gesture, widget)            
            namespace = "OPENHAB." + widget["type"]
            mappedCommands = config.get_mapped_commands(gesture=event.gesture, namespace=namespace)
            # Add additional commands defined via custom mapping
            customCommand = self.resolveCustomMappings(widget["mappings"], event.gesture.name)
            if customCommand is not None:
                mappedCommands.append(customCommand)

            logging.debug("Mapped command openHAB: %s (requested namespace: %s)", mappedCommands, namespace)

            for command in mappedCommands:
                # Special handling for mappings:
                # On custom switches (=switches with mappings), mapped commands have another meaning:
                # they define "extra mapping labels" that CAN be used within mappings, but don't have to
                # if those extra mapping labels are not used within the current widget, command is resolved as None and skipped
                if widget["type"] == "CustomSwitch" and command != customCommand:
                    command = self.resolveCustomMappings(widget["mappings"], command)

                # Special handling for TOGGLE: Resolve state first to be able showing the correct action icon
                if command == "TOGGLE":
                    state = self.openhab.get_item(widget["item"]["name"]).state
                    if state in config["toggle_mapping"]:
                        command = str(config["toggle_mapping"][state])
                    elif state == "NULL" and widget["item"]["type"] in config["initial_command"]:
                        command = str(config["initial_command"][widget["item"]["type"]])
                    else:
                        logging.warning("There is no toggle counterpart known for state '"+state+"'. Skip TOGGLE command.")

                if command is not None:
                    self.openhab.req_post("/items/" + widget["item"]["name"], command)
                    # Push back command executed, full qualified command for action icon
                    gestureResult = namespace + "." + command

        return gestureResult

    def resolveCustomMappings(self, mappings, command: str):
        for mapping in mappings:
            if mapping["label"] == command:
                return mapping["command"]
            # Workaround for toggling players
            elif mapping["label"] == ">" and command == "TOGGLEIFPLAYER":
                return "TOGGLE"

    def handleBatteryLevel(self, battery_level):
        try:
            self.openhab.req_post("/items/" + config["openhab_batterylevel_item"], str(battery_level))
            logging.debug("Updated battery level on item '%s' to %s", config["openhab_batterylevel_item"], str(battery_level))
        except requests.HTTPError as error:
            if error.response.status_code == 404:
                logging.debug("Skipping battery level update. No item with name '%s' found.", config["openhab_batterylevel_item"])
            else:
                raise error

    def handleRotation(self, event):
        return self.handleSliders(event.value)

    @synchronized
    def handleSliders(self, rotationOffset):
        valueChange = rotationOffset / (30 * config["rotation_sensitivity"])
        currentTimestamp = int(round(time.time() * 1000))
        isNewRotationAction = self.lastSliderEventTimestamp < currentTimestamp - self.maxNewRotationActionWait
        self.lastSliderEventTimestamp = currentTimestamp
        if isNewRotationAction:
            self.reminder = 0
        self.reminder += valueChange

        for widget in self.sliderWidgets:
            if isNewRotationAction:
                # Take care that the slider status shown on the LED matrix
                # and used for calculating the new slider state is not older than 3s
                self.openhab.req_post("/items/" + widget["item"]["name"], "REFRESH")
                logging.debug("New Rotation Action" + widget["item"]["name"] + "/state")
                item = self.openhab.get_item(widget["item"]["name"])
                if(item.is_state_null() or item.is_state_undef()):
                    currentState = config["initial_command"]["Dimmer"]
                else:
                    currentState = float(item.state)
                if currentState <= 0:
                    currentState = 0
                elif currentState < 1:
                    currentState *= 100
                self.lastSliderState = int(currentState)
                logging.debug("Item State: "+ str(item.state))

            if abs(self.reminder) >= 1:
                logging.debug("Old state: " + str(self.lastSliderState))

                roundedReminder = int(self.reminder)
                self.reminder -= roundedReminder
                self.lastSliderState += roundedReminder
                if self.lastSliderState <= 0:
                    self.lastSliderState = 0
                    self.reminder = 0
                elif self.lastSliderState >= 100:
                    self.lastSliderState = 100
                    self.reminder = 0

                logging.debug("New state: " + str(self.lastSliderState))

                if self.lastSliderSentTimestamp <= currentTimestamp - widget["sendFrequency"]:
                    # Send command
                    logging.debug("Sending command...")
                    self.openhab.req_post("/items/" + widget["item"]["name"], str(self.lastSliderState))

                    self.lastSliderSentTimestamp = currentTimestamp
                    if widget["sendFrequency"] != 0:
                        threading.Timer(widget["sendFrequency"]/1000, self.handleSliders, [0]).start()

        return self.lastSliderState