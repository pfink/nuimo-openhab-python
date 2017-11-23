from nuimo import Gesture
from util.button import ButtonEvents
from enum import IntEnum
from itertools import chain

# Merges Nuimo gestures with generic high-level button events
AdvancedGesture = Gesture
AdvancedGesture = IntEnum('AdvancedGesture', [(i.name, i.value) for i in chain(Gesture,ButtonEvents)])