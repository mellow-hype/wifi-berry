# --------------------------------------------------------------------------- #
# These are the main Wizard mode menus
# --------------------------------------------------------------------------- #
# Import the menu module.
import menu3

# Config Menu(s)
# --------------------------------------------------------------------------- #
# This section includes the configuration menu and the specific
# configuration child menus, for editing specific configurations.
# --------------------------------------------------------------------------- #

# IP configuration menu
def menu_wizard_ip(settings_d):
    """This is the configuration menu for IP settings."""

    # Set info string and menu title
    my_menu_wizard_ip_info_str = '[Configure the static IP settings]'
    my_menu_wizard_ip_title_str = '[IP Configuration]'

    # This dict will contains key-value pairs for the menu items.
    # This is how we will reference the data.
    my_menu_wizard_ip_choices_d = {
        'Private IP': '172.24.1.1',
        'Netmask': '255.255.255.0',
    }

    # Prompt and return choice strings for the menu.
    my_menu_wizard_ip_prompt_str = '[IP]: '
    my_menu_wizard_ip_return_choice_str = 'Done'

    # Instantiate and configure the menu object.
    my_menu_wizard = menu3.Menu(ALLOW_QUIT=True)
    my_menu_wizard.info(my_menu_wizard_ip_info_str)

    # Present the menu to the user; my_menu_wizard_ip_return is a dictionary
    # that contains the key-value pairs for the menu options.
    while True:
        my_menu_wizard_ip_return = my_menu_wizard.config_menu(
            title=my_menu_wizard_ip_title_str,
            config=my_menu_wizard_ip_choices_d,
            prompt=my_menu_wizard_ip_prompt_str,
            return_choice=my_menu_wizard_ip_return_choice_str
        )

        # Import functions for checking IP addresses
        from ipaddress import IPv4Address, IPv4Network
        from ipaddress import NetmaskValueError, AddressValueError

        # Import the IP converter function to transform IPs to different formats
        from ..core.config import ip_converter

        # Private IP/netmask validation
        try:
            # check if the IP is an invalid private IP address
            if IPv4Address(
                  my_menu_wizard_ip_return['Private IP']).is_private is False:
                print("Please enter a valid private IP address.")
                continue
            elif IPv4Address(my_menu_wizard_ip_return['Private IP']) is False:
                raise AddressValueError
            # check if the netmask is valid
            elif IPv4Network(
                 my_menu_wizard_ip_return['Private IP'] + "/" +
                    my_menu_wizard_ip_return['Netmask'], strict=False
            ) is False:
                raise NetmaskValueError
            else:
                # Save values to our settings dict and pass it back to the parent
                # function.
                settings_d['ip'] = \
                    ip_converter(my_menu_wizard_ip_return['Private IP'], '1')
                settings_d['netmask'] = my_menu_wizard_ip_return['Netmask']
                settings_d['network'] = \
                    ip_converter(settings_d['ip', '0'])
                settings_d['broadcast'] = \
                    ip_converter(settings_d['ip'], '255')
                return settings_d
        except NetmaskValueError:
            print("Please enter a valid netmask.", NetmaskValueError)
        except AddressValueError:
            print("Please enter a valid IP address.")


def menu_wizard_hostapd_interface():
    """This menu will display available wireless interfaces and allow the user
    to select one. Its only argument is a list of available interfaces
    generated by menu.core.core.available_iface."""

    menu_wizard_hostapd_interface_info_s = \
        '[Select the desired wireless interface you wish to use.'
    menu_wizard_hostapd_interface_title_s = \
        '[Wireless Interface Selection]'
    menu_wizard_hostapd_interface_prompt_s = \
        '[interface selection]: '

    # Find a list of available interfaces, using
    # the function defined in the core module.
    from ..core.config import available_iface
    menu_wizard_hostapd_interface_choices_l = available_iface()

    # Instantiate and configure the menu
    menu_wizard_hostapd_interface_menu = menu3.Menu(ALLOW_QUIT=True)
    menu_wizard_hostapd_interface_menu.info(
        menu_wizard_hostapd_interface_info_s)

    # Initialize an empty dictionary for storing
    # the HostAPD interface selections.
    menu_wizard_hostapd_interface_selections_d = {}

    # Populate the dict with the interfaces
    for i in range(len(menu_wizard_hostapd_interface_choices_l)):
        menu_wizard_hostapd_interface_selections_d[str(i)] = \
            menu_wizard_hostapd_interface_choices_l[i]

    # Disply the menu
    while True:
        # generate the menu using our settings
        menu_wizard_hostapd_interface_return = \
            menu_wizard_hostapd_interface_menu.menu(
                title=menu_wizard_hostapd_interface_title_s,
                choices=menu_wizard_hostapd_interface_choices_l,
                prompt=menu_wizard_hostapd_interface_prompt_s)

        # Selection handling
        return menu_wizard_hostapd_interface_selections_d[str(
            menu_wizard_hostapd_interface_return-1)]


# hostapd configuration menu
def menu_wizard_hostapd(settings_d):
    '''This is the configuration menu for hostapd settings.'''

    # Declare an info string for the menu.
    menu_wizard_hostapd_info_str = \
        '[hostapd configuration: settings for the access point.]'

    # Declare title and prompt strings for the menu.
    menu_wizard_hostapd_title_str = '[Access Point Configuration]'
    menu_wizard_hostapd_prompt_str = '[hostapd config]: '

    # Declare a list of hostapd menu choices.
    menu_wizard_hostapd_choices_l = [
        'Interface',
        'SSID',
        'Channel',
        'Passphrase',
        'Done'
    ]

    # Instantiate and configure the menu object.
    menu_wizard_hostapd_menu = menu3.Menu(ALLOW_QUIT=True)
    menu_wizard_hostapd_menu.info(menu_wizard_hostapd_info_str)

    # Import the get_ssid(), pass_prompt(), and get_channel() functions
    from ..core.config import get_ssid, pass_prompt, get_channel

    # Present the menu to the user.
    while True:
        # Define the selections dictionary that point to the input handling
        # functions.
        menu_wizard_hostapd_selections_d = {
            'Interface': menu_wizard_hostapd_interface,
            'SSID': get_ssid,
            'Channel': get_channel,
            'Passphrase': pass_prompt,
        }

        # Initialize the menu object and save its return string.
        menu_wizard_hostapd_return = menu_wizard_hostapd_menu.menu(
            title=menu_wizard_hostapd_title_str,
            choices=menu_wizard_hostapd_choices_l,
            prompt=menu_wizard_hostapd_prompt_str,
        )

        # ----------------------------------------------------------------------
        # User selection handling:
        # ----------------------------------------------------------------------

        # Interface selection
        if menu_wizard_hostapd_choices_l[int(
                menu_wizard_hostapd_return)-1] == 'Interface':
            settings_d['interface'] = \
                menu_wizard_hostapd_selections_d[
                    menu_wizard_hostapd_choices_l[int(
                        menu_wizard_hostapd_return)-1]]()

        # SSID selection
        elif menu_wizard_hostapd_choices_l[
                int(menu_wizard_hostapd_return)-1] == 'SSID':
            # Assign the value that get_ssid()
            # returns to the settings dictionary.
            settings_d['ssid'] = menu_wizard_hostapd_selections_d[
                menu_wizard_hostapd_choices_l[int(
                    menu_wizard_hostapd_return)-1]]()

        # Channel selection
        elif menu_wizard_hostapd_choices_l[int(
                menu_wizard_hostapd_return)-1] == 'Channel':
            # Assign the get_channel() value to the settings dictionary.
            settings_d['channel'] = menu_wizard_hostapd_selections_d[
                menu_wizard_hostapd_choices_l[int(
                    menu_wizard_hostapd_return)-1]]()

        # Passphrase selection
        elif menu_wizard_hostapd_choices_l[int(
                menu_wizard_hostapd_return)-1] == 'Passphrase':
            # Assign the get_pass() value to the settings dictionary.
            settings_d['passphrase'] = \
                menu_wizard_hostapd_selections_d[
                    menu_wizard_hostapd_choices_l[int(
                        menu_wizard_hostapd_return)-1]]()

        # When done, return the settings dict
        # back to the calling function in wizard_install.
        elif (menu_wizard_hostapd_choices_l[
                int(menu_wizard_hostapd_return) - 1] == 'Done'):
            return settings_d


def menu_wizard_main(settings_d):
    """This is the main wizard menu. This menu contains further
        choices for selecting which configuration options to edit."""

    # Define the variables that are needed for the menu object, including
    # info and title strings, a choices list, and a prompt string.
    my_menu_wizard_info_str = '[Wizard Mode main configuration menu]'
    my_menu_wizard_title_str = '[Wizard Mode: Main Menu] (Q to quit.)'
    my_menu_wizard_prompt_str = '[Prompt]: '
    my_menu_wizard_choices_l = [
        'IP Configuration',
        'Access Point Configuration',
        'DNS Configuration',
        '',
        'Continue',
        'Return to Main Menu'
    ]


    # Instantiate and configure the menu object to allow quitting.
    my_menu_wizard = menu3.Menu(ALLOW_QUIT=True)
    my_menu_wizard.info(my_menu_wizard_info_str)

    # Present the menu to the user, repeating until they exit.
    while True:
        my_menu_wizard_return = my_menu_wizard.menu(
            title=my_menu_wizard_title_str,
            choices=my_menu_wizard_choices_l,
            prompt=my_menu_wizard_prompt_str)

        # Import the main dnsmasq menu function
        from ._dnsmasq_menu import menu_wizard_dnsmasq

        # Create a dictionary of each selection and its
        # corresponding function, where the key is the menu
        # choice text and the value is a function pointer.
        my_menu_wizard_selections_d = {
            'IP Configuration': menu_wizard_ip,
            'Access Point Configuration': menu_wizard_hostapd,
            'DNS Configuration': menu_wizard_dnsmasq
        }

        # Copy settings over to a dict
        settings_d = dict(settings_d)

        # Check if the return to main menu option was selected, otherwise
        # access the dictionary by finding the menu choice that was selected.
        # Return to parent menu
        if (my_menu_wizard_choices_l[
                int(my_menu_wizard_return)-1] == 'Return to Main Menu'):
            return

        # IP configuration menu
        elif (my_menu_wizard_choices_l[
                int(my_menu_wizard_return)-1] == 'IP Configuration'):
            settings_d.update(menu_wizard_ip(settings_d.copy()))

        # hostapd configuration menu
        elif (my_menu_wizard_choices_l[
                int(my_menu_wizard_return)-1] == 'Access Point Configuration'):
            settings_d.update(menu_wizard_hostapd(settings_d.copy()))
        
        # dnsmasq configuration menu
        elif (my_menu_wizard_choices_l[
                int(my_menu_wizard_return)-1] == 'DNS Configuration'):
            settings_d.update(menu_wizard_dnsmasq(settings_d.copy()))

        # Return the dict with the updated settings back to main_menu()
        elif (my_menu_wizard_choices_l[
                int(my_menu_wizard_return)-1] == 'Continue'):
            return settings_d


# Final menu to display settings and confirm configuration
def final_menu(settings):
    # Title, info, and prompt string for menu
    final_menu_info_str = '[Review and confirm settings for installation.]'
    final_menu_title_str = '[Confirm Installation]'
    final_menu_prompt_str = "[1: install / 2: cancel]: "
    
    # Display final settings and ask for confirmation
    final_menu_choices_l = [
        '-- Confirm and Install',
        '-- Cancel and return to main menu'
    ]

    # Instantiate and configure the menu object with option to quit
    final_menu_m = menu3.Menu(ALLOW_QUIT = True)
    final_menu_m.info(final_menu_info_str)

    # Display the menu until they exit
    while(True):
        # show current settings
        settings = dict(settings)
        for key, value in settings.items():
            print(key + ' : ' + value)
        
        # configure the menu object and save its returns
        final_menu_return = final_menu_m.menu(
            title=final_menu_title_str,
            choices=final_menu_choices_l,
            prompt=final_menu_prompt_str
        )

        if final_menu_return == 1:
            return
        else:
            menu_wizard_main(settings)


