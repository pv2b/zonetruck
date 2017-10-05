import dns.resolver

def main():
	answers = dns.resolver.query('dnspython.org', 'MX')
	for rdata in answers:
    		print 'Host', rdata.exchange, 'has preference', rdata.preference
