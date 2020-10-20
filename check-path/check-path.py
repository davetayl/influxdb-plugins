#!/bin/env python3

# Import libraries
import sys
import argparse
from icmplib import traceroute, ping

# Set up command line parser
parser = argparse.ArgumentParser(description='Format: check-path.py -r -R -t -m host')
parser.add_argument('-r', '--rttok', type=float, default='25',
                    help='Upper rtt limit considered ok')
parser.add_argument('-R', '--rttmax', type=float, default='50',
                    help='Max rtt limit before host considered critical')
parser.add_argument('-t', '--ttype', type=int, default='1',
                    help='Test type\n\t1: Simple status and RTT\n\t2: Status with worst hop\n\t3: Status with all hops')
parser.add_argument('-m', '--maxhops', type=float, default='30',
                    help='The maximum numbr of hops to trace')
parser.add_argument('host', metavar='host',
                   help='The host address that will be tested')

args = parser.parse_args()

# Setup variables
host = vars(args)['host']
rttok = vars(args)['rttok']
rttmax = vars(args)['rttmax']
ttype = vars(args)['ttype']
maxhops = vars(args)['maxhops']
# Instantiate objects
check = ping(host)

def trace(host,ttype):
        if ttype == 1:
                print('')
                return
        elif ttype == 2:
                tracedict = {}
                tracertt = 0.0
                print(' | ', end='')
                for hop in traceroute(host,fast_mode=True):
                        tracedict.update({hop.distance:{'hopa':hop.address,'hopr':hop.avg_rtt}})
                        if hop.avg_rtt > tracertt:
                                tracedist = hop.distance
                                tracertt = hop.avg_rtt
                                traceaddr = hop.address
                print(f'hop={tracedist},addr={traceaddr},rtt={tracertt};')
                return
        elif ttype == 3:
                last_distance = 0    
                print(' | ', end='')
                for hop in traceroute(host,fast_mode=True):
                        if last_distance + 1 != hop.distance:
                                print('*')
                        print(f'hop={hop.distance},addr={hop.address},rtt={hop.avg_rtt}ms;')
                        last_distance = hop.distance
                return
        else:
            print(f'ttype {ttype} invalid.')
            return
    
# Run the ping and print out the results in Nagios format, exit if ping fails
if check.is_alive:
    if check.avg_rtt <= rttok:
        print(f'HOST OK - RTT = {check.max_rtt}ms;', end = '')
        trace(host,ttype)
        sys.exit(0)
    elif (check.avg_rtt > rttok) and (check.avg_rtt < rttmax):
        print(f'HOST WARN - RTT = {check.max_rtt}ms;', end = '')
        trace(host,ttype)
        sys.exit(1)
    elif check.avg_rtt > rttmax:
        print(f'HOST CRITICAL - RTT = {check.avg_rtt}ms;', end = '')
        trace(host,ttype)
        sys.exit(2)
    else:
        print(f'HOST CRITICAL - Down;', end = '')
        sys.exit(2)
