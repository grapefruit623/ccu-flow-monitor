import netifaces
import datetime

def dateTesting():
	now = datetime.datetime.today() 
	for i in range(1, now.day+1):
			print '%d / %d/%d'%( now.year, now.month, i )
	
if __name__ == '__main__':
		dateTesting()
		'''print netifaces.interfaces()
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
								'''
#		print netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
#		print netifaces.ifaddresses('eth0')[netifaces.AF_LINK][0]['addr']
