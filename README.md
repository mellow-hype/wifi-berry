# WifiBerry - Raspberry Pi Wireless AP, Automated

## Introduction
This script will automate the process of configuring a Raspberry Pi 3 to serve as a wireless AP. It assumes a stock install of Raspbian Jessie.

## Status
Testing. Almost complete, just fixing bugs that hadn't been tested. Code clean-up next.

## TODO
+ ~~Automagic install mode prompts and logic~~
+ ~~dnsmasq configuring menu (started)~~
+ ~~Wizard install mode functions~~
+ Testing
+ Bug fixes

## Requirements
Before running the script, you should have the Pi plugged into a monitor with a keyboard and an ethernet connection to the Internet. It is not possible to run the script over the network as it will disable the wireless interface. It may be possible to do it over the ethernet connection but this has not been tested so far.

Also, please go through the raspi-config process and be sure to set all of your localization settings and change the root password before proceeding. This is just good practice and will ensure things run smoothly.

### Dependencies
Before installing, install these dependencies if they have not been installed already.
```
sudo apt-get install python3 python3-setuptools git

```

## Installation
```

git clone https://github.com/mellow-hype/wifi-berry.git
cd wifi-berry
sudo python3 setup.py install

```
You can also use ```sudo python3 setup.py develop``` to keep the module from being installed to your main Python packages path and avoid conflicts.

## Usage
Use wifi-berry to start the interactive menu. You will need to run with sudo in order to successfully install.
```

sudo wifi-berry

```

## Goals
These are some general goals for the script:
+ Provide a default autoconfig option that uses default settings.
+ Provide a custom interactive mode that steps through the process and allows the user to enter custom configurations
    * _E.g. Static IP settings,  netmask, etc._
+ Keep copies of original configuration files for an option to uninstall/undo changes.
