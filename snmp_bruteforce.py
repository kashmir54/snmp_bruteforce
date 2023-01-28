from pysnmp.hlapi import *
import sys
import argparse
from tqdm import tqdm
from functools import partial
import tqdm.notebook as tq

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def bruteforce_communities(wordlist, snmp_version, ip, port, timeout):

    v_arg = 1 if '2c' == snmp_version else 0

    print(f'Starting SNMPv{snmp_version} bruteforce')

    with open(wordlist, 'r') as in_file:
        communities = in_file.read().splitlines()


    for com in tqdm(communities):

        iterator = getCmd(
            SnmpEngine(),
            CommunityData(com, mpModel=v_arg),
            UdpTransportTarget((ip, port), timeout=timeout, retries=0),
            ContextData(),
            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))
        )

        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

        if errorIndication:
            pass
            # print(errorIndication)

        elif errorStatus:
            pass
            #print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            tqdm.write(f"Found community name {bcolors.BOLD}{bcolors.OKGREEN}{com}{bcolors.ENDC} !")
            for varBind in varBinds:
                tqdm.write(' = '.join([x.prettyPrint() for x in varBind]))


def main():

    # Command example
    # python3 snmp_bruteforce.py -w /usr/share/wordlists/SecLists/Discovery/SNMP/common-snmp-community-strings.txt -i 10.129.228.102 -t 1
    parser = argparse.ArgumentParser(description='SNMP community bruteforce by kashmir54')

    parser.add_argument('--wordlist', '-w', action="store", required=True, help='Wordlist with usual community names')
    parser.add_argument('--ip', '-i', action="store", required=True, help='Target IP')

    parser.add_argument('--snmp-version', '-v', action='store', default='2c', help='SNMP Version to use (1, [2c])')
    parser.add_argument('--port', '-p', action="store", default=161, help='Target port [161]')
    parser.add_argument('--timeout', '-t', action="store", default=2, help='Timeout for the SNMP calls [2]')

    myargs = parser.parse_args()
    
    file = myargs.wordlist
    version = myargs.snmp_version
    ip = myargs.ip
    port = myargs.port
    timeout = int(myargs.timeout)

    bruteforce_communities(file, version, ip, port, timeout)


if __name__ == "__main__":
    main()
