# Nuimo Menue Component

## Keymap Configuration

Please find a component-agnostic documentation of the keymap configuration [here](../examples/keymaps).

Component name for keymap configuration: `MENUE`

## Available actions:

### CHANGEMODE=mode_name

Changes the mode currently active to the specified `mode_name`.

### SHOWAPP

Shows the icon of the app currently active via LED matrix

### PREVIOUS

Changes the currently active app to the previous app and shows the icon of the previous app via LED matrix.

### NEXT

Changes the currently active app to the next app and shows the icon of the next app via LED matrix.

### WHEELNAVIGATION

*Rotation action*

Same as PREVIOUS and NEXT, but instead the wheel is used for navigation.

Left rotation -> PREVIOUS

Right rotation -> NEXT

### PARENT

Changes the currently active app to the parent app and shows the icon of the parent app via LED matrix.

### CHILD 

Changes the currently active app to it's first child app and shows the icon of this child app via LED matrix.