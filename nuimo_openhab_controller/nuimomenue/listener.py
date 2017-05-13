import nuimo
from nuimo_openhab_controller.nuimomenue.model import NuimoMenue

class NuimoMenueControllerListener(nuimo.ControllerListener):
    def __init__(self, nuimoMenue: NuimoMenue):
        self.nuimoMenue = nuimoMenue

    def received_gesture_event(self, event):
        if event.gesture == nuimo.Gesture.SWIPE_UP:
            self.nuimoMenue.navigateToNextApp()
        elif event.gesture == nuimo.Gesture.SWIPE_DOWN:
            self.nuimoMenue.navigateToPreviousApp()
        else:
            self.nuimoMenue.getCurrentApp().getListener().received_gesture_event(event)

    def started_connecting(self):
        print("Connecting...")

    def connect_succeeded(self):
        print("Connecting succeeded!")

    def connect_failed(self, error):
        print("Connecting failed!")

    def started_disconnecting(self):
        print("Disconnecting...")

    def disconnect_succeeded(self):
        print("Nuimo disconnected!")