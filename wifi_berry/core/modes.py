
def automagic_install(default_settings_d):
    # TODO: create automagic installation logic
    pass


def wizard_install():
    # Import the configuration menus for IP, hostapd, and dnsmasq
    from ..menu.wizard_main_menu import menu_wizard_ip
    from ..menu.wizard_main_menu import menu_wizard_hostapd
    from ..menu._dnsmasq_menu import menu_wizard_dnsmasq

    # -- Get IP configuration settings
    ip_config_d = menu_wizard_ip()
    # DEBUG: 
    print(ip_config_d)
    
    # -- Get hostapd configuration settings
    ap_config_d = menu_wizard_hostapd()
    # DEBUG: 
    print(ap_config_d)

    # -- Get dnsmasq configuration settings
    # Pass previously set values to dnsmasq menu function 
    dns_custom_d = {
        "network": ip_config_d["network"],
        "iface": ap_config_d["interface"]
        }

    dns_config_d = menu_wizard_dnsmasq(dns_custom_d)
