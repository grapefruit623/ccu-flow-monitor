import netifaces
import datetime
import calendar

def dateTesting():
	print calendar.monthrange(2013, 2)[1]
	
if __name__ == '__main__':
		#dateTesting()
		print netifaces.interfaces()
		print 'AF_INET: %d, AF_LINK: %d' %(netifaces.AF_INET, netifaces.AF_LINK)
		for i in netifaces.interfaces():
				print i
				print netifaces.ifaddresses(i)
				if None != netifaces.ifaddresses(i):
						if None != netifaces.ifaddresses(i)[netifaces.AF_INET]:
								print '\t%s'%(netifaces.ifaddresses(i)[netifaces.AF_INET][0])
								print '\t%s'%(netifaces.ifaddresses(i)[netifaces.AF_INET][0]['addr'])
						if None != netifaces.ifaddresses(i)[netifaces.AF_LINK]:
								print '\t%s'%(netifaces.ifaddresses(i)[netifaces.AF_LINK][0]['addr'])
								
#		print netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
#		print netifaces.ifaddresses('eth0')[netifaces.AF_LINK][0]['addr']
