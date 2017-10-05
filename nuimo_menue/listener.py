import math
import time

import nuimo

from nuimo_menue.model import NuimoMenue


class NuimoMenueControllerListener(nuimo.ControllerListener):
    def __init__(self, nuimoMenue: NuimoMenue):
        self.nuimoMenue = nuimoMenue
        self.connected = True

    def received_gesture_event(self, event):
        if event.gesture == nuimo.Gesture.SWIPE_UP:
            self.nuimoMenue.navigateToNextApp()
        elif event.gesture == nuimo.Gesture.SWIPE_DOWN:
            self.nuimoMenue.navigateToPreviousApp()
        elif event.gesture == nuimo.Gesture.SWIPE_RIGHT:
            self.nuimoMenue.navigateToSubMenue()
        elif event.gesture == nuimo.Gesture.SWIPE_LEFT:
            self.nuimoMenue.navigateToParentMenue()
        else:
            gestureResult = self.nuimoMenue.getCurrentApp().getListener().received_gesture_event(event)

            if event.gesture == nuimo.Gesture.BUTTON_PRESS:
                self.nuimoMenue.controller.display_matrix(nuimo.LedMatrix(
                    "         "
                    "   .     "
                    "   ..    "
                    "   ...   "
                    "   ....  "
                    "   ...   "
                    "   ..    "
                    "   .     "
                    "         "
                ))
            if event.gesture == nuimo.Gesture.TOUCH_BOTTOM:
                self.nuimoMenue.controller.display_matrix(nuimo.LedMatrix(
                    "         "
                    "  .. ..  "
                    "  .. ..  "
                    "  .. ..  "
                    "  .. ..  "
                    "  .. ..  "
                    "  .. ..  "
                    "  .. ..  "
                    "         "
                ))
            if event.gesture == nuimo.Gesture.TOUCH_LEFT:
                self.nuimoMenue.controller.display_matrix(nuimo.LedMatrix(
                    "         "
                    "         "
                    "  .  .   "
                    "  . ..   "
                    "  ....   "
                    "  . ..   "
                    "  .  .   "
                    "         "
                    "         "
                ))
            if event.gesture == nuimo.Gesture.TOUCH_RIGHT:
                self.nuimoMenue.controller.display_matrix(nuimo.LedMatrix(
                    "         " +
                    "         " +
                    "   .  .  " +
                    "   .. .  " +
                    "   ....  " +
                    "   .. .  " +
                    "   .  .  " +
                    "         " +
                    "         "
                ))
            if event.gesture == nuimo.Gesture.ROTATION:
                self.showRotationState(percent=gestureResult)

    def started_connecting(self):
        print("Connecting...")

    def connect_succeeded(self):
        self.connected = True
        print("Connecting succeeded!")

    def connect_failed(self, error):
        print("Connecting failed!")

    def started_disconnecting(self):
        print("Disconnecting...")

    def disconnect_succeeded(self):
        self.connected = False
        self.attempt_reconnect()
        print("Nuimo disconnected!")

    def attempt_reconnect(self):
        while (not self.connected):
            time.sleep(5)
            self.nuimoMenue.reconnect()

    def showRotationState(self, percent):
        fullRotationString = str(
            "    *    "
            "  *   *  "
            " *     * "
            "*       *"
            "*       *"
            "*       *"
            " *     * "
            "  *   *  "
            "    *   "
        )
        fullRotationIsCircular = True
        '''
        fullRotationString = str(
            "*********"
            "*       *"
            "*       *"
            "*       *"
            "*       *"
            "*       *"
            "*       *"
            "*       *"
            "*********"
        )
        fullRotationIsCircular = True
        '''
        '''
        fullRotationString = str(
            "*********"
            "*********"
            "*********"
            "*********"
            "*********"
            "*********"
            "*********"
            "*********"
            "*********"
        )
        fullRotationIsCircular = False
        '''

        ledCnt = int()
        for c in fullRotationString:
            if c == "*":
                ledCnt += 1

        if(percent != 0):
            ledsToShow = math.ceil(percent*ledCnt/100)
            print("leds:"+str(ledsToShow))
            currentRotationString = list()
            itCnt = 0

            for c in fullRotationString:
                itCnt += 1
                if c == "*" and ledsToShow != 0 and (itCnt%9 > 4 or itCnt%9 ==0 or not fullRotationIsCircular):
                    ledsToShow -= 1
                    currentRotationString.append("*")
                else:
                    currentRotationString.append(" ")

            itCnt = 0
            if fullRotationIsCircular:
                first = True
                for c in fullRotationString[::-1]:
                    itCnt += 1
                    if c == "*" and ledsToShow != 0 and (itCnt%9 > 4 or itCnt%9 ==0):
                        if(not first):
                            ledsToShow -= 1
                        index = int(abs(itCnt-81))
                        print("print Led:" + str(index))
                        currentRotationString[index] = "*"
                        first = False

            matrix = nuimo.LedMatrix("".join(currentRotationString))
            self.nuimoMenue.controller.display_matrix(matrix=matrix,fading=True, ignore_duplicates=True)
        pass
    pass
