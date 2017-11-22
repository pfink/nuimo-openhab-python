import math
import time

import nuimo

from nuimo_menue.model import NuimoMenue


class NuimoMenueControllerListener(nuimo.ControllerListener):
    def __init__(self, nuimoMenue: NuimoMenue):
        self.nuimoMenue = nuimoMenue
        self.connected = True
        self.isButtonHold = False
        self.menueWheelTurnWhileHold = False
        self.reminder = 0

    def received_gesture_event(self, event):
        print(event.gesture)

        #mappedCommand = config.getCommand

        if event.gesture == nuimo.Gesture.BUTTON_PRESS:
            self.isButtonHold = True
        elif event.gesture == nuimo.Gesture.BUTTON_RELEASE:
            self.isButtonHold = False
        elif event.gesture == nuimo.Gesture.ROTATION and self.isButtonHold:
            self.menueWheelTurnWhileHold = True


        if event.gesture == nuimo.Gesture.SWIPE_UP:
        #    self.nuimoMenue.navigateToNextApp()
            self.nuimoMenue.navigateToParentMenue()
        elif event.gesture == nuimo.Gesture.SWIPE_DOWN:
        #    self.nuimoMenue.navigateToPreviousApp()
        #elif event.gesture == nuimo.Gesture.SWIPE_RIGHT:
            self.nuimoMenue.navigateToSubMenue()
        #elif event.gesture == nuimo.Gesture.SWIPE_LEFT:
        #    self.nuimoMenue.navigateToParentMenue()
        elif event.gesture == nuimo.Gesture.ROTATION and self.isButtonHold:
            self.nuimoMenue.showIcon()
            self.wheelNavigation(event)
        elif not(self.isButtonHold or event.gesture == nuimo.Gesture.BUTTON_RELEASE and self.menueWheelTurnWhileHold):
            gestureResult = self.nuimoMenue.getCurrentApp().getListener().received_gesture_event(event)

            if event.gesture == nuimo.Gesture.BUTTON_RELEASE:
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

        if event.gesture == nuimo.Gesture.BUTTON_RELEASE:
            self.menueWheelTurnWhileHold = False

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


    def wheelNavigation(self, event):
        valueChange = event.value / 30
        self.reminder += valueChange
        if (abs(self.reminder) >= 10):
            if(self.reminder < 0):
                self.nuimoMenue.navigateToPreviousApp()
            else:
                self.nuimoMenue.navigateToNextApp()
            self.reminder = 0

    def showRotationState(self, percent):

        fullRotationString = str(
            "   ***   "
            "  *   *  "
            " *     * "
            "*       *"
            "*       *"
            "*       *"
            " *     * "
            "  *   *  "
            "   ***   "
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
