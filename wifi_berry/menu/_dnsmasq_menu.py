# Import the menu module.
import menu3

# Auxiliary functions:
# --------------------------------------------------------------------------- #
# This section includes helper functions for input gathering, for the menu.
# --------------------------------------------------------------------------- #
def dhcp_ranger(network):
    '''Get DHCP settings'''
    
    start_str = 'Start of range(1-254): '
    start = input(start_str)

    end_str = 'End of range(1-254) '
    end = input(end_str)

    lease_str = 'Lease time (hrs): '
    lease = input(lease_str)

    try:
        if int(end) <= int(start):
            print('End of range must be greater than start. Retry')
            dhcp_ranger(network)
        elif int(lease) < 1:
            print('Lease time must be at least one hour. Retry')
            dhcp_ranger(network)
    except TypeError:
        print('Wrong input type. Only numeric characters are needed.')
        dhcp_ranger(network)

    dhcp_string = \
        network[:len(network)-1] + str(start) + ',' + network[:len(network)-1] +\
            str(end) + ',' + lease + 'h'
    return dhcp_string


# Menus:
# --------------------------------------------------------------------------- #
# Main dnsmasq configuration menus
# --------------------------------------------------------------------------- #

# dnsmasq upstream DNS provider configuration menu
def dnsmasq_upstream_menu():
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

        return dnsmasq_upstream_menu_selections_d[
            dnsmasq_upstream_menu_choices_l[int(dnsmasq_upstream_menu_menu_return)-1]
        ]



# Main dnsmasq configuration menu
def menu_wizard_dnsmasq(presets_d):
    '''dnsmasq configuration main menu'''

    # Import the default dnsmasq config values
    from ..core.config import dnsmasq_conf_default_d
    dnsmasq_conf_d = dnsmasq_conf_default_d

    # Set the interface value from presets_d
    dnsmasq_conf_d["iface"] = presets_d["iface"]

    # Define the variables that are needed for the configuration menu.
    main_dnsmasq_info_str = '[Configure DNS and DHCP settings]'
    main_dnsmasq_title_str = '[dnsmasq Configuration Menu]'

    # Define a list of choices available to the user
    main_dnsmasq_choices_l = [
        'Upstream DNS',
        'DHCP Settings',
        'Done'
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
        # dnsmasq_conf_d (look in core/core.py to find its keys:values)
        if main_dnsmasq_choices_l[int(main_dnsmasq_return)-1] == "Upstream DNS":
            dnsmasq_conf_d["upstream"] = \
                main_dnsmasq_selections_d["Upstream DNS"]()
        elif main_dnsmasq_choices_l[int(main_dnsmasq_return)-1] == "DHCP Settings":
            dnsmasq_conf_d["dhcp-string"] = \
                main_dnsmasq_selections_d["DHCP Settings"](presets_d["network"])
        else:
            return dnsmasq_conf_d
