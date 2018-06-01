# Customizing the applications behavior with keymaps

This article describes how you can customize the applications behavior using a predefined or custom keymap configuration.

## Concepts

### Events and Gestures

An event is triggered when a user is interacting with the Nuimo by doing a specific gesture. You can find a list of all available Nuimo gesture types [here](https://github.com/getsenic/nuimo-linux-python/blob/0.3.6/nuimo/nuimo.py#L398).
Additionally, `BUTTON_HOLD`, `BUTTON_CLICK`, `BUTTON_DOUBLE_CLICK` and `BUTTON_TRIPLE_CLICK` are available.

### Modes

A mode is a specific context of the application. For each mode / context, different mapping can be applied. Every keymap has to define a `default` mode that is entered
on application startup. Optionally, the user can add additional modes within the keymap configuration.

### Apps

An app is a set of functionalities of a device or system that can by controlled by the Nuimo.

### Actions

Actions are things that this application can do after an event is triggered. E.g.

* Navigating to a different app
* Show the icon of the currently selected app via LED matrix
* Changing the currently active mode
* Calling an app-specific functionality (turn the light on, increase volume, send web service requests, ...)

There is one special type of action called *rotation action*. Those actions can only be mapped to the `ROTATION` event.

### Keymaps

A keymap defines the behavior of this application by mapping **actions** to the **events** triggered by the user. Zero, one or multiple actions can be mapped to each event. A special action is to switch between different **modes** which makes it possible to let the mapping between events and actions depend on previous user interaction (context).

## Keymap configuration

The keymap can be configured within **[config.yml](../../config.example.yml#L23).** The schema for the keymap configuration is the following:

```
key_mapping:
  mode_name:
    event_name: "component_name.action_name[=action_value]"
```

The keywords explained:
- **key_mapping**: Static keyword that starts the keymap configuration section, must not be changed.
- **mode_name**: Name of the mode. It's mandatory to define the mode `default` which is the initially active mode. The name of additional modes can be chosen freely.
- **event_name**: Name of the Nuimo event (e.g. `BUTTON_RELEASE` or `SWIPE_LEFT`). Events that are not listed within the keymap configuration will just be ignored. 
- **component_name**: Name of the component that is responsible for handling this action (e.g. [MENUE](../../nuimo_menue) or [OPENHAB](../../nuimo_openhab))
- **action_name**: Name of the action to be executed when the event is triggered. The available actions can be found within the components documentation.
- **action_value** (optional): If the action requires a static configuration value, this one can be passed here (the available values are depending on the action).

Multiple actions can be assigned to a single event by using YAML lists. Find a generic example containing some dummy entries below:

```
key_mapping:
  mode1_name:
    event1_name: "component1_name.action1_name"
    event2_name: "component1_name.action2_name"
    ...
  mode2_name:
    event1_name: "component2_name.action1_name"
    event2_name:
      - event2_name: "component1_name.action2_name"
      - event2_name: "component1_name.action2_name"
    ...
```

## Example Keymaps

Currently, two example keymaps are available:

**[Default Keymap](default.yml)**: This keymap defines two modes.

Default/Initial mode:
- App-specific functionality only

Navigation mode:
- Swipe up+down: Go up or down the hierarchy.
- Wheel / Swipe left+right: Navigate between apps on the same hierarchy.

The navigation mode is active **as long as the Nuimo's main button is pressed**. It's entered on a `BUTTON_PRESS` event and the mode is switched back to default after a `BUTTON_RELEASE` event.


**[Simple Keymap](simple.yml):**

This sitemap has only one mode, so it does not have any context-specific mapping. Every gesture always triggers the same action(s)
Swipe up+down: Navigate between apps (hierarchies / nexted `Text` elements are NOT supported by this keymap).
A short button click sends a TOGGLE command to switches while the wheel will control the Slider elements.
