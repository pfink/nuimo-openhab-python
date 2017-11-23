from enum import IntEnum
import time

class ButtonEvents(IntEnum):
    RAWBUTTON_PRESS = 1
    RAWBUTTON_RELEASE = 2
    BUTTON_HOLD = 30
    BUTTON_CLICK = 40
    BUTTON_DOUBLE_CLICK = 50
    BUTTON_TRIPLE_CLICK = 60


class ButtonRawEventHandler:

    def __init__(self):
        self.lastRawEvent = ButtonEvents.RAWBUTTON_RELEASE
        self.lastEventTimestamp = 0
        self.clickCounter = 0

    def get_highlevel_event(self, rawEvent: ButtonEvents):
        result = None
        currentTime = time.time()
        if(rawEvent.value == ButtonEvents.RAWBUTTON_RELEASE.value):
            if(self.lastEventTimestamp+0.5 > currentTime):
                self.clickCounter += 1
                if self.clickCounter == 1:
                    result = ButtonEvents.BUTTON_CLICK
                elif self.clickCounter == 2:
                    result = ButtonEvents.BUTTON_DOUBLE_CLICK
                elif self.clickCounter == 3:
                    result = ButtonEvents.BUTTON_TRIPLE_CLICK
            else:
                result = ButtonEvents.BUTTON_HOLD
        elif rawEvent.value == ButtonEvents.RAWBUTTON_PRESS.value and self.lastEventTimestamp + 1 < currentTime:
            self.clickCounter = 0

        if(rawEvent.value == ButtonEvents.RAWBUTTON_RELEASE.value or rawEvent.value == ButtonEvents.RAWBUTTON_PRESS.value):
            self.lastRawEvent = rawEvent
            self.lastEventTimestamp = currentTime

        return result



