# coding:utf-8

import socket
import os
import re
import time
ISOTIMEFORMAT='%Y%m%d'

def reply_to_iplist(data):
    assert isinstance(data, basestring)
    iplist = ['.'.join(str(ord(x)) for x in s) for s in re.findall('\xc0.\x00\x01\x00\x01.{6}(.{4})', data) if all(ord(x) <= 255 for x in s)]
    return iplist

def domain_to_ip(dnsserver,domain):
    dnsserver = dnsserver
    seqid = os.urandom(2)
    host = ''.join(chr(len(x))+x for x in domain.split('.'))
    data = '%s\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00%s\x00\x00\x01\x00\x01' % (seqid, host)
    sock = socket.socket(socket.AF_INET,type=socket.SOCK_DGRAM)
    sock.settimeout(100)
    sock.sendto(data, (dnsserver, 53))
    data = sock.recv(512)
    return reply_to_iplist(data)

dnsServer = "8.8.8.8"


while True:
	longtime = open('/var/www/html/hosts/hosts.'+str(time.strftime( ISOTIMEFORMAT, time.localtime())),'w')
	shorttime = open('/var/www/html/hosts/hosts.latest','w')

	valid_domains = set()

	for d in open('../data/domains.txt').readlines():
		print 'DNS:::',d
		time.sleep(1)
		try:
			ips =domain_to_ip(dnsServer,d.strip())
			if len(ips) != 0 :
				valid_domains.add(d)
				print d,ips[0]
				longtime.write(str(ips[0])+'    '+d.strip()+'\n')
				shorttime.write(str(ips[0])+'    '+d.strip()+'\n')
			else:
				print d,'VOID'
		except:
			print d
	longtime.close()
	shorttime.close()
	fout = open('../data/domains.txt','w')
	for vd in valid_domains:
		fout.write(vd+'\n')
	fout.close()


	time.sleep(24*3600)
