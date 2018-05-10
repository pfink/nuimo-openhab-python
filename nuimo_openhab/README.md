# Nuimo openHAB Component

## Keymap Configuration

Please find a component-agnostic documentation of the keymap configuration [here](../examples/keymaps).

Component name for keymap configuration: `OPENHAB`

## Available actions:

### Switch.[ITEM_COMMAND]

Executes a command on all openHAB Switches that don't have any custom mappings within the sitemap configuration.

[ITEM_COMMAND] is [any valid openHAB command for Switches](https://docs.openhab.org/configuration/items.html).

### Switch.TOGGLE

Executes a specific command based on the current state of the element to toggle the state. Which command is executed can be configured within the 
`toggle_mapping` section of **[config.yml](../../config.example.yml#L64).**

### CustomSwitch.[MAPPED_LABEL]

Executes a command on all openHAB Switches that *have* custom mappings within their sitemap configuration.
Triggers the command that is mapped to `MAPPED_LABEL` within the sitemap configuration.

[MAPPED_LABEL] is any label (can be chosen freely).

### CustomSwitch.TOGGLEIFPLAYER

Workaround making default Player elements work without extra config. Toggles PLAY/PAUSE on player elements.

### Slider.WHEELDIMMER

*Rotation action*

Sends a command between `0` and `100` depending on the current wheel state to all mapped Sliders.