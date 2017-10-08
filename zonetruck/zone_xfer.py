import sys
from time import sleep
import dns.query
import dns.zone

def zone_xfer(masters, zone):
    for _ in range(3):
        for master in masters:
            try:
                return [dns.zone.from_xfr(dns.query.xfr(master, zone))]
            except:
                # TODO Better error printing
                print("Zone transfer error: ", sys.exc_info()[0])
                sleep(1)
    raise Exception('Unable to transfer zone %s from any master' % zone)