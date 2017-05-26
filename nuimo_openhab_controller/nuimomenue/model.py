import nuimo
import math

class AppListener(nuimo.ControllerListener):
    def __init__(self, app):
        self.app = app
pass

class App:
    def __init__(self, name, icon: nuimo.LedMatrix, appListener: AppListener):
        self.appListener = appListener
        self.icon = icon
        self.name = name
        self.appListener.app = self
        self.lastLedsToShow = 0

    def getListener(self) -> AppListener:
        return self.appListener

    def getIcon(self):
        return self.icon

    def getName(self):
        return self.name

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
            self.controller.display_matrix(matrix=matrix,fading=True, ignore_duplicates=True)
        pass

    pass

class NuimoMenue:

    def __init__(self, controller: nuimo.Controller, apps):
        self.apps = apps
        self.currentAppIndex = 0
        self.controller = controller
        for a in apps:
            a.controller = self.controller


    def navigateToNextApp(self):
        self.currentAppIndex = (self.currentAppIndex+1) % len(self.apps)
        self.showIcon()

    def navigateToPreviousApp(self):
        self.currentAppIndex = (self.currentAppIndex-1) % len(self.apps)
        self.showIcon()

    def getCurrentApp(self) -> App:
        return self.apps[self.currentAppIndex]

    def showIcon(self):
        icon = self.getCurrentApp().getIcon()
        self.controller.display_matrix(matrix=self.getCurrentApp().getIcon())

    def reconnect(self):
        self.controller.connect()
