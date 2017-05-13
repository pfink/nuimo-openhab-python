import nuimo
from  nuimo_openhab_controller import nuimomenue
import requests
import sys

class OpenHabItemListener(nuimomenue.model.AppListener):

    def __init__(self):
        # Reminds changes that are too small to directly expose them
        self.reminder = 0.0

    def received_gesture_event(self, event):
        print(event.gesture)
        if event.gesture == nuimo.Gesture.ROTATION:
            valueChange = event.value/30
            self.reminder += valueChange
            if(abs(self.reminder) >= 1):
                requests.post("http://192.168.0.31:8080/rest/items/" + self.app.getName(), "REFRESH")
                itemStateRaw = requests.get("http://192.168.0.31:8080/rest/items/"+self.app.getName()+"/state").text
                print("http://192.168.0.31:8080/rest/items/"+self.app.getName()+"/state")
                try:
                    print(itemStateRaw)
                    state = float(itemStateRaw)
                    if(state < 0):
                        state = 0
                    if(state < 1):
                        state *= 100
                    state = int(state)
                    print("Old state: "+ str(state))
                    state += round(self.reminder)
                    if(state > 100):
                        state=100
                    self.reminder = 0
                    print("New state: "+str(state))
                except Exception:
                    print(sys.exc_info()[0])
                    state = 0
                requests.post("http://192.168.0.31:8080/rest/items/"+self.app.getName(), str(state))
                self.app.showRotationState(state)

        elif event.gesture == nuimo.Gesture.BUTTON_PRESS:
            itemStateRaw = requests.get("http://192.168.0.31:8080/rest/items/" + self.app.getName() + "/state").text
            print(itemStateRaw)
            if itemStateRaw != "ON":
                requests.post("http://192.168.0.31:8080/rest/items/" + self.app.getName(), "ON")
            else:
                print("http://192.168.0.31:8080/rest/items/" + self.app.getName())
                requests.post("http://192.168.0.31:8080/rest/items/" + self.app.getName(), "OFF")
        elif event.gesture == nuimo.Gesture.TOUCH_RIGHT:
            requests.post("http://192.168.0.31:8080/rest/items/" + self.app.getName(), "NEXT")
        elif event.gesture == nuimo.Gesture.TOUCH_LEFT:
            requests.post("http://192.168.0.31:8080/rest/items/" + self.app.getName(), "PREVIOUS")
