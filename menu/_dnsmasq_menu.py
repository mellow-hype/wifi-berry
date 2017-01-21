# Import the menu module.
import menu3

# Auxiliary functions:
# --------------------------------------------------------------------------- #
# This section includes helper functions for input gathering, for the menu.
# --------------------------------------------------------------------------- #
def dhcp_ranger():
    '''This function prompts the user for DHCP settings. After receiving
        a starting IP, and ending IP, and a lease time (hours),
        return the user's inputs as a joined string.'''
    start_str = 'Starting IP: '
    start_ip = input(start_str)

    end_str = 'Ending IP: '
    end_ip = input(end_str)

    lease_str = 'Lease time: '
    lease = input(lease_str)

    dhcp_settings = start_ip + ',' + end_ip + ',' + lease + 'h'
    return dhcp_settings


# Menus:
# --------------------------------------------------------------------------- #
# Main dnsmasq configuration menus
# --------------------------------------------------------------------------- #


# dnsmasq upstream DNS provider configuration menu
def dnsmasq_upstream_menu(ip_settings):
    '''This menu will present a list of possible upstream DNS
        providers for the user to select.'''

    # Declare info string and title for DNS menu
    dnsmasq_upstream_menu_info_str = '[Upstream DNS servers selection]'
    dnsmasq_upstream_menu_title_str = '[Available DNS Servers]'

    # Create selections dict 
    dnsmasq_upstream_menu_selections_d = {
        "Level31": "209.244.0.3",
        "Verisign": "264.6.64.6",
        "Google": "8.8.8.8",
        "DNS WATCH4": "84.200.69.80",
        "Comodo Secure DNS": "8.26.56.26",
        "OpenDNS": "208.67.222.222",
        "DNS Advantage": "156.154.70.1",
        "Norton Connect Safe6": "199.85.126.10",
        "Green Team DNS7": "81.218.119.11",
        "Safe DNS8": "195.46.39.39",
        "OpenNIC9": "45.32.215.96",
        "SmartViper": "208.76.50.50",
        "Dyn": "216.146.35.35",
        "Free DNS10": "37.235.1.174",
        "Alternate DNS11": "198.101.242.72",
        "Yandex DNS12": "77.88.8.8",
        "censurfridns": "91.239.100.100",
        "HurricaneElectric14": "74.82.42.42",
        "puntCAT15": "109.69.8.51"
    }

    # Fill our choices list using keys from selections
    dnsmasq_upstream_menu_choices_l = list(dnsmasq_upstream_menu_selections_d.keys())

    # Declare a prompt string for the menu
    dnsmasq_upstream_menu_prompt = 'DNS Selection: '

    # Instantiate and configure the menu object
    dnsmasq_upstream_menu_menu = menu3.Menu(ALLOW_QUIT=True)
    dnsmasq_upstream_menu_menu.info(
        dnsmasq_upstream_menu_info_str
        )

    while True:
        # display the menu to the user until they quit
        dnsmasq_upstream_menu_menu_return = \
            dnsmasq_upstream_menu_menu.menu(
                title=dnsmasq_upstream_menu_title_str,
                choices=dnsmasq_upstream_menu_choices_l,
                prompt=dnsmasq_upstream_menu_prompt
            )

        # NOTE: Use same method as in menu_wizard_hostapd_interface to get the
        # selection: generate a dictionary with numbers as keys and the choices
        # as values, etc.



        # 

# Main dnsmasq configuration menu
def menu_wizard_dnsmasq():
    '''This is the configuration menu for the dnsmasq settings.'''

    # Import the default dnsmasq config values
    from ..core.core import dnsmasq_conf_default_d

    # Define the variables that are needed for the configuration menu.
    main_dnsmasq_info_str = '[Configure DNS and DHCP settings]'
    main_dnsmasq_title_str = '[dnsmasq Configuration Menu]'

    # Define a list of choices available to the user
    main_dnsmasq_choices_l = [
        'Upstream DNS',
        "DHCP Settings"
    ]

    # Declare prompt and return strings for the dnsmasq menu.
    main_dnsmasq_prompt_str = '[dnsmasq config]: '

    # Instantiate and configure the menu object.
    main = menu3.Menu(ALLOW_QUIT=True)
    main.info(main_dnsmasq_info_str)

    while True:
        # Present the menu to the user and store the return value.
        main_dnsmasq_return = main.menu(
            title=main_dnsmasq_title_str,
            choices=main_dnsmasq_choices_l,
            prompt=main_dnsmasq_prompt_str,
        )

        # Declare a dictionary that link the selections to functions.
        main_dnsmasq_selections_d = {
            'Upstream DNS': dnsmasq_upstream_menu,
            'DHCP Settings': dhcp_ranger
        }

        # TODO: Selection handling -- check which option the user chose, call
        # the function, and save it's return to the appropriate key in
        # dnsmasq_conf_default_d (look in core/core.py to find its keys:values)

        # Use the user's return to match one of the choices and use that string
        # to as the key to the selections dict to call the appropriate function
        main_dnsmasq_selections_d[
            main_dnsmasq_choices_l[int(main_dnsmasq_return)-1]
            ]()

        # NOTE: This function should return dnsmasq_conf_default_d when done.

        # XXX DEBUG: Print the return value and the config dictionary.
        print(main_dnsmasq_return)
