#!/bin/env python3

# Import libraries
import sys
import argparse
import time
from icmplib import traceroute, ping

# Set up command line parser
parser = argparse.ArgumentParser(description='Format: check-path.py -r -R -m host')
parser.add_argument('-r', '--rttok', type=float, default='25',
                    help='Upper rtt limit considered ok')
parser.add_argument('-R', '--rttmax', type=float, default='50',
                    help='Max rtt limit before host considered critical')
parser.add_argument('-m', '--maxhops', type=float, default='30',
                    help='The maximum numbr of hops to trace')
parser.add_argument('host', metavar='host',
                   help='The host address that will be tested')

args = parser.parse_args()

# Setup variables
host = vars(args)['host']
rttok = vars(args)['rttok']
rttmax = vars(args)['rttmax']
maxhops = vars(args)['maxhops']
timestamp = time.time()

# Instantiate objects
check = ping(host)

def trace(host):
        last_distance = 0
        for hop in traceroute(host,fast_mode=True):
                if last_distance + 1 != hop.distance:
                        print('*')
                print(f'path,hop={hop.distance},addr={hop.address} rtt={hop.avg_rtt}ms {timestamp}')
                last_distance = hop.distance
        return

    
# Run the ping and print out the results in InfluxDB format, exit if ping fails
if check.is_alive:
    if check.avg_rtt <= rttok:
        trace(host)
        sys.exit(0)
