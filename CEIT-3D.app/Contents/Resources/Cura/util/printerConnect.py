from ftplib import FTP
import os

class printerConnect(object):
	def __init__(self):
		self.ftp = FTP('130.102.87.49')
		self.queueloc = os.path.normpath(os.path.normpath(os.path.join(os.path.split(__file__)[0], "../pifiles", 'queue.txt')))

	def connect(self):
		return self.ftp.login()

	def getQueue(self):
		self.ftp.retrbinary("RETR queue.txt", open(self.queueloc, 'w').write)
		queue = open(self.queueloc, 'r').readlines()
		return queue

	def sendJob(self, filename, uid):
		name = filename[filename.rfind('/')+1:-4]
		self.ftp.storbinary("STOR Jobs/" + name + "." + uid + ".gcode", open(filename[:-4]+".gcode"))

	def sendJobInfo(self, filename, uid):
		name = filename[filename.rfind('/')+1:-4]
		self.ftp.storbinary("STOR JobInfo/" + name + "." + uid + ".info", open(filename[:-4]+".info"))

	def closeConnection(self):
		self.ftp.quit()

		

		
		
		
