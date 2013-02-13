import wx
import style

from customControls import ToggleSwitch, GenericButton
from gui import preview3d

class TransformPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, size=(style.width*3+1, style.height*7+1))

		heading_font = wx.Font(16, wx.SWISS, wx.NORMAL, wx.LIGHT)
		small_font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.LIGHT)

		swap_heading = wx.StaticText(self, label='Swap')
		mirror_heading = wx.StaticText(self, label='Mirror')
		scale_heading = wx.StaticText(self, label='Scale')

		swap_heading.SetFont(heading_font)
		mirror_heading.SetFont(heading_font)
		scale_heading.SetFont(heading_font)

		swap_heading.SetForegroundColour(style.accent1)
		mirror_heading.SetForegroundColour(style.accent1)
		scale_heading.SetForegroundColour(style.accent1)

		# swap panel
		swap_panel = wx.Panel(self)

		xy_heading = wx.StaticText(swap_panel, label='Swap X and Y')
		yz_heading = wx.StaticText(swap_panel, label='Swap Y and Z')

		xy_heading.SetFont(small_font)
		yz_heading.SetFont(small_font)

		self.xy_button = ToggleSwitch(swap_panel)
		self.yz_button = ToggleSwitch(swap_panel)

		self.xy_button.Bind(wx.EVT_CHECKBOX, self.onSwap)
		self.yz_button.Bind(wx.EVT_CHECKBOX, self.onSwap)

		sizer = wx.GridBagSizer()
		sizer.AddSpacer((20,1), (0,0))
		sizer.AddSpacer((100,1), (0,1))
		sizer.AddSpacer((1,25), (1,0))
		sizer.AddSpacer((1,25), (2,0))
		sizer.AddSpacer((20,1), (0,2))

		sizer.Add(xy_heading, (1,1))
		sizer.Add(yz_heading, (2,1))
		sizer.Add(self.xy_button, (1,3))
		sizer.Add(self.yz_button, (2,3))

		swap_panel.SetSizerAndFit(sizer)

		#mirror panel
		mirror_panel = wx.Panel(self)

		x_heading = wx.StaticText(mirror_panel, label='Mirror X')
		y_heading = wx.StaticText(mirror_panel, label='Mirror Y')
		z_heading = wx.StaticText(mirror_panel, label='Mirror Z')

		x_heading.SetFont(small_font)
		y_heading.SetFont(small_font)
		z_heading.SetFont(small_font)

		self.x_button = ToggleSwitch(mirror_panel)
		self.y_button = ToggleSwitch(mirror_panel)
		self.z_button = ToggleSwitch(mirror_panel)

		self.x_button.Bind(wx.EVT_CHECKBOX, self.onMirror)
		self.y_button.Bind(wx.EVT_CHECKBOX, self.onMirror)
		self.z_button.Bind(wx.EVT_CHECKBOX, self.onMirror)

		sizer = wx.GridBagSizer()
		sizer.AddSpacer((20,1), (0,0))
		sizer.AddSpacer((100,1), (0,1))
		sizer.AddSpacer((1,25), (1,0))
		sizer.AddSpacer((1,25), (2,0))
		sizer.AddSpacer((1,25), (3,0))
		sizer.AddSpacer((20,1), (0,2))

		sizer.Add(x_heading, (1,1))
		sizer.Add(y_heading, (2,1))
		sizer.Add(z_heading, (3,1))
		sizer.Add(self.x_button, (1,3))
		sizer.Add(self.y_button, (2,3))
		sizer.Add(self.z_button, (3,3))

		mirror_panel.SetSizerAndFit(sizer)

		#scale panel
		scale_panel = wx.Panel(self)

		self.scale = wx.TextCtrl(scale_panel)
		self.scale.SetValue('1.0')

		self.scale.Bind(wx.EVT_TEXT, self.onScale)

		sizer = wx.GridBagSizer()
		sizer.AddSpacer((20,1), (0,0))
		sizer.AddSpacer((1,25), (1,0))

		sizer.Add(self.scale, (1,1))

		scale_panel.SetSizer(sizer)

		#reset button
		reset = GenericButton(self, 'Reset All')
		reset.Bind(wx.EVT_BUTTON, self.onReset)

		#3d preview window
		self.preview = preview3d.previewPanel(self)
		#self.preview.loadModelFiles(['/Users/ProChef/Desktop/Cura-v2/images/UltimakerRobot_support.stl'])

		# window settings
		sizer = wx.GridBagSizer()
		sizer.AddSpacer((30,20), (0,0))

		sizer.Add(swap_heading, (1,1))
		sizer.AddSpacer((1,10), (2,1))
		sizer.Add(swap_panel, (3,1))
		sizer.AddSpacer((1,10), (4,1))

		sizer.Add(mirror_heading, (5,1))
		sizer.AddSpacer((1,10), (6,1))
		sizer.Add(mirror_panel, (7,1))
		sizer.AddSpacer((1,10), (8,1))

		sizer.Add(scale_heading, (9,1))
		sizer.AddSpacer((1,10), (10,1))
		sizer.Add(scale_panel, (11,1))
		sizer.AddSpacer((1,10), (12,1))

		#sizer.AddSpacer((1,30), (13,1))
		sizer.Add(reset, (14,1))

		sizer.AddSpacer((30,1), (1,2))
		sizer.Add(self.preview, (2,3), span=(15,1))

		self.SetSizer(sizer)
		self.Fit()

	def onSwap(self, event):
		self.preview.flipxy = self.xy_button.isSelected()
		self.preview.flipyz = self.yz_button.isSelected()
		self.preview.updateModelTransform()

	def onMirror(self, event):
		self.preview.mirrorx = self.x_button.isSelected()
		self.preview.mirrory = self.y_button.isSelected()
		self.preview.mirrorz = self.z_button.isSelected()
		self.preview.updateModelTransform()

	def onScale(self, event):
		try:
			scale = float(self.scale.GetValue())
			if scale == 0:
				return
			self.preview.OnScale(scale)
		except:
			return

	def onReset(self, event):
		self.xy_button.clear()
		self.yz_button.clear()
		self.x_button.clear()
		self.y_button.clear()
		self.z_button.clear()
		self.scale.SetValue('1.0')

		self.onSwap(None)
		self.onMirror(None)
		self.onScale(None)

	def load(self, filepath):
		self.preview.loadModelFiles([filepath])
