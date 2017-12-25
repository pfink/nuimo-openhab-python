import nuimo
import logging

class PrintingControllerListener(nuimo.ControllerListener):
    def received_gesture_event(self, event):
        if isinstance(event, nuimo.GestureEvent):
            logging.info("Received gesture: %s", event.value)

    def started_connecting(self):
        logging.info("Connecting...")

    def connect_succeeded(self):
        logging.info("Connecting succeeded!")

    def connect_failed(self, error):
        logging.info("Connecting failed!")

    def started_disconnecting(self):
        logging.info("Disconnecting...")

    def disconnect_succeeded(self):
        logging.info("Nuimo disconnected!")