import nuimo
import logging

class AppListener(nuimo.ControllerListener):
    def __init__(self, app):
        self.app = app

class App:
    def __init__(self, name, icon: nuimo.LedMatrix, appListener: AppListener, parent = None):
        logging.info("Create app: " + name + "(parent: "+ str(parent)+ ")")
        self.appListener = appListener
        self.icon = icon
        self.name = name
        self.lastLedsToShow = 0
        self.children = []
        self.parent = parent
        if self.parent is not None:
            self.parent.children.append(self)

    def getListener(self) -> AppListener:
        return self.appListener

    def getIcon(self):
        return self.icon

    def getName(self):
        return self.name

    def getParent(self):
        return self.parent

    def getChildren(self):
        return self.children

class NuimoMenue:

    def __init__(self, controller: nuimo.Controller, apps):
        self.apps = apps
        self.rootApps = apps
        self.currentAppIndex = 0
        self.controller = controller
        self.currentMode = "default"

    def navigateToNextApp(self):
        self.currentAppIndex = (self.currentAppIndex+1) % len(self.apps)
        self.showIcon()

    def navigateToPreviousApp(self):
        self.currentAppIndex = (self.currentAppIndex-1) % len(self.apps)
        self.showIcon()

    def navigateToSubMenue(self):
        children = self.getCurrentApp().getChildren()
        if(children):
            self.currentAppIndex = 0
            self.apps = children
        self.showIcon()

    def navigateToParentMenue(self):
        parent = self.getCurrentApp().getParent()
        if(parent is not None):
            if(parent.getParent() is None):
                self.apps = self.rootApps
            else:
                self.apps = parent.parent.children

            self.currentAppIndex = self.apps.index(parent)
        self.showIcon()

    def getCurrentApp(self) -> App:
        return self.apps[self.currentAppIndex]

    def showIcon(self):
        icon = self.getCurrentApp().getIcon()
        self.controller.display_matrix(matrix=icon, ignore_duplicates=True, fading=True)

    def reconnect(self):
        self.controller.connect()
