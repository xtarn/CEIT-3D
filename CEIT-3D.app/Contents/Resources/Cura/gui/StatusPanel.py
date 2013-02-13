import wx
import style
import os

from gui.customControls import GenericButton
from util import printerConnect

class StatusPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, size=(style.width*3+1, style.height*7+1))

		heading_font = wx.Font(16, wx.SWISS, wx.NORMAL, wx.LIGHT)
		small_font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.LIGHT)

		#---current status---
		head1_panel = wx.Panel(self)
		head1 = Text(head1_panel, 'Status', heading_font)

		head1_1 = Text(head1_panel, 'Current status', small_font)
		head1_2 = Text(head1_panel, 'Current job', small_font)
		head1_3 = Text(head1_panel, 'Progress', small_font)
		head1_4 = Text(head1_panel, 'Time to completion', small_font)

		self.status = Text(head1_panel, 'Unknown', small_font)
		self.current_job = Text(head1_panel, 'Unknown\n', small_font)
		self.progress = Text(head1_panel, 'Unknown', small_font)
		self.time_left = Text(head1_panel, 'Unknown', small_font)

		sizer = wx.GridBagSizer()
		sizer.Add(head1, (0,0), span=(1,4))
		sizer.AddSpacer((20,10), (1,0))
		sizer.AddSpacer((500,0), (1,3))
		sizer.AddSpacer((150,0), (1,1), span=(1,2))
		sizer.AddSpacer((0,25), (2,0))
		sizer.AddSpacer((0,25), (3,0))
		sizer.AddSpacer((0,25), (4,0))

		sizer.Add(head1_1, (2,1))
		sizer.Add(head1_2, (3,1))
		sizer.Add(head1_3, (4,1))
		sizer.Add(head1_4, (5,1))

		sizer.Add(self.status, (2,3))
		sizer.Add(self.current_job, (3,3))
		sizer.Add(self.progress, (4,3))
		sizer.Add(self.time_left, (5,3))

		head1_panel.SetSizer(sizer)

		#---Queue info---
		head2_panel = wx.Panel(self)
		head2 = Text(head2_panel, 'Queue Info', heading_font)

		head2_1 = Text(head2_panel, 'Total number of jobs', small_font)
		head2_2 = Text(head2_panel, 'Total queue time', small_font)

		self.num_jobs = Text(head2_panel, 'Unknown', small_font)
		self.tot_time = Text(head2_panel, 'Unknown', small_font)

		sizer = wx.GridBagSizer()
		sizer.Add(head2, (0,0), span=(1,4))
		sizer.AddSpacer((20,10), (1,0))
		sizer.AddSpacer((150,0), (1,1), span=(1,2))
		sizer.AddSpacer((0,25), (2,0))

		sizer.Add(head2_1, (2,1))
		sizer.Add(head2_2, (3,1))

		sizer.Add(self.num_jobs, (2,3))
		sizer.Add(self.tot_time, (3,3))

		head2_panel.SetSizer(sizer)

		#---my job info---
		head3_panel = wx.Panel(self)
		head3 = Text(head3_panel, 'My Jobs', heading_font)

		head3_1 = Text(head3_panel, 'Time to first job', small_font)
		head3_2 = Text(head3_panel, 'Job positions', small_font)

		self.time_to_first = Text(head3_panel, 'Unknown', small_font)
		self.my_jobs = Text(head3_panel, 'Unknown\n\n\n\n\n\n\n', small_font)


		sizer = wx.GridBagSizer()
		sizer.Add(head3, (0,0), span=(1,4))
		sizer.AddSpacer((20,10), (1,0))
		sizer.AddSpacer((500,0), (1,3))
		sizer.AddSpacer((150,0), (1,1), span=(1,2))
		sizer.AddSpacer((0,25), (2,0))

		sizer.Add(head3_1, (2,1))
		sizer.Add(head3_2, (3,1))

		sizer.Add(self.time_to_first, (2,3))
		sizer.Add(self.my_jobs, (3,3))

		head3_panel.SetSizer(sizer)

		#---main sizer---
		sizer = wx.GridBagSizer()
		sizer.AddSpacer((30,20), (0,0))
		sizer.Add(head1_panel, (1,1))
		sizer.AddSpacer((1,20), (2,1))
		sizer.Add(head2_panel, (3,1))
		sizer.AddSpacer((1,20), (4,1))
		sizer.Add(head3_panel, (5,1))

		self.SetSizerAndFit(sizer)

		self.greyOut()
		self.Connect()

	def Connect(self):
		try:
			printserv = printerConnect.printerConnect()
		except:
			wx.CallLater(5000, self.Connect)
			return

		status = printserv.connect()

		if status == '230 Login successful.':
			self.colourise()
			try:
				self.refreshInfo(printserv)
			except:
				wx.CallLater(5000, self.Connect)
		else:
			wx.CallLater(5000, self.Connect)

	def greyOut(self):
		for panel in self.GetChildren():
			for text in panel.GetChildren():
				if type(text) is Text:
					text.SetForegroundColour(style.accent2)

		self.Refresh()

	def colourise(self):
		for panel in self.GetChildren():
			for text in panel.GetChildren():
				text.SetForegroundColour(wx.BLACK)

			heading = panel.GetChildren()[0]
			heading.SetForegroundColour(style.accent1)

		self.Refresh()

	def refreshInfo(self, printserv):
		queue = printserv.getQueue()

		print queue
		
		queueline = queue[1].strip().split('\t')

		#--num jobs
		self.num_jobs.SetLabel(queueline[0])

		#--total time
		self.tot_time.SetLabel(self.minToString(int(queueline[1])))

		#--status
		currentid = None
		if 'Printing' in queueline[2]:
			self.status.SetLabel('Busy')
			self.status.SetForegroundColour('#FF8C00')
			currentid = queueline[2][8:]
		else:
			self.status.SetLabel('Idle')
			self.status.SetForegroundColour('#228B22')
		#--% progress
		self.progress.SetLabel(queueline[3] + '%')
		progress = int(queueline[3])

		#-- current id
		if not currentid:
			self.current_job.SetLabel('None')
			self.time_left.SetLabel('0min')

		my_jobs = []
		time_to_first = 0
		
		for i in range(len(queue[4:])):
			queueline = queue[i+4].strip().split('\t')

			#-- current job
			if currentid and currentid == queueline[7]:
				self.current_job.SetLabel('%s - %s' %(queueline[0], queueline[6]))
				if queueline[6] == os.uname()[1]:
					self.status.SetLabel('Printing My Job')
					self.status.SetForegroundColour('#228B22')

				#-- time left
				t = int(int(queueline[1]) * (1-progress/100.0)) 
				self.time_left.SetLabel(self.minToString(t))

			#-- my jobs
			if queueline[6] == os.uname()[1]:
				my_jobs.append([i,queueline])
			if my_jobs == [] and queueline[6] != os.uname()[1]:
				time_to_first += int(queueline[1])

		self.time_to_first.SetLabel(self.minToString(time_to_first))

		s = ''
		for job in my_jobs:
			s = s + str(job[0]+1) + ' - ' + job[1][0] + '\n'

		if s == '':
			s = 'No Jobs'

		self.my_jobs.SetLabel(s)

		self.Refresh()

		printserv.closeConnection()

		wx.CallLater(2000, self.Connect)

	def minToString(self, min):
		hrs = min/60
		mins = min%60
		s = 'min'
		if mins > 1:
			s = str(mins) + s + 's'
		else:
			s = str(mins) + s
		if hrs == 1:
			s = '1hr ' + s
		elif hrs > 1:
			s = str(hrs) + 'hrs ' + s
		return s

class Text(wx.StaticText):
	def __init__(self, parent, label, font, colour=wx.BLACK):
		wx.StaticText.__init__(self, parent, label=label)
		self.SetFont(font)
		self.SetForegroundColour(colour)