
def automagic_install(default_settings_d):
    # TODO: create automagic installation logic
    pass


def wizard_install():
    # Import the configuration menus for IP, hostapd, and dnsmasq
    from menu.wizard_main_menu import menu_wizard_ip
    from menu.wizard_main_menu import menu_wizard_hostapd
    from menu._dnsmasq_menu import menu_wizard_dnsmasq

    # IP configuration
    ip_config_d = menu_wizard_ip()
    
    # hostapd configuration 
    ap_config_d = menu_wizard_hostapd()

    # dnsmasq configuration
    dns_config_d = menu_wizard_dnsmasq(ip_config_d)
