from xml.dom import minidom
from optparse import OptionParser
import os.path

# Option Parser Menu
parser = OptionParser(usage="usage: %prog [options] -f (filename.xml)",
                          version="%prog 1.0")
parser.add_option("-f", "--file",
                action="store",
                dest="xmlfile",
                # default=False,
                 help="The XML file exported from PDF")

(options, args) = parser.parse_args()

# Global Variables from Parser Menu
xmlFilename = options.xmlfile

# Read the XML Document
xmldoc = minidom.parse(xmlFilename)

# Pull the XML Information from the XML Document
def xmlElement(xmlobject):
    xmlElement = xmldoc.getElementsByTagName(xmlobject)[0].firstChild.data
    return xmlElement

# EXAMPLE ROUTER CONFIGURATION
def routerConfig():
    # ----------------------------------------------------------------------------------------------
    # ------------------------------------ Router Configuration ------------------------------------
    # ----------------------------------------------------------------------------------------------
    routerCommands = [
        '!', # ----------------------- System Configuration -----------------------
        'hostname ' + xmlElement("routerHostname"),
        '!',
        'enable password ' + xmlElement("routerPassword"),
        'enable secret ' + xmlElement("routerSecretPassword"),
        '!',
        'line vty 0 4',
        'password ' + xmlElement("routerVirtualTerminalPassword"),
        'no snmp-server',
        'exit',
        '!',
        'interface GigabitEthernet0',
        'no shutdown',
        'ip address ' + xmlElement("routerManagementIP") + ' ' + xmlElement("routerManagementNetmask"),
        'exit',
        '!',
        'interface Vlan1',
        'shutdown',
        'no ip address',

        '!', # --------------------------- Default Route ---------------------------
        'ip route 0.0.0.0 0.0.0.0 GigabitEthernet0/0/1',

        '!', # ------------------------- SSH Configuration -------------------------
        'ip domain name ' + xmlElement("DomainName"),
        'crypto key generate rsa',
        'y',
        xmlElement("routerHostname") + '.' + xmlElement("DomainName"),
        '1024',
        'line vty 0 4',
        'transport input SSH',
        'exit',
        'username admin priviledge 15 secret 0 ' + xmlElement("routerSecretPassword"),
        'line vity 0 4',
        'login local',
        'exit',

        '!', # ------------------- Spanning Tree Configuration --------------------
        'spanning-tree mode rapid-pvst',
        'spanning-tree vlan 1-4094 priority 4096',

        '!', # ------------------------ VLAN Configuration ------------------------
        'vlan 2',
        'name Native-VLAN',
        '!',
        'vlan 200',
        'name Client-Access-VLAN',
        '!',
        'vlan 201',
        'name Management-VLAN',
        '!',
        'vlan 250',
        'name Cluster-VLAN',
        '!',
        'vlan 275',
        'name LiveMigration-VLAN',
        '!',
        'vlan 300',
        'name iSCSI-A-VLAN',
        '!',
        'vlan 301',
        'name iSCSI-B-VLAN',
        'exit',

        '!', # ------------------ NetApp FAS MGMT Configuration -------------------
        'interface GigabitEthernet0/1/0',
        'description ' + xmlElement("netAppHostname") + '-01:e0M',
        'switchport access vlan 201',
        'switchport mode access',
        'load-interval 30',
        'spanning-tree portfast',
        'exit',
        '!',
        'interface GigabitEthernet0/2/0',
        'description ' + xmlElement("netAppHostname") + '-02:e0M',
        'switchport access vlan 201',
        'switchport mode access',
        'load-interval 30',
        'spanning-tree portfast',
        'exit',

        '!', # ------------------ NetApp FAS DATA Configuration -------------------
        'interface GigabitEthernet0/1/1',
        'description ' + xmlElement("netAppHostname") + '-01:e0c',
        'switchport trunk native vlan 2',
        'switchport trunk allowed vlan 201,300,301',
        'switchport mode trunk',
        'load-interval 30',
        'exit',
        '!',
        'interface GigabitEthernet0/2/1',
        'description ' + xmlElement("netAppHostname") + '-02:e0c',
        'switchport trunk native vlan 2',
        'switchport trunk allowed vlan 201,300,301',
        'switchport mode trunk',
        'load-interval 30',
        'exit',

        '!', # ------------------ WAN IP Address Configuration -------------------
        'interface GigabitEthernet0/0/1',
        'description WAN Connection to NRP',
        'ip address ' + xmlElement("IsrWanIP") + ' ' + xmlElement("IsrWanNetmask"),
        'media-type rj45',
        'negotiation auto',
        'no shutdown',
        'exit',

        '!', # ------------------- VLAN Interface Configuration ------------------
        'interface Vlan200',
        'description Client_Access-' + xmlElement("clientAccessNetmask"),
        'ip address ' + xmlElement("clientAccessIP") + ' ' + xmlElement("clientAccessNetmask"),
        'ip nat inside',
        'no shutdown',
        '!',
        'interface Vlan201',
        'description Mgmt-' + xmlElement("Management_Netmask"),
        'ip address ' + xmlElement("Management_NW_IP_ISR") + ' ' + xmlElement("Management_Netmask"),
        'no shutdown',

        '!', # -------------------- NTP Server Configuration ---------------------
        'ntp server vrf Mgmt-intf ' + xmlElement("ntpServerIP"),
        'ntp source GigabitEthernet0',
        'ntp master 3',

        '!', # ---------------- PnP Server @ SP Core Configuration ----------------
        'ip http client source-interface Vlan200',
        'pnp profile ztd',
        ' transport http ipv4 ' + xmlElement("pnpServerIP") + ' port 80',
        'exit',

        '!', # --------------------- Applying Security License ---------------------
        'license boot level sec',
        'end',
        'copy running-config startup-config',
        '!'
    ]

    # Create the Router Configuration based on the XML's input.
    file = open("router.cfg","w")

    count = 0
    while (count < len(routerCommands)):
        print(routerCommands[count])
        file.write(routerCommands[count]+"\n")
        count = count + 1

    file.close()

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exists!" % arg)
    else:
        return open(arg, 'r')

def main():
    routerConfig()

if __name__ == "__main__":
    main()