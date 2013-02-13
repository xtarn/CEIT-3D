import wx
import style
import threading
import os
import binascii
import time

from gui.customControls import GenericButton
from util import printerConnect
from util import sliceRun
from util import profile
from util import gcodeInterpreter

class PrintPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, size=(style.width*3+1, style.height*7+1))

		heading_font = wx.Font(16, wx.SWISS, wx.NORMAL, wx.LIGHT)
		small_font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.LIGHT)

		head1_panel = wx.Panel(self)
		head1 = Text(head1_panel, 'Setting Summary', heading_font, style.accent1)

		head1_1 = Text(head1_panel, 'Quality', small_font)
		head1_2 = Text(head1_panel, 'Material', small_font)
		head1_3 = Text(head1_panel, 'Optional', small_font)

		self.quality = Text(head1_panel, 'Unknown', small_font)
		self.material = Text(head1_panel, 'Unknown', small_font)
		self.special = Text(head1_panel, 'Unknown', small_font)

		slice_panel = wx.Panel(self)
		prepare_button = GenericButton(slice_panel, label='Prepare Print\t')
		prepare_button.Bind(wx.EVT_BUTTON, self.OnSlice)

		self.progress_gauge = wx.Gauge(slice_panel, size=(200,20))
		self.progress_gauge.SetRange(100)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(prepare_button)
		sizer.AddSpacer(20)
		sizer.Add(self.progress_gauge)
		sizer.AddSpacer(10)
		slice_panel.SetSizer(sizer)

		self.head2_panel = wx.Panel(self)
		head2 = Text(self.head2_panel, 'Print Summary', heading_font, style.accent2)

		head2_1 = Text(self.head2_panel, 'Print Time', small_font, style.accent2)
		head2_2 = Text(self.head2_panel, 'Filament Length', small_font, style.accent2)
		head2_3 = Text(self.head2_panel, 'Filament Weight', small_font, style.accent2)
		head2_4 = Text(self.head2_panel, 'Cost', small_font, style.accent2)

		self.ptime = Text(self.head2_panel, 'Unknown', small_font, style.accent2)
		self.fil_len = Text(self.head2_panel, 'Unknown', small_font, style.accent2)
		self.fil_wgt = Text(self.head2_panel, 'Unknown', small_font, style.accent2)
		self.cost = Text(self.head2_panel, 'Unknown', small_font, style.accent2)

		self.send_button = GenericButton(self, label='Send to Printer\t')
		self.send_button.Bind(wx.EVT_BUTTON, self.OnSend)

		sizer = wx.GridBagSizer()
		sizer.Add(head1, (0,0), span=(1,4))
		sizer.AddSpacer((20,10), (1,0))
		sizer.AddSpacer((500,0), (1,3))
		sizer.AddSpacer((150,0), (1,1), span=(1,2))
		sizer.AddSpacer((0,25), (2,0))
		sizer.AddSpacer((0,25), (3,0))

		sizer.Add(head1_1, (2,1))
		sizer.Add(head1_2, (3,1))
		sizer.Add(head1_3, (4,1))

		sizer.Add(self.quality, (2,3))
		sizer.Add(self.material, (3,3))
		sizer.Add(self.special, (4,3))

		head1_panel.SetSizer(sizer)

		sizer = wx.GridBagSizer()
		sizer.Add(head2, (0,0), span=(1,4))
		sizer.AddSpacer((20,10), (1,0))
		sizer.AddSpacer((500,0), (1,3))
		sizer.AddSpacer((150,0), (1,1), span=(1,2))
		sizer.AddSpacer((0,25), (2,0))
		sizer.AddSpacer((0,25), (3,0))
		sizer.AddSpacer((0,25), (4,0))

		sizer.Add(head2_1, (2,1))
		sizer.Add(head2_2, (3,1))
		sizer.Add(head2_3, (4,1))
		sizer.Add(head2_4, (5,1))

		sizer.Add(self.ptime, (2,3))
		sizer.Add(self.fil_len, (3,3))
		sizer.Add(self.fil_wgt, (4,3))
		sizer.Add(self.cost, (5,3))

		self.head2_panel.SetSizer(sizer)

		sizer = wx.GridBagSizer()
		sizer.AddSpacer((30,20), (0,0))
		sizer.Add(head1_panel, (1,1))
		sizer.AddSpacer((0,20), (2,1))
		sizer.Add(slice_panel, (3,1))
		sizer.AddSpacer((0,20), (4,1))
		sizer.Add(self.head2_panel, (5,1))
		sizer.AddSpacer((0,20), (6,1))
		sizer.Add(self.send_button, (7,1))

		self.SetSizerAndFit(sizer)

		self.printTime = None

		self.send_button.disable()

	def OnSlice(self, event):

		self.progress_gauge.SetValue(0)
		self.prevStep = 'start'
		self.totalDoneFactor = 0.0
		self.startTime = time.time()

		frame = self.GetParent().GetParent().GetParent()
		settings = frame.step4_panel

		put = profile.putProfileSetting

		put('nozzle_size', settings.nozzle_size.GetValue())
		put('layer_height', settings.layer_height.GetValue())
		put('wall_thickness', settings.wall_thickness.GetValue())
		put('solid_layer_thickness', settings.bottom_top_thickness.GetValue())
		put('fill_density', settings.fill_density.GetValue())
		put('skirt_line_count', settings.skirt_count.GetValue())
		put('skirt_gap', settings.skirt_distance.GetValue())
		put('print_speed', settings.print_speed.GetValue())
		put('print_temperature', settings.print_temperature.GetValue())
		put('support', settings.support_type.GetValue())
		put('filament_diameter', settings.fillament_diameter.GetValue())
		put('filament_density', settings.packing_density.GetValue())
		put('retraction_min_travel', settings.retract_min_travel.GetValue())
		put('retraction_enable', str(settings.retraction.GetValue()))
		put('retraction_speed', settings.retract_speed.GetValue())
		put('retraction_amount', settings.retract_distance.GetValue())
		put('retraction_extra', settings.retract_extra.GetValue())
		put('retract_on_jumps_only', str(settings.retract_on_jumps.GetValue()))
		put('travel_speed', settings.travel_speed.GetValue())
		put('max_z_speed', settings.max_z_speed.GetValue())
		put('bottom_layer_speed', settings.bottom_speed.GetValue())
		put('cool_min_layer_time', settings.min_layer_time.GetValue())
		put('fan_enabled', str(settings.enable_fan.GetValue()))
		put('fan_layer', settings.fan_layer.GetValue())
		put('fan_speed', settings.fan_min_speed.GetValue())
		put('fan_speed_max', settings.fan_max_speed.GetValue())
		put('extra_base_wall_thickness', settings.extra_wall.GetValue())
		put('sequence', settings.sequence.GetValue())
		put('infill_type', settings.infill_pattern.GetValue())
		put('solid_top', str(settings.solid_top.GetValue()))
		put('fill_overlap', settings.infill_overlap.GetValue())
		put('support_rate', settings.support_material_amount.GetValue())
		put('support_distance', settings.support_distance.GetValue())
		put('enable_skin', str(settings.skin.GetValue()))
		put('enable_raft', str(settings.add_raft.GetValue()))
		put('raft_margin', settings.raft_margin.GetValue())
		put('raft_base_material_amount', settings.raft_base.GetValue())
		put('raft_interface_material_amount', settings.raft_interface.GetValue())

		put('machine_center_x', '100')
		put('machine_center_y', '100')
		put('machine_type', 'ultimaker')
		put('machine_width', '205')
		put('machine_depth', '205')
		put('machine_height', '200')

		thread = WorkerThread(self, frame.filename)

	def OnSend(self, event):

		uniqueId = binascii.hexlify(os.urandom(4))

		frame = self.GetParent().GetParent().GetParent()

		info = []
		info.append(frame.filename[frame.filename.rfind('/')+1:-4] + '\n')
		info.append(self.printTime + '\n')
		info.append(self.fil_len.GetLabel()[:-1] + '\n')
		info.append(self.fil_wgt.GetLabel()[:-1] + '\n')
		info.append(self.material.GetLabel() + '\n')
		info.append(self.cost.GetLabel()[1:] + '\n')
		info.append(os.uname()[1] + '\n')
		info.append(uniqueId)

		infofile = open(frame.filename[:-4] + ".info", "w")
		infofile.writelines(info)
		infofile.close()

		printserv = printerConnect.printerConnect()
		printserv.connect()

		printserv.sendJob(frame.filename, uniqueId)
		printserv.sendJobInfo(frame.filename, uniqueId)
		printserv.closeConnection()

	def OnSliceDone(self, result):
		self.progress_gauge.SetValue(100)

		self.progressLog = result.progressLog

		if result.returnCode == 0:

			self.printTime = str(int(result.gcode.totalMoveTimeMinute))
			self.ptime.SetLabel(self.minToString(int(result.gcode.totalMoveTimeMinute)))
			self.fil_len.SetLabel('%.2f' % (result.gcode.extrusionAmount /1000) + 'm')
			self.fil_wgt.SetLabel('%.2f' % (result.gcode.calculateWeight() *1000) + 'g')
			self.cost.SetLabel('$' + result.gcode.calculateCost())

			for child in self.head2_panel.GetChildren():
				child.SetForegroundColour(wx.BLACK)

			self.head2_panel.GetChildren()[0].SetForegroundColour(style.accent1)


			self.send_button.enable()

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

	def SetProgress(self, stepName, layer, maxLayer):
		if self.prevStep != stepName:
			self.totalDoneFactor += sliceRun.sliceStepTimeFactor[self.prevStep]
			newTime = time.time()

			self.startTime = newTime
			self.prevStep = stepName

		progressValue = ((self.totalDoneFactor + sliceRun.sliceStepTimeFactor[stepName] * layer / maxLayer) / sliceRun.totalRunTimeFactor) * 100
		
		self.progress_gauge.SetValue(int(progressValue))

	def UpdateSettingSummary(self):
		frame = self.GetParent().GetParent().GetParent()
		(q, m, s) = frame.step3_panel.GetSettings()
		
		self.quality.SetLabel(q)
		self.material.SetLabel(m)
		self.special.SetLabel(s)

	def ClearPrintSummary(self):
		for child in self.head2_panel.GetChildren():
				child.SetForegroundColour(style.accent2)

		self.ptime.SetLabel('Unknown')
		self.fil_len.SetLabel('Unknown')
		self.fil_wgt.SetLabel('Unknown')
		self.cost.SetLabel('Unknown')

		self.send_button.disable()


class WorkerThread(threading.Thread):
	def __init__(self, notifyWindow, filename):
		threading.Thread.__init__(self)

		self.filename = filename
		self.notifyWindow = notifyWindow
		self.cmdList = []
		self.cmdList.append(sliceRun.getSliceCommand(filename))
		self.start()

	def run(self):
		p = sliceRun.startSliceCommandProcess(self.cmdList[0])
		line = p.stdout.readline()
		self.progressLog = []
		maxValue = 1

		while(len(line) > 0):
			line = line.rstrip()
			if line[0:9] == "Progress[" and line[-1:] == "]":
				progress = line[9:-1].split(":")
				if len(progress) > 2:
					maxValue = int(progress[2])
				wx.CallAfter(self.notifyWindow.SetProgress, progress[0], int(progress[1]), maxValue)

			else:
				self.progressLog.append(line)

			line = p.stdout.readline()

		self.returnCode = p.wait()

		gcodeFilename = sliceRun.getExportFilename(self.filename)
		gcodefile = open(gcodeFilename, "a")

		for logLine in self.progressLog:
			if logLine.startswith('Model error('):
				gcodefile.write(';%s\n' % (logLine))
		gcodefile.close()

		self.gcode = gcodeInterpreter.gcode()
		self.gcode.load(gcodeFilename)
		profile.replaceGCodeTags(gcodeFilename, self.gcode)

		wx.CallAfter(self.notifyWindow.OnSliceDone, self)

	# def run(self):
	# 	#p = sliceRun.startSliceCommandProcess(self.cmdList[0])

	# 	p = sliceRun.startSliceCommandProcess(['ls'])

	# 	line = p.stdout.readline()

	# 	while(len(line) > 0):
	# 		line = line.rstrip()
	# 		print line

	# 		line = p.stdout.readline()

	# 	# while(len(line) > 0):

	# 	# 	line = line.rstrip()
	# 	# 	print line

	# 	self.returnCode = p.wait() 

	# 	# wx.CallAfter(self.notifyWindow.OnSliceDone, self)

class Text(wx.StaticText):
	def __init__(self, parent, label, font, colour=wx.BLACK):
		wx.StaticText.__init__(self, parent, label=label)
		self.SetFont(font)
		self.SetForegroundColour(colour)