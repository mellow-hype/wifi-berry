from .config import dnsmasq_conf_default_d
from .config import hostapd_conf_default_d
from .config import ip_conf_default_d
from .config import BerryInit
from .config import BerryConfig


def automagic_install(
    ip_settings=ip_conf_default_d,
    ap_settings=hostapd_conf_default_d,
    dns_settings=dnsmasq_conf_default_d):
    
    # Create an instance of Init and Install classes
    init = BerryInit()
    config = BerryConfig()

    # Install dependencies
    init.dep_install()

    # Modify dhcpcd.conf to ignore selected interface
    init.mod_dhcpcd(ap_settings['interface'])

    # Configure static IP settings @ /etc/network/interfaces
    config.ipconf(ip_settings)

    # Restart dhcpcd and reload config for interface
    init.service_reload()

    # Configure hostapd @ /etc/hostapd/hostapd.conf
    config.hostapd_conf(ap_settings)

    # Configure dnsmasq @ /etc/dnsmasq.conf
    config.dnsmasq_conf(dns_settings)

    # Enable IPv4 forwarding and configure NAT
    init.ipv4_forward()
    init.net_conf()
    


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
