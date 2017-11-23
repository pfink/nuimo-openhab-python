# nuimo-openhab-python (Pre-Alpha)

[![Join the chat at https://gitter.im/nuimo-openhab-python/Lobby](https://badges.gitter.im/nuimo-openhab-python/Lobby.svg)](https://gitter.im/nuimo-openhab-python/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

An application based on [getsenic/nuimo-linux-python](https://github.com/getsenic/nuimo-linux-python) to use your Nuimo as a UI for OpenHab! This project is in a very early state of development - so please be prepared that the configuration capabilities are quite limited at the moment and that there will be bugs and unexpected behaviour.

## Installation (Linux only)

1. Make sure bluez version 5.43 or higher  is installed. Normally, you can check your bluez version by executing this command: `bluetoothd --version`.
1. `git clone --recursive https://github.com/pfink/nuimo-openhab-python`
1. Adjust *config.example.yml* to your needs and rename it to *config.yml*
1. Optionally, you can move config.yml to another location (e.g. */etc/nuimo-openhab/config.yml*). If you do so, you have to specify that path via the environment variable `NUIMO_OPENHAB_CONFIG_PATH`.
1. Install dependencies (the following commands are examples for a Debian-based system):
    1. `apt-get install python3-pip python3-dbus python3-gi python3-yaml`
    1. `pip3 install -r nuimo-openhab-python/requirements.txt`

## openHAB Configuration

Before you start the App, you should configure the openHAB-side to define which items you want to control with your Nuimo.

1. Create a group item with the name *Nuimo* on your openHAB and add items you want to control with the Nuimo to that Group.
1. Icons are not supported yet. As a "dirty workaround", you have to use labels for your items to define the icons showed on the 9x9 Nuimo LED matrix. The label have to be a string of the length of 81 chars (9x9) and consist of asterisks(`*`) for led=on and spaces (` `) for led=off.

Please find an example configuration below:

```
Group Nuimo

Group:String:AVG S "**********        *        *        *********        *        *        **********" (Nuimo)
Group:String:AVG W "*       **       **       **       **   *   **  * *  ** *   * ***     ***       *" (Nuimo)
Group:String:AVG B "******** *       **       **      * *******  *      * *       **       ********* " (Nuimo)
```

This will define 3 group items (`S`, `W` and `B`) that can be controlled via Nuimo (you don't have to use group items, normal items will also work). Each "real item" you add to one of those 3 groups will receive the commands sent via the nuimo to that particular group.

## Start the application

### Installed from source

```
cd nuimo-openhab-python
python3 main.py
```

### Docker container

```
docker start nuimo-openhab
```

## Usage

Swipe up and down to navigate between the items. Swipe left and right to switch in our out of a group. Using the "turning knob" will always send Dimmer commands (from 0 to 100) - this can only work, if the item you bound holds a dimmer state (Number from 0 to 100). Other gestures will trigger openHAB commands as configured within the *config.yml*.

## Roadmap
- [ ] Extend configuration possibilities & usability
- [ ] Logging
- [ ] Support icon sets
- [ ] Nuimo should be bound on a sitemap instead to the *Nuimo* group item. This will make the configuration more flexible and robust.
- [x] It should be possible to "jump into" a group so that you can navigate with the Nuimo similar to other UIs
- [ ] Improve stability & robustness
