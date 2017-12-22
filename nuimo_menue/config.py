import yaml
from nuimo_menue.advanced_gesture import AdvancedGesture

class NuimoMenueConfiguration:

    def __init__(self, key_mapping = None, rotation_icon = None):
        if key_mapping is None:
            self.key_mapping = yaml.load("""
                    default:
                        SWIPE_UP: "MENUE.PARENT"
                        SWIPE_DOWN: "MENUE.CHILD"
                        SWIPE_LEFT: "MENUE.PREVIOUS"
                        SWIPE_RIGHT: "MENUE.NEXT"
                        ROTATION: "MENUE.WHEELNAVIGATION"
                        """)
        else:
            self.key_mapping = key_mapping

        if rotation_icon is None:
            self.rotation_icon = "circle"
        else:
            self.rotation_icon = rotation_icon


    def get_mapped_commands(self, gesture: AdvancedGesture, mode: str = "default", namespace: str = None):
        print(gesture.name)
        mapped_commands = []
        currentModeKeys = self.key_mapping[mode]
        if gesture.name in currentModeKeys:
            if isinstance(currentModeKeys[gesture.name], list):
                for fq_command in currentModeKeys[gesture.name]:
                    command = self.resolve_fq_command(fq_command, namespace)
                    if(command is not None):
                        mapped_commands.append(command)
            else:
                command = self.resolve_fq_command(currentModeKeys[gesture.name], namespace)
                if (command is not None):
                    mapped_commands.append(command)

        return mapped_commands




    def resolve_fq_command(self, fq_command: str, namespace: str = None):
        splittedFqCommand = fq_command.split(".")
        givenNamespace = ".".join(splittedFqCommand[:-1])
        command = splittedFqCommand[-1]
        if namespace is None or namespace == givenNamespace:
            return command