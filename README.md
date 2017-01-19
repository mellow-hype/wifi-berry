# WifiBerry - Raspberry Pi Wireless AP, Automated

## Introduction
This script will automate the process of configuring a Raspberry Pi 3 to serve as a wireless AP. It assumes a stock install of Raspbian Jessie.

## Requirements
Before running the script, you should have the Pi plugged into a monitor with a keyboard and an ethernet connection to the Internet. It is not possible to run the script over the network as it will disable the wireless interface. It may be possible to do it over the ethernet connection but this has not been tested so far.

## Status
Currently a work in progress. Not functional as of yet, but close.

## TODO
+ Automagic install mode prompts and logic
+ dnsmasq configuring menu (started)
+ Wizard install mode functions

## Goals
These are some general goals for the script:
+ Provide a default autoconfig option that only requires the user to pass the name of the new wireless AP as a command-line argument
+ Provide a custom interactive mode that steps through the process and allows the user to enter custom configurations
    * _E.g. Static IP settings,  netmask, etc._
+ Keep copies of original configuration files for an option to uninstall/undo changes.


