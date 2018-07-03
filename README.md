# Nuimo openHAB Integration

[![Actively Maintained](https://maintained.tech/badge.svg)](https://maintained.tech/)
[![Join the chat at https://gitter.im/nuimo-openhab-python/Lobby](https://badges.gitter.im/nuimo-openhab-python/Lobby.svg)](https://gitter.im/nuimo-openhab-python/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![codebeat badge](https://codebeat.co/badges/7cf5a386-927c-4df9-b5e0-738637d9bb0c)](https://codebeat.co/projects/github-com-pfink-nuimo-openhab-python-master)

An application based on [getsenic/nuimo-linux-python](https://github.com/getsenic/nuimo-linux-python) to use your Nuimo as a UI for openHAB!

## Installation (Linux only)

1. Make sure bluez version 5.43 or higher  is installed. Normally, you can check your bluez version by executing this command: `bluetoothd --version`.
1. Download the latest release to your machine: `git clone --recurse-submodules https://github.com/pfink/nuimo-openhab-python -b latest-release`
1. Create a copy of *config.example.yml* with the name *config.yml*: `cd nuimo-openhab-python && cp config.example.yml config.yml`
1. Install dependencies (the following commands are examples for a Debian-based system, they may differ on other Linux distributions):
    1. `apt-get install python3-pip python3-dbus python3-gi python3-yaml`
    1. `pip3 install -r requirements.txt`
    
Optionally, you can move config.yml to another location (e.g. */etc/nuimo-openhab/config.yml*). If you do so, you have to specify that path via the environment variable `NUIMO_OPENHAB_CONFIG_PATH`.

### Setup a systemd service

To automatically run this app on system boot, you could optionally set it up in your init service. Most modern linux distributions use systemd as their init service (e.g. Debian/Raspbian since Jessie, Ubuntu since 15.04). To setup this app as a systemd service, you can put the following file to `/etc/systemd/system/nuimo-openhab.service`:

```
[Unit]
Description=Nuimo openHAB Integration Service
Requires=network-online.target bluetooth.service
After=network-online.target bluetooth.service rsyslog.service

[Service]
ExecStart=/usr/bin/python3 /YOUR_PATH_TO_THIS_APP/main.py
Type=simple
SyslogIdentifier=nuimo-openhab

[Install]
WantedBy=multi-user.target
````

Afterwards, run

```
systemctl daemon-reload
systemctl enable nuimo-openhab
```

to reload your configuration and activate auto-start on every boot.
    
### Upgrade an existing installation

1. Run `git pull --recurse-submodules && git submodule update --recursive --remote` to upgrade to the latest version of this app
1. Run `pip3 install --upgrade -r nuimo-openhab-python/requirements.txt` to update all dependencies
1. You may have to merge the newest version of `config.example.yml` to your `config.yml`
1. Consider the release notes whether more actions are required

## Application / Nuimo Configuration

The configuration of this application is done via **[config.yml](config.example.yml).**  To get started, usually just the following parameters have to be checked and adjusted:

- `openhab_api_url`
- `nuimo_mac_address`
- `bluetooth_adapter`

All other parameters have adequate default values which do not have to be changed to get started.
Anyway, you have extensive possibilities to change the applications behavior.
Normally, the descriptions and examples within  **[config.example.yml](config.example.yml)** are a sufficient documentation
of the available options. Exception: For the option `key_mapping` which is more complex, you can find a comprehensive documentation [here](examples/keymaps).

## openHAB Configuration

Before you start the App, you have to configure the openHAB-side to define which items you want to control with your Nuimo.

### Getting started

1. Create a [sitemap](https://docs.openhab.org/configuration/sitemaps.html) with the name *nuimo* on your openHAB instance (in case you have multiple Nuimo's, you can change the name of
   sitemap used within your config.yml).
1. Add elements / items you want to control with the Nuimo to that sitemap. As the possibilities of the Nuimo serving as a 
   UI are limited, only a small subset of [element types](https://docs.openhab.org/configuration/sitemaps.html#element-types) is supported:
   - `Switch`: Is used to map the Nuimo buttons to specific items / commands.
   - `Slider`: Is used to bind the Nuimo wheel to specific items.
   - `Text`: Is used to aggregate items to several "apps" among those you can navigate with the Nuimo.
   - `Default`: Partially supported. It works as long as it is internally resolved to a `Switch` or `Slider` element
     which is true for some item types (e.g. `Switch`, `Dimmer`, `Player`).
   - `Frame`: This element type is allowed, but ignored. Aggregation is done with `Text` elements because they're
   more flexible, especially they can be nested.
   
   All other element types are *not* allowed and the application won't start if they're used.
   
   [Blocks](https://docs.openhab.org/configuration/sitemaps.html#concepts) are only allowed (and mandatory) on `Frame` and `Text` elements. Nesting is supported without any limitations.
   
   [Mappings](https://docs.openhab.org/configuration/sitemaps.html#mappings) are supported. Please find all details how
   to use mappings [below](https://github.com/pfink/nuimo-openhab-python#mappings--custom-switch-configuration).
   
   Labels are supported in the way that error messages thrown by this application usually contain the label of the affected item.
1. Make sure that each `Text` element defines a 9x9 LED icon (as well as `Switch`, `Slider` and `Default` elements
   if they're not a child of a `Text` element). There are two ways of defining such an icon for an item:
    1. Add the name of a [predefined icon](https://gist.github.com/pfink/7a468eb906644dc570cc28acb7c4d2b7) with the `icon` parameter of the sitemap element or the `<icon>` tag of the bound item.
    1. Alternatively, you can use labels to define the icons showed on the 9x9 Nuimo LED matrix. The label have to be a 
       string of the length of 81 chars (9x9) and consist of asterisks(`*`) for led=on and spaces (` `) for led=off.
       In case you create custom icons, it would be great if you contribute them so that the number of predefined icons
       grows! Just leave a comment with your icon [here](https://gist.github.com/pfink/7a468eb906644dc570cc28acb7c4d2b7#comments).

### Example Sitemap Configuration

```
sitemap nuimo
{
    Text label="Multiroom Audio System" icon="music" {
        Switch item=AllRooms_Player mappings=[TOGGLE=BUTTON_CLICK]
        Slider item=AllRooms_Volume
        
        Text label="Audio Bedroom" icon="letterB" {
            Default item=Bedroom_Player
            Slider item=Bedroom_Volume
        }
        Text label="Audio Guest Room" icon="letterG" {
            Default item=GuestRoom_Player
            Slider item=GuestRoom_Volume
        }
    }
    Slider item=Simple_Light icon="light"
    
    Text label="Simple Light" icon="letterO" {
        Switch item=Simple_Light
        Slider item=Simple_Light
    }
}
```

This configuration defines 3 _apps_ on root level between those you can navigate:
- A multiroom audio system where you can control the music (Play/Pause) and volume of all rooms.
  In addition, you can jump into a sub-menu that you can use to control the music of the single rooms (here: _Bedroom_ and _Guest Room_)
- A light that you can only control with the wheel of the nuimo
- The same light again, but with a different configuration: Here you can use the wheel AND the button to control the light.

Some noteworthy details about this example configuration:
- For `Bedroom_Player` and `Guestroom_Player` (both are `Player` items), the `Default` element is used.
  This causes openHAB to create a Switch with a mapping for PLAY/PAUSE and PREVIOUS/NEXT controls. This application
  is already preconfigured so that not only PLAY/PAUSE can be used, but also PREVIOUS/NEXT (by swiping left/right).
- For `AllRooms_Player`, the `Switch` element is used instead which will suppress the special mapping so that just
  `ON`/`OFF` commands are sent. This can be useful e.g. to suppress the possibility for previous/next commands because
  they'll maybe executed multiple times when different rooms are grouped together.

All explanations refer to the default keymap configuration within `config.example.yml`. Limitations or differences may apply to deviant keymap configurations.

### Mappings / Custom Switch Configuration

[Mappings](https://docs.openhab.org/configuration/sitemaps.html#mappings) can be used to customize the mapping from
Nuimo gesture to openHAB command for each item so you're able to create customized keymaps on item level. Mappings
should always have the structure: `[OPENHAB_COMMAND1=NUIMO_GESTURE1, OPENHAB_COMMAND2=NUIMO_GESTURE2, ..]`

Some examples: 
```
Switch MyCustomPlayer mappings=[TOGGLE=BUTTON_CLICK, NEXT=SWIPE_RIGHT, PREVIOUS=SWIPE_LEFT, REWIND=TOUCH_LEFT, FASTFORWARD=TOUCH_RIGHT]
Switch MyCustomLight mappings=[OFF=SWIPE_LEFT, ON=SWIPE_RIGHT]
Switch MyCustomDimmer mappings=[INCREASE=FLY_LEFT, DECREASE=FLY_RIGHT]
```

You can find a list of all available Nuimo gestures [here](https://github.com/getsenic/nuimo-linux-python/blob/0.3.6/nuimo/nuimo.py#L398).
Additionally, `BUTTON_HOLD`, `BUTTON_CLICK`, `BUTTON_DOUBLE_CLICK` and `BUTTON_TRIPLE_CLICK` are available.

### Reading the Battery Level

If you like to track the battery level of your Nuimo within openHAB, you can simply create the following item:

```
Number Nuimo_BatteryLevel "Nuimo Battery Level [%d]"
```

In case this item is present, this app will automatically update it with the current battery level accordingly.
If you like to use a different name for this item, you can change it [within the config.yml](config.example.yml#L6).

## Start the application

Plain (without systemd or another init service):
```
cd nuimo-openhab-python
python3 main.py
```

With systemd setup:

```
systemctl start nuimo-openhab
```

## Usage

Usage depends on which [keymap](examples/keymaps) you use.

**Default Keymap:** You can navigate between apps with swipes as well as with the wheel **only as long as you hold the button**.
Swipe up+down: Go up or down the hierarchy. Wheel / Swipe left+right: Navigate between apps on the same hierarchy. When
the button is not hold, by default a short button click sends a TOGGLE command to switches while the wheel will control
the Slider elements.

**Simple Keymap:** 
Swipe up+down: Navigate between apps (hierarchies / nexted `Text` elements are NOT supported by this keymap).
A short button click sends a TOGGLE command to switches while the wheel will control the Slider elements.

This short introduction video gives a hands-on overview on the usage:

[![How to use the Nuimo openHAB integration](https://img.youtube.com/vi/QGt0zuFNhH0/3.jpg)](https://www.youtube.com/watch?v=QGt0zuFNhH0)
