# check-path.py
This is a simple python script that uses icmplib to run a ping and traceroute to a specified 
destination. It returns results in Nagios check API format. ceck-path.py is a stand alone file
however it requires icmplib, which can be installed using pip

```
pip install icmplib
```

## Command Format ##
```
usage: check-path.py [-h] [-r RTTOK] [-R RTTMAX] [-m MAXHOPS] host

positional arguments:
  host                  The host address that will be tested

optional arguments:
  -h, --help            show this help message and exit
  -r RTTOK, --rttok RTTOK
                        Upper rtt limit considered ok
  -R RTTMAX, --rttmax RTTMAX
                        Max rtt limit before host considered critical
  -m MAXHOPS, --maxhops MAXHOPS
                        The maximum numbr of hops to trace

```
