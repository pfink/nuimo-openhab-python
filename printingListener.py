import nuimo

class PrintingControllerListener(nuimo.ControllerListener):
    def received_gesture_event(self, event):
        if isinstance(event, nuimo.GestureEvent):
            print(event.value)

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