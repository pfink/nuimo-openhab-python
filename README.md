# nuimo-openhab-python (Alpha)

[![Join the chat at https://gitter.im/nuimo-openhab-python/Lobby](https://badges.gitter.im/nuimo-openhab-python/Lobby.svg)](https://gitter.im/nuimo-openhab-python/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

An application based on [getsenic/nuimo-linux-python](https://github.com/getsenic/nuimo-linux-python) to use your Nuimo as a UI for OpenHab! This project is in a very early state of development - so please be prepared that the configuration capabilities are quite limited at the moment and that there will be bugs and unexpected behaviour.

## Installation (Linux only)

1. Make sure bluez version 5.43 or higher  is installed. Normally, you can check your bluez version by executing this command: `bluetoothd --version`.
1. `git clone --recursive https://github.com/pfink/nuimo-openhab-python && cd nuimo-openhab-python && git checkout latest-release`
1. Adjust *config.example.yml* to your needs and rename it to *config.yml*
1. Optionally, you can move config.yml to another location (e.g. */etc/nuimo-openhab/config.yml*). If you do so, you have to specify that path via the environment variable `NUIMO_OPENHAB_CONFIG_PATH`.
1. Install dependencies (the following commands are examples for a Debian-based system):
    1. `apt-get install python3-pip python3-dbus python3-gi python3-yaml`
    1. `pip3 install -r nuimo-openhab-python/requirements.txt`
    
### Upgrade an existing installation

1. Run `git pull --recurse-submodules`
1. Re-Run `pip3 install -r nuimo-openhab-python/requirements.txt` to make sure you have all dependencies needed
1. You may have to merge the newest version of `config.example.yml` to your `config.yml`
1. Consider the release notes whether more actions are required

## openHAB Configuration

Before you start the App, you should configure the openHAB-side to define which items you want to control with your Nuimo.

1. Create a group item with the name *Nuimo* on your openHAB and add items you want to control with the Nuimo to that Group.
1. Make sure that every group member defines an icon. There are two ways of defining an icon for an item:
    1. Put the name of a [predefined icon](https://gist.github.com/pfink/7a468eb906644dc570cc28acb7c4d2b7) into the `<icon>` tag.
    1. Alternatively, you can put use labels to define the icons showed on the 9x9 Nuimo LED matrix. The label have to be a string of the length of 81 chars (9x9) and consist of asterisks(`*`) for led=on and spaces (` `) for led=off.
1. You can nest groups to create menu hierarchies.

Please find an example configuration below:

```
Group Nuimo

Group:String:AVG MyLamp <light> (Nuimo)
Group:String:AVG MyMusic <music> (Nuimo)
Group:String:AVG PlayerGuestroom <letterG> (MyMusic)
Group:String:AVG PlayerBedroomWithCustomIcon "******** *       **       **      * *******  *      * *       **       ********* " (Nuimo)
```

This will define 4 group items (`MyLamp` and `MyMusic` with it's childs `PlayerGuestroom` (led icon is a "G") and `PlayerBedroomWithCustomIcon` (led icon is a custom "B")) that can be controlled via Nuimo. Each "real item" you add to one of those 4 groups will receive the commands sent via the nuimo to that particular group.

## Start the application

### Installed from source

```
cd nuimo-openhab-python
python3 main.py
```

## Usage

Swipe up and down to navigate between the items. Swipe left and right to switch in our out of a group. Using the "turning knob" will always send Dimmer commands (from 0 to 100) - this can only work, if the item you bound holds a dimmer state (Number from 0 to 100). Other gestures will trigger openHAB commands as configured within the *config.yml*.

## Roadmap
- [x] Extend configuration possibilities & usability
- [ ] Add alternative key mapping examples and introduction video for the recommended key mapping
- [ ] Logging
- [x] Support icon sets
- [ ] Nuimo should be bound on a sitemap instead to the *Nuimo* group item. This will make the configuration more flexible and robust.
- [x] It should be possible to "jump into" a group so that you can navigate with the Nuimo similar to other UIs
- [ ] Improve stability & robustness
