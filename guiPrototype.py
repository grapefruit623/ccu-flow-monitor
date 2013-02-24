#!/usr/bin/env python

import sys
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import * 
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import urllib
import urllib2
import re
import datetime 
import numpy.numarray as na
from BeautifulSoup import BeautifulSoup
import netifaces

class showTraffic(QMainWindow):
	def __init__(self, parent=None):
		QMainWindow.__init__(self, parent)
		self.setWindowTitle('ccu network')
		self.resize(800, 500)
		self.creatMainWin()
		self.ipParse()
		self.macParse()
		self.drawHistogram(self.eth0Ip)
		self.drawPlot(self.eth0Ip)
		#self.requestForMonth(self.eth0Ip)

	def creatMainWin(self):
		self.mainFrame = QWidget()
		self.fig = Figure( (5, 4) )
		self.canvas = FigureCanvas(self.fig)
		self.canvas.setParent(self.mainFrame)
		self.axes = self.fig.add_subplot(111, xlim=(0, 24), ylim=(0, 5500))

		self.ipAddr = QLineEdit()
		self.connect(self.ipAddr, SIGNAL("returnPressed()"), self.ipChanged )#when 'enter' presed, call drawing function

		self.macAddr = QLabel()

		vbox = QVBoxLayout()
		vbox.addWidget(self.canvas)
		hbox = QHBoxLayout()
		hbox.addWidget(self.ipAddr)
		hbox.addWidget(self.macAddr)
		vbox.addLayout(hbox)
		self.mainFrame.setLayout(vbox)
		self.setCentralWidget(self.mainFrame)

	def ipChanged(self):
		self.eth0Ip = self.ipAddr.text()
		self.drawHistogram(self.eth0Ip)
		self.drawPlot(self.eth0Ip)
	def macParse(self):
		self.macInfo = netifaces.ifaddresses('eth0')[netifaces.AF_LINK][0]['addr']
		self.macAddr.setText(self.macInfo)
	def ipParse(self):
		self.eth0Ip = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
		self.ipAddr.setText(self.eth0Ip)

	def setAxesInfo(self):
		toDay = datetime.datetime.now()
		self.axes.set_ylabel('MB (1024 x 1024 Bytes)', fontsize=12, fontweight='bold')
		self.axes.set_xlabel('%s %s / %s'%(str(toDay.year),str(toDay.month),str(toDay.day)), fontsize=12, fontweight='bold')
		self.axes.set_ylim(0, 5500)
		self.axes.set_xlim(0, 24)
		self.axes.set_xticks( range(0, 24, 1) )
		self.axes.set_yticks( range(0, 5500, 500) )
		self.axes.grid()
		self.axes.get_yaxis().tick_right() 
		self.axes.get_xaxis().tick_bottom() 
		
	def drawPlot(self, ip):
		(timeRange, flowdata ) = self.request(ip)
		for i in range(1, len(flowdata)):
				flowdata[i] += flowdata[i-1]
				
		#self.axes.cla()
		#self.setAxesInfo()
		self.axes.plot(range(0, len(flowdata)), flowdata, color='red', linestyle='dashed', linewidth = 2)
		self.canvas.draw()

	def drawHistogram(self, ip):
		print('hello');
		self.axes.clear()
		(timeRange, flowdata) = self.request(ip)
		#(timeRange, flowdata) = self.requestForMonth(ip)
		self.axes.bar(range(0, len(flowdata)), flowdata, width = 1 )
		self.setAxesInfo()
		self.canvas.draw()

	def requestForMonth(self, ip):
		now = datetime.datetime.now()
		year = str(now.year)	
		month = str(now.month).zfill(2)
		flowData = []
		timeStamp = []

		for i in range(1, now.day+1):
				timeStamp.append(i)
				day = str(i).zfill(2)
				data = {'year':year, 'month':month, 'day':day, 'ip':ip}
				url = 'http://netflow.dorm.ccu.edu.tw/query.php'
				user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
				headers = { 'User-Agent': user_agent }

				try:
					postData = urllib.urlencode(data)
					req = urllib2.Request(url+'?'+ postData)
					#req = urllib2.OpenerDirector.open(url, postData)
					res = urllib2.urlopen(req)
					htmlCode = res.read().decode('big5').encode('utf-8')

					soup = BeautifulSoup(htmlCode)
				except Exception as log:
					print 'error mesage'
					print log

				try:
					#try to get table2 which record data flow per hours
					table2 = soup.findAll('table')[0]
					tr = table2.findAll('tr')[4]
					td = tr.findAll('td', text=True)
					flowData.append(float(td[9]))
					#row2 is list of < class BeautifulSoup.Tag >
				except IndexError:
					print 'The reason of error is that the data table isn''t created by CNA'	
					flowData.append(0)
				except Exception as log:
					print 'error mesage'
					print log
		return ( timeStamp, flowData ) 

	def request(self, ip):
		now = datetime.datetime.now()
		year = str(now.year)	
		month = str(now.month).zfill(2)
		day = str(now.day).zfill(2)
		data = {'year':year, 'month':month, 'day':day, 'ip':ip}
		url = 'http://netflow.dorm.ccu.edu.tw/query.php'
		user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		headers = { 'User-Agent': user_agent }

		try:
			postData = urllib.urlencode(data)
			req = urllib2.Request(url+'?'+ postData)
			#req = urllib2.OpenerDirector.open(url, postData)
			res = urllib2.urlopen(req)
			htmlCode = res.read().decode('big5').encode('utf-8')

			soup = BeautifulSoup(htmlCode)
		except Exception as log:
			print 'error mesage'
			print log

		try:
			#try to get table2 which record data flow per hours
			table2 = soup.findAll('table')[1]
			#row2 is list of < class BeautifulSoup.Tag >
		except IndexError:
			print 'The reason of error is that the data table isn''t created by CNA'	
		except Exception as log:
			print 'error mesage'
			print log
		try:	
			myTable = []
			flowData = []
			tr = table2.findAll('tr')
			for d in [4, 9, 14]:
				data = tr[d].findAll('td', text=True)
				for stmp in range(3, len(data)): #data[0~2] is '\n', data[3] is chinese
					if not re.match('\n', data[stmp]):
						flowData.append(float(data[stmp]))
		
			timeRange = range(1,25)
			return (timeRange, flowData)
		except Exception as log:
			print 'error mesage'
			print log

if __name__ == "__main__":
		mainFrame = QApplication(sys.argv)
		lineEdit = QLineEdit()
		putton1 = QPushButton("hello world")

		graph = showTraffic()
		graph.show()

		'''frame = QVBoxLayout()
		frame.addWidget(lineEdit)
		frame.addWidget(putton1)
		frame.addWidget(graph)

		widget = QWidget()
		widget.setLayout(frame)
		widget.show()
		'''
		
		mainFrame.exec_()

