from scapy.all import *

def print_packets(packet):
    
    if packet[ARP].op == 1:
        return('Request: {} is asking about {}.'.format(
            packet[ARP].psrc, packet[ARP].pdst))

    elif packet[ARP].op == 2:
        return('Response: {} is at {}'.format(
            packet[ARP].hwsrc, packet[ARP].psrc))
    else:
        return('Unexpected Response')

sniff(prn=print_packets, filter='arp', store=0, count=0, timeout=300)
