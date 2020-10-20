hops = traceroute('www.cisco.com')

print('Distance (ttl)    Address    Average round-trip time')
last_distance = 0

for hop in hops:
    if last_distance + 1 != hop.distance:
        print('Some routers are not responding')

        # See the Hop class for details
        print(f'{hop.distance}    {hop.address}    {hop.avg_rtt} ms')

        last_distance = hop.distance
        
        
traceroute(address, count=3, interval=0.05, timeout=2, id=PID, max_hops=30, fast_mode=False)

ping(address, count=4, interval=1, timeout=2, id=PID, **kwargs)