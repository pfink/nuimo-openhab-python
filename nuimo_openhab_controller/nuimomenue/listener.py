import nuimo
from nuimo_openhab_controller.nuimomenue.model import NuimoMenue
import time

class NuimoMenueControllerListener(nuimo.ControllerListener):
    def __init__(self, nuimoMenue: NuimoMenue):
        self.nuimoMenue = nuimoMenue
        self.connected = True

    def received_gesture_event(self, event):
        if event.gesture == nuimo.Gesture.SWIPE_UP:
            self.nuimoMenue.navigateToNextApp()
        elif event.gesture == nuimo.Gesture.SWIPE_DOWN:
            self.nuimoMenue.navigateToPreviousApp()
        else:
            if event.gesture == nuimo.Gesture.BUTTON_PRESS:
                self.nuimoMenue.showIcon()
            self.nuimoMenue.getCurrentApp().getListener().received_gesture_event(event)

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
        while(not self.connected):
            time.sleep(5)
            self.nuimoMenue.reconnect()