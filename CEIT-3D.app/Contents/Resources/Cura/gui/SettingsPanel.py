import wx
import style
import os

from customControls import ToggleSwitch


class SettingsPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, size=(style.width*3+1, style.height*7+1))

		heading_font = wx.Font(16, wx.SWISS, wx.NORMAL, wx.LIGHT)
		small_font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.LIGHT)

		quality_heading = wx.StaticText(self, label='Print Quality')
		material_heading = wx.StaticText(self, label='Print Material')
		optional_heading = wx.StaticText(self, label='Optional Settings')

		quality_heading.SetFont(heading_font)
		quality_heading.SetForegroundColour(style.accent1)
		material_heading.SetFont(heading_font)
		material_heading.SetForegroundColour(style.accent1)
		optional_heading.SetFont(heading_font)
		optional_heading.SetForegroundColour(style.accent1)

		quality_panel = wx.Panel(self)
		
		low_heading = wx.StaticText(quality_panel, label='Fast')
		med_heading = wx.StaticText(quality_panel, label='Normal')
		high_heading = wx.StaticText(quality_panel, label='High')
		ultra_heading = wx.StaticText(quality_panel, label='Ultra')

		low_heading.SetFont(small_font)
		med_heading.SetFont(small_font)
		high_heading.SetFont(small_font)
		ultra_heading.SetFont(small_font)

		self.low_button = ToggleSwitch(quality_panel, 'A fast, low quality print that will lack strength and have a poor surface finish. Use when printing a draft model for maximum speed and minimum cost.')
		self.med_button = ToggleSwitch(quality_panel, 'A regular quality print. Has a better surface finish and a denser infill than fast quality. Appropriate for most models, particularly large ones.')
		self.high_button = ToggleSwitch(quality_panel, 'A high quality print with good surface finish and a strong infill. Good for small models and models that require high dimensional accuracy.')
		self.ultra_button = ToggleSwitch(quality_panel, 'A very high quality print. Has a honeycomb infill pattern for extra strength and a very fine surface finish. Use only on final models (VERY slow!)')

		self.low_button.Bind(wx.EVT_CHECKBOX, self.onQualityClick)
		self.med_button.Bind(wx.EVT_CHECKBOX, self.onQualityClick)
		self.high_button.Bind(wx.EVT_CHECKBOX, self.onQualityClick)
		self.ultra_button.Bind(wx.EVT_CHECKBOX, self.onQualityClick)

		sizer = wx.GridBagSizer()
		sizer.AddSpacer((20,1), (0,0))
		sizer.AddSpacer((100,1), (0,1))
		sizer.AddSpacer((1,25), (1,0))
		sizer.AddSpacer((1,25), (2,0))
		sizer.AddSpacer((1,25), (3,0))
		sizer.AddSpacer((1,25), (4,0))
		sizer.AddSpacer((20,1), (0,2))

		sizer.Add(low_heading, (1,1))
		sizer.Add(med_heading, (2,1))
		sizer.Add(high_heading, (3,1))
		sizer.Add(ultra_heading, (4,1))
		sizer.Add(self.low_button, (1,3))
		sizer.Add(self.med_button, (2,3))
		sizer.Add(self.high_button, (3,3))
		sizer.Add(self.ultra_button, (4,3))

		quality_panel.SetSizerAndFit(sizer)

		self.material_panel = MaterialPanel(self)

		optional_panel = wx.Panel(self, size=(200, 100))

		support_heading = wx.StaticText(optional_panel, label='Print support')
		hollow_heading = wx.StaticText(optional_panel, label='Print hollow')
		solid_heading = wx.StaticText(optional_panel, label='Print solid')

		support_heading.SetFont(small_font)
		hollow_heading.SetFont(small_font)
		solid_heading.SetFont(small_font)

		self.support_button = ToggleSwitch(optional_panel, 'Use when the object has a lot of overhang.')
		self.hollow_button = ToggleSwitch(optional_panel)
		self.solid_button = ToggleSwitch(optional_panel)

		self.support_button.Bind(wx.EVT_CHECKBOX, self.onSupportClick)
		self.solid_button.Bind(wx.EVT_CHECKBOX, self.onDensityClick)
		self.hollow_button.Bind(wx.EVT_CHECKBOX, self.onDensityClick)

		sizer = wx.GridBagSizer()
		sizer.AddSpacer((20,1), (0,0))
		sizer.AddSpacer((100,1), (0,1))
		sizer.AddSpacer((1,25), (1,0))
		sizer.AddSpacer((1,25), (2,0))
		sizer.AddSpacer((1,25), (3,0))
		sizer.AddSpacer((20,1), (0,2))

		sizer.Add(support_heading, (1,1))
		sizer.Add(hollow_heading, (2,1))
		sizer.Add(solid_heading, (3,1))
		sizer.Add(self.support_button, (1,3))
		sizer.Add(self.hollow_button, (2,3))
		sizer.Add(self.solid_button, (3,3))

		optional_panel.SetSizerAndFit(sizer)

		sizer = wx.GridBagSizer()
		sizer.AddSpacer((30,20), (0,0))

		sizer.Add(quality_heading, (1, 1))
		sizer.AddSpacer((1,10), (2,1))
		sizer.Add(quality_panel, (3, 1))
		sizer.AddSpacer((1,20), (4,1))

		sizer.Add(material_heading, (5, 1))
		sizer.AddSpacer((1,10), (6,1))
		sizer.Add(self.material_panel, (7,1))
		sizer.AddSpacer((1,20), (8,1))


		sizer.Add(optional_heading, (9, 1))
		sizer.AddSpacer((1,10), (10,1))
		sizer.Add(optional_panel, (11,1))

		self.SetSizer(sizer)
		self.Fit()

	def onQualityClick(self, event):

		button = event.GetEventObject()
		if button.isSelected() == False:
			button.set()
			return

		self.low_button.clear()
		self.med_button.clear()
		self.high_button.clear()
		self.ultra_button.clear()

		button.set()

		advanced = self.GetParent().GetParent().GetParent().step4_panel
		advanced.doReset(None)

	def onSupportClick(self, event):
		advanced = self.GetParent().GetParent().GetParent().step4_panel
		advanced.doReset(None)

	def onDensityClick(self, event):
		button = event.GetEventObject()
		if button.isSelected() == False:
			button.clear()
		else:
			self.hollow_button.clear()
			self.solid_button.clear()
			button.set()

		advanced = self.GetParent().GetParent().GetParent().step4_panel
		advanced.doReset(None)

	def getSelectedMaterial(self):
		return self.material_panel.selected

	def GetSettings(self):
		if self.low_button.isSelected():
			q = 'Low'
		elif self.med_button.isSelected():
			q = 'Regular'
		elif self.high_button.isSelected():
			q = 'High'
		elif self.ultra_button.isSelected():
			q = 'Ultra'

		m = ' '.join(self.getSelectedMaterial()[0:1])

		s = ''
		if self.hollow_button.isSelected():
			s = 'Print hollow'
		elif self.solid_button.isSelected():
			s = 'Print solid'

		if self.support_button.isSelected() and s:
			s = s + ' with support'
		elif self.support_button.isSelected():
			s = 'Print support'

		if not s:
			s = 'None'

		return (q, m, s)


class MaterialPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, size=(style.width*2.5, 50))

		self.mat_panels = []
		self.mat_borders = []
		self.mat_labels1 = []
		self.mat_labels2 = []
		self.selected = None
		self.mat_list = []
		self.addMaterials(os.path.normpath(os.path.normpath(os.path.join(os.path.split(__file__)[0], "../pifiles", 'materials.txt'))))

	def addMaterials(self, filename):
		materials = open(filename, 'r').readlines()[1:]

		for mat in materials:
			info = mat.split()
			self.mat_list.append(info)
			border = wx.Panel(self, size=(50,50))
			mat_panel = wx.Panel(border, size=(46,46))

			mat_panel.BackgroundColour = info[2]
			border.BackgroundColour = style.accent1

			mat_label1 = wx.StaticText(mat_panel, label=''+info[0])
			self.mat_labels1.append(mat_label1)
			mat_label1.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.LIGHT))

			mat_label2 = wx.StaticText(mat_panel, label=' '+info[1])
			self.mat_labels2.append(mat_label2)
			mat_label2.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.NORMAL))

			avg_col = (int(info[2][1:3], 16) + int(info[2][3:5],16) + int(info[2][5:7],16))/3
			if avg_col < 255/2:
				mat_label1.SetForegroundColour(wx.WHITE)
				mat_label2.SetForegroundColour(wx.WHITE)

			sizer = wx.BoxSizer()
			sizer.Add(mat_label2, flag=wx.CENTER)
			mat_panel.SetSizer(sizer)
			mat_panel.Fit()

			mat_panel.Bind(wx.EVT_LEFT_UP, self.onClick)

			self.mat_panels.append(mat_panel)

			sizer = wx.GridBagSizer()
			sizer.AddSpacer((2,2), (0,0))
			sizer.Add(mat_panel, (1,1))
			sizer.AddSpacer((2,2), (2,2))
			border.SetSizerAndFit(sizer)

			self.mat_borders.append(border)



		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.AddSpacer(20,50)
		for border in self.mat_borders:
			sizer.Add(border)
			sizer.AddSpacer((5,5))
		self.SetSizer(sizer)
		self.Fit()
		self.Refresh()

	def onClick(self, event):

		clicked = event.GetEventObject()

		for i in range(len(self.mat_panels)):
			self.mat_panels[i].BackgroundColour = style.mouse_off_colour
			self.mat_labels1[i].SetForegroundColour(style.accent2)
			self.mat_labels2[i].SetForegroundColour(style.accent2)
			if self.mat_panels[i] == clicked:
				self.selected = self.mat_list[i]

				self.mat_panels[i].BackgroundColour = self.mat_list[i][2]

				advanced = self.GetParent().GetParent().GetParent().GetParent().step4_panel
				settings = {}
				settings['print_temperature'] = self.mat_list[i][3]
				settings['fillament_diameter'] = self.mat_list[i][4]
				advanced.doSettings(settings)


				avg_col = (int(self.mat_list[i][2][1:3], 16) + int(self.mat_list[i][2][3:5],16) + int(self.mat_list[i][2][5:7],16))/3
				if avg_col < 255/2:
					self.mat_labels1[i].SetForegroundColour(wx.WHITE)
					self.mat_labels2[i].SetForegroundColour(wx.WHITE)
				else:
					self.mat_labels1[i].SetForegroundColour(wx.BLACK)
					self.mat_labels2[i].SetForegroundColour(wx.BLACK)


		self.Refresh()

