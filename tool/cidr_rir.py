#!/usr/bin/env python
import sys
import ipaddress
import urllib.request

# https://www.apnic.net/about-apnic/corporate-documents/documents/resource-guidelines/

RIR_STATISTICS_URL = [
    'http://ftp.arin.net/pub/stats/arin/delegated-arin-extended-latest',
    'http://ftp.ripe.net/pub/stats/ripencc/delegated-ripencc-extended-latest',
    'http://ftp.apnic.net/pub/stats/apnic/delegated-apnic-extended-latest',
    'http://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-extended-latest',
    'http://ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-extended-latest'
]

def make_data(rir_url):
    url = urllib.request.urlopen(rir_url)

    for line in url:
        item = line.decode("utf-8").split('|')

        if len(item) < 5 or item[0][0] == '#' or item[1] == '*' or item[2] != 'ipv4':
            continue

        start = ipaddress.IPv4Address(item[3])
        end = start + (int(item[4]) - 1)
        for ipaddr in ipaddress.summarize_address_range(start,end):
            bin_addr = "".join([format(int(x),'08b')  for x in str(ipaddr.network_address).split('.')])
            print(format("%s\t%s\t%s\t%s" % (bin_addr, ipaddr.prefixlen, ipaddr.with_prefixlen, item[1])))

    url.close()

if __name__ == "__main__":
    try:
        for r in RIR_STATISTICS_URL:
            sys.stderr.write('start ' + r + "\n")
            make_data(r)
            sys.stderr.write("done. \n")
    except Exception as e:
        traceback.print_exc()
