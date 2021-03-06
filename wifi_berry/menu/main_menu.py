#!/usr/bin/env python
# --------------------------------------------------------------------------- #
# This is the main file for the CLI interface.
# NOTE: If this script is invoked directly, the main menu will be presented.
# NOTE: To use, import this script and call the main() function.
# --------------------------------------------------------------------------- #

# Import the Menu3 module.
import menu3

# Import wizard mode menus and final menu
from .wizard_main_menu import menu_wizard_main, final_menu
from wifi_berry.core.config import BerryInit, BerryConfig


def menu_main():
    """This function will run present the main menu to the user and
        settings to be used for installation."""

    # Define the variables that are needed for the menu object.
    menu_main_info_str = '[Main Menu]'
    menu_main_title_str = '[WifiBerry Setup: Main Menu] (Q to quit.)'
    menu_main_choices_l = [
        'Automagic Install',
        'Wizard Install',
    ]
    menu_main_prompt_str = '[Selection]: '

    # Instantiate and configure the menu object.
    menu_main = menu3.Menu(True)
    menu_main.info(menu_main_info_str)

    # Present the menu to the user, until they exit.
    while True:
        menu_main_return = menu_main.menu(title=menu_main_title_str,
                                                choices=menu_main_choices_l,
                                                prompt=menu_main_prompt_str)

        # Create a dictionary of each selection and its corresponding function,
        # where the key is the menu choice text and the value is a function
        # pointer.
        menu_main_selections_d = {
            'Wizard Install': menu_wizard_main,
            'Exit': quit
        }

        # Access the dictionary by finding the menu choice that was selected.
        if (menu_main_choices_l[int(menu_main_return)-1] == 'Automagic Install'):
            return
        
        # If selected, call wizard_main_menu, save it's return, and pass the settings
        # dict back to main() to update the instance's settings attribute.
        elif (menu_main_choices_l[int(menu_main_return)-1] == 'Wizard Install'):
            settings = dict(menu_wizard_main)
            return settings


# Define the main runtime function.
def main():
    """This is the main function that we will call, to initiate the menu."""

    # Initialize objects
    init = BerryInit()
    config = BerryConfig()

    # Invoke the main menu and update settings attribute with returned
    # dictionary
    try:
        config.settings.update(menu_main())
    except TypeError:
        pass

    # Confirm final settings
    final_menu(config.settings)

    # Run installation procedure

    init.dep_install()  # install dependencies
    init.mod_dhcpcd(config.settings['interface'])   # modify dhcpcd.conf  
    config.ipconf()     # static IP configuration
    init.service_reload(config.settings['interface']) # reload dhcpcd and iface
    config.hostapd_conf()   # configure hostapd
    config.dnsmasq_conf()   # configure dnsmasq
    init.ipv4_forward()     # enable IPv4 forwarding
    init.net_conf()         # configure the NAT
    init.enable_services()  # enable services

    # Perform cleanup here.
    print('\n\nInstallation complete. You should reboot the system to \
    ensure settings are persistent. The access point should now be \
    visible as' + config.settings["ssid"] + '.\n\n')

    return

# If this script is invoked directly, run the main menu.
if __name__ == '__main__':
    main()
