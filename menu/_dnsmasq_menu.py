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


# DNS providers list.
# NOTE: These are organized in order of priority, i.e.
# primary DNS server, followed by secondary server, etc.
Level31 = ["209.244.0.3", "209.244.0.4"]
Verisign = ["264.6.64.6", "64.6.65.6"]
Google3 = ["8.8.8.8", "8.8.4.4"]
DNSWATCH4 = ["84.200.69.80", "84.200.70.40"]
ComodoSecure = ["8.26.56.26", "8.20.247.20"]
OpenDNS = ["208.67.222.222", "208.67.220.220"]
DNS_Advantage = ["156.154.70.1", "156.154.71.1"]
NortonConnectSafe6 = ["199.85.126.10", "199.85.127.10"]
GreenTeamDNS7 = ["81.218.119.11", "209.88.198.133"]
SafeDNS8 = ["195.46.39.39", "195.46.39.40"]
OpenNIC9 = ["45.32.215.96", "104.238.153.178"]
SmartViper = ["208.76.50.50", "208.76.51.51"]
Dyn = ["216.146.35.35", "216.146.36.36"]
FreeDNS10 = ["37.235.1.174", "37.235.1.177"]
AlternateDNS11 = ["198.101.242.72", "23.253.163.53"]
YandexDNS12 = ["77.88.8.8", "77.88.8.1"]
censurfridns = ["91.239.100.100", "89.233.43.71"]
HurricaneElectric14 = ["74.82.42.42"]
puntCAT15 = ["109.69.8.51"]

# DNS providers dictionary. Place the IP lists defined above into a dictionary.
dns_d = {
    "Level31": Level31,
    "Verisign": Verisign,
    "Google": Google3,
    "DNS WATCH4": DNSWATCH4,
    "Comodo Secure DNS": ComodoSecure,
    "OpenDNS": OpenDNS,
    "DNS Advantage": DNS_Advantage,
    "Norton Connect Safe6": NortonConnectSafe6,
    "Green Team DNS7": GreenTeamDNS7,
    "Safe DNS8": SafeDNS8,
    "OpenNIC9": OpenNIC9,
    "SmartViper": SmartViper,
    "Dyn": Dyn,
    "Free DNS10": FreeDNS10,
    "Alternate DNS11": AlternateDNS11,
    "Yandex DNS12": YandexDNS12,
    "censurfridns": censurfridns,
    "HurricaneElectric14": HurricaneElectric14,
    "puntCAT15": puntCAT15
}


def dnsmasq_upstream_menu(ip_settings):
    '''This menu will present a list of possible upstream DNS
        providers for the user to select.'''

    # Declare info string and title for DNS menu
    dnsmasq_upstream_menu_info_str = '[Upstream DNS servers selection]'
    dnsmasq_upstream_menu_title_str = '[Available DNS Servers]'

    # Declare a list of choices available
    dnsmasq_upstream_menu_choices_l = list(dns_d.keys())

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

        # function to return the list of values based on selection
        def ret_selection(dns_selection):
            return dns_selection

        # NOTE: Use same method as in menu_wizard_hostapd_interface to get the
        # selection: generate a dictionary with numbers as keys and the choices
        # as values, etc.


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
