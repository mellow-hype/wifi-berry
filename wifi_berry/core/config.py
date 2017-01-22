# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
# Core Functions + Definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import string

# OTHERS
iface = 'wlan0'


# DEFAULT CONFIGURATION VALUES
ip_conf_default_d = {
    'ip': '172.24.1.1',
    'netmask': '255.255.255.0',
    'network': '172.24.1.0',
    'broadcast': '172.24.1.255'
}

hostapd_conf_default_d = {
    'interface': 'wlan0',
    'ssid': 'APname',
    'channel': 'channel=6',
    'passphrase': 'raspberry1'
}

dnsmasq_conf_default_d = {
    'interface': 'wlan0',
    'upstream': '8.8.8.8',
    'dhcp-string': '172.24.1.50,172.24.1.150,12h'
}


# --------------------------------------------------------------------------- #
# Initialization Class: these functions are used by both Automagic and Wizard 
# mode for initialization tasks.
# --------------------------------------------------------------------------- #

class BerryInit:

    # Save original configs for uninstall
    def keep_orig(file_path):
        from subprocess import call
        new_name = file_path + '.orig'
        call(["mv", file_path, new_name])
        print("Saved original configuration file as " + new_name)
        return new_name


    # Install hostapd and dnsmasq
    def dep_install():
        from subprocess import check_output
        from subprocess import STDOUT
        from subprocess import CalledProcessError
        try:
            print("Installing dnsmasq and hostapd...")
            check_output(
                ["sudo", "apt-get", "install", "dnsmasq", "hostapd"], stderr=STDOUT
                )
        except CalledProcessError as e:
            print("Error: installation failed.\n", e.output)
        else:
            print("Dependency installation completed successfully")


    # Configure dhcpcd
    def mod_dhcpcd(iface):
        dDhcpcdConf = '/etc/dhcpcd.conf'
        keep_orig(dDhcpcdConf)
        # append 'denyinterfaces wlan0' to the end of file
        with open(dDhcpcdConf, "a") as dhcpcd_conf:
            dhcpcd_conf.write("\ndenyinterfaces " + iface + "\n")
        dhcpcd_conf.close()
        print("Modified /etc/dhcpcd.conf.")


    # Reload dhcpcd and bring wlan0 down and then up to reload config
    def service_reload():
        from subprocess import call
        print("Restarting dhcpcd and reloading interface configuration...")
        call(["sudo", "service", "dhcpcd", "restart"])
        call(["sudo", "ifdown", iface])
        call(["sudo", "ifup", iface])
        print("Service reload successful.")


    # enable IPv4 forwarding
    def ipv4_forward():
        sysctl = '/etc/sysctl.conf'
        orig = '#net.ipv4.ip_forward=1'
        f_original = open((keep_orig(sysctl)), 'r')
        f_new = open(sysctl, 'w')
        for line in f_original:
            f_new.write(line.replace(orig, orig[1:]))
            print("Wrote changes to /etc/sysctl.conf.")
        f_original.close()
        f_new.close()


    # iptables nat config
    def net_conf():
        # Import the subprocess.call() function.
        from subprocess import call
        dRCLocal = '/etc/rc.local'

        # Configure NAT and port forwarding between interfaces.
        call([
            "sudo", "iptables", "-t", "nat", "-A",
            "POSTROUTING", "-o", "eth0", "-j", "MASQUERADE"
            ])
        call([
            "sudo", "iptables", "-A", "FORWARD", "-i", "eth0", "-o",
            "wlan0", "-m", "state", "--state", "RELATED,ESTABLISHED",
            "-j", "ACCEPT"
            ])
        call([
            "sudo", "iptables", "-A", "FORWARD", "-i",
            "wlan0", "-o", "eth0", "-j", "ACCEPT"
            ])

        # Save iptables configuration for persistence after reboot.
        call(["sudo", "sh", "-c", "iptables-save < /etc/iptables.ipv4.nat"])

        # Modify /etc/rc.local so it loads our saved iptables settings upon reboot.
        reader = open((keep_orig(dRCLocal)), 'r')
        writer = open(dRCLocal, 'w')

        # replace existing 'exit 0' in file with iptables-restore
        for line in reader:
            writer.write(line.replace(
                'exit 0', 'iptables-restore < /etc/iptables.ipv4.nat'
                ))

        # move position to eof and append 'exit 0' string
        writer.seek(0, 2)
        writer.write('\nexit 0')

        # close up
        reader.close()
        writer.close()


# --------------------------------------------------------------------------- #
# Install class that will handle modifying the config files with the
# given values if present, otherwise uses the default settings laid out in the
# dictionaries at the top of this file.
# --------------------------------------------------------------------------- #
class BerryConfig:
    '''Main functions for pushing settings to dnsmasq, IP, and hostapd'''

    # Static IP configuration @ /etc/network/interfaces
    def ipconf(settings_d=ip_conf_default_d):
        '''Modify /etc/network/interfaces with default settings if no\
             settings dict passed.''' 
        # open provided config file for reading and the user's for writing
        sIfaceConf = 'config/iface.conf'
        dIfaceConf = '/etc/network/interfaces'
        f_orig = open(sHostapdConf, 'r')
        f_new = open(dHostapdConf, 'w')

        # iterate through each line searching for default values and replacing
        # with custom values
        for line in f_orig:
            # modify address value
            if ip_conf_default_d['address'] in line:
                f_new.write(line.replace(
                    ip_conf_default_d['address'], settings_d['address']))
            # modify netmask value
            elif ip_conf_default_d['netmask'] in line:
                f_new.write(line.replace(
                    ip_conf_default_d['netmask'], settings_d['netmask']))
            # modify network address value
            elif ip_conf_default_d['network'] in line:
                f_new.write(line.replace(
                    ip_conf_default_d['network'], ip_converter(
                                    settings_d['network'], '0')))
            # modify broadcast value
            elif ip_conf_default_d['broadcast'] in line:
                f_new.write(line.replace(
                    ip_conf_default_d['broadcast'], ip_converter(
                                    settings_d['broadcast'], '255')))
            # if nothing to modify, write the line
            else:
                f_new.write(line)

        # close up
        f_orig.close()
        f_new.close()

    
    # Convert last bit of the input IP to format it as gateway, broadcast, etc
    def ip_converter(ip_addr, finbit):
        '''"Change the last bit of an IP to format as gateway, broadcast, etc.\
            (ip_addr = IP to modify, finbit = value for final field in IP)'''

        cust_ip = list(ip_addr)
        cust_ip[(len(ip_addr) - 1)] = finbit
        fin = ''
        return fin.join(cust_ip)


    # dnsmasq configuration @ /etc/dnsmasq.conf
    def dnsmasq_conf(settings_d=dnsmasq_conf_default_d):
        '''Modify /etc/dnsmasq.conf with default settings if no settings dict \
            passed.''' 
        # open source config for reading and dst config for writing
        dDnsmasqConf = '/etc/dnsmasq.conf'
        sDnsmasqConf = 'config/dnsmasq.conf'
        f_orig = open(sDnsmasqConf, 'r')
        f_new = open(dDnsmasqConf, 'w')

        # iterate through each line searching for default values and replacing with
        # custom values
        for line in f_orig:
            # modify interface
            if dnsmasq_conf_default_d['interface'] in line:
                f_new.write(line.replace(dnsmasq_conf_default_d['interface'], iface_in))
            # modify upstream DNS server
            elif dnsmasq_conf_default_d['upstream'] in line:
                f_new.write(line.replace(dnsmasq_conf_default_d['upstream'], upstr))
            # modify dhcp range and least time limit
            elif dnsmasq_conf_default_d['dhcp-string'] in line:
                f_new.write(line.replace(dnsmasq_conf_default_d['dhcp-string'], settings_d['dhcp-string']))
            else:
                f_new.write(line)

        # close up
        f_new.close()
        f_orig.close()



    # Access point (hostapd) configuration at /etc/hostapd/hostapd.conf
    def hostapd_conf(settings_d=hostapd_conf_default_d):
        '''Modify /etc/hostapd.conf and /etc/default/hostapd with default settings if no \
            settings dict passed.'''
        # open source config for reading and dst config for writing
        sHostapdConf = 'config/hostapd.conf'
        dHostapdConf = '/etc/hostapd/hostapd.conf'
        f_orig = open(sHostapdConf, 'r')
        f_new = open(dHostapdConf, 'w')

        # iterate through each line searching for default values and replacing with
        # custom values
        for line in f_orig:
            if hostapd_conf_default_d['interface'] in line:
                f_new.write(line.replace(hostapd_conf_default_d['iface'], iface_in))
            elif hostapd_conf_default_d['ssid'] in line:
                f_new.write(line.replace(hostapd_conf_default_d['ssid'], ssid))
            elif hostapd_conf_default_d['chan'] in line:
                f_new.write(line.replace(hostapd_conf_default_d['channel'], chan))
            elif hostapd_conf_default_d['passphrase'] in line:
                f_new.write(line.replace(hostapd_conf_default_d['passphrase'], settings_d['passphrase']))
            else:
                f_new.write(line)

        # close up
        f_orig.close()
        f_new.close()

        # edit /etc/default/hostapd to point daemon to our config:
        # we use keep_orig() to make a new copy of the existing config on the system and open it for reading and 
        # open the old existing copy to replace the desired string
        hostapdDefault = '/etc/default/hostapd'
        daemonStr = '#DAEMON_CONF=""'
        daemonStrX = 'DAEMON_CONF="/etc/hostapd/hostapd.conf"'
        f_original = open(keep_orig(hostapdDefault), 'r')
        f_new = open(hostapdDefault, 'w')
        print("Editing /etc/default/hostapd...")
        for line in f_original:
            f_new.write(line.replace(daemonStr, daemonStrX))
        f_original.close()
        f_new.close()
        print("Done editing /etc/default/hostapd.\n hostapd configuration complete.")

# --------------------------------------------------------------------------- #
# Wizard Mode Input utilities: auxiliary functions for gathering input
# --------------------------------------------------------------------------- #
# Get desired SSID
def get_ssid():
    ''' Prompt the user for the desired SSID and do length checking.
        Returns the new SSID, in a str() object.'''

    # Declare a prompt string.
    prompt = 'Please enter the SSID for the new access point: '

    while True:
        # Prompt the user for a desired SSID, and read the input.
        new_ssid_str = input(prompt)
        # Enforce a minimum length of 1 character, maximum of 62 characters.
        if len(new_ssid_str) < 1 or len(new_ssid_str) > 62:
            print("SSID has min. length of 1 character and max length of \
                                63 characters. Please try again.")
            continue
        else:
            # Return the AP's new SSID.
            print("New AP's SSID will be: " + new_ssid_str)
            return new_ssid_str


# Get the desired channel for the AP
def get_channel():
    '''Prompt the user for the desired channel and do length/type checking.
        Returns new channel, stored in an int() object.'''

    # Declare a prompt string.
    prompt = 'Enter a channel for the new access point [between 1-13] '

    while True:
        # Read an input string, check that it is a valid channel number.
        chan = input(prompt)

        # Raise a ValueError exception if the integer is not valid.
        try:
            int(chan) < 1 or int(chan) > 13
        except ValueError:
            print("Error: Channel must be a number between 1-13.")
            continue

        # Return the integer if it is a valid channel number.
        if int(chan) < 1 or int(chan) > 13:
            print("Error: Channel not within min/max limits.")
            continue
        else:
            print("The new channel is " + chan)
            return chan


# Find available network interfaces
def available_iface():
    '''Parse output of /proc/net/dev for lines containing wireless devices. Get the name of the
        device and returns a list of names.'''
    iface_l = [0]
    for line in open('/proc/net/dev', 'r'):
        if 'wlan' in line:
            for index, char in enumerate(line):
                x = 0
                if char == ':':
                    iface_l[x] = line[:index]
    return iface_l

# Prompt user for desired AP passphrase with verification
def pass_prompt():
    '''Prompt for the new WPA2 passphrase of the new access point.'''
    prompt = 'Desired passphrase for access point: '
    prompt2 = 'Repeat password for verification: '
    pass_1 = ''
    while len(pass_1) < 8:
        from getpass import getpass
        pass_1 = getpass(prompt)
        # enforce min passphrase length
        if len(pass_1) < 8:
            print("[Error]: Passphrase must be at least 8 characters.")
            continue
        # enforce max passphrase length (wpa2 sets max at 63 chars)
        elif len(pass_1) > 63:
            print("[Error]: Passphrase must be less than 64 characters.")
            continue
        # enforce passphrase contain only printable characters
        elif all(c in string.printable for c in pass_1) is False:
            print("[Error]: Passphrase can only contain printable characters.")
            continue
        else:
            # ask for passphrase again for verification
            pass_2 = getpass(prompt2)
            if pass_2 == pass_1:
                return pass_2
            else:
                print("[Error]: Passphrases do not match. Please try again.")
                pass_1 = ''
                continue