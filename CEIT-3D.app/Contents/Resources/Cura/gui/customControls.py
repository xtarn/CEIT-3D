import wx
import style

class ToggleSwitch(wx.Panel):
	def __init__(self, parent, label=''):
		wx.Panel.__init__(self, parent, size=(20,20))

		self.BackgroundColour = style.accent1

		self.fill = wx.Panel(self, size=(12,12))
		self.fill.BackgroundColour = wx.WHITE

		sizer = wx.GridBagSizer()
		sizer.AddSpacer((2,2), (0,0))
		sizer.Add(self.fill, (1,1))
		sizer.AddSpacer((2,2), (2,2))

		self.SetSizerAndFit(sizer)

		self.Bind(wx.EVT_LEFT_UP, self.onClick)
		self.fill.Bind(wx.EVT_LEFT_UP, self.onClick)
		self.fill.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver)
		self.fill.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseLeave)

		self.tooltip = wx.PopupWindow(parent, flags=wx.SIMPLE_BORDER)
		self.tooltip.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))
		self.tooltip.text = wx.StaticText(self.tooltip, label=label)
		self.tooltip.text.Wrap(350)

		self.tooltip.sizer = wx.BoxSizer()
		self.tooltip.sizer.Add(self.tooltip.text, flag=wx.EXPAND|wx.ALL, border=1)
		self.tooltip.SetSizerAndFit(self.tooltip.sizer)

		self.tooltip.Hide()

		if label == '':
			self.tooltip = None

	def onClick(self, event):
		if self.fill.BackgroundColour != style.accent1:
			self.set()
		else:
			self.clear()

		checkEvent = wx.CommandEvent(wx.wxEVT_COMMAND_CHECKBOX_CLICKED, self.GetId())
		checkEvent.SetEventObject(self)
		self.GetEventHandler().ProcessEvent(checkEvent)

		self.Refresh()

	def ShowToolTip(self, state):
		if self.tooltip == None:
			return

		x, y = self.ClientToScreenXY(0,0)

		sx, sy = self.GetSizeTuple()
		self.tooltip.SetPosition((x, y+sy))

		self.tooltip.Show(state)

	def onMouseOver(self, event):
		self.ShowToolTip(True)

		if self.fill.BackgroundColour != style.accent1:
			self.fill.BackgroundColour = style.mouse_over_colour
			self.Refresh()

	def onMouseLeave(self, event):
		self.ShowToolTip(False)
		if self.fill.BackgroundColour != style.accent1:
			self.fill.BackgroundColour = wx.WHITE
			self.Refresh()

	def isSelected(self):
		if self.fill.BackgroundColour == wx.WHITE:
			return False
		else:
			return True

	def set(self):
		self.fill.BackgroundColour = style.accent1
		self.Refresh()
	
	def clear(self):
		self.fill.BackgroundColour = wx.WHITE
		self.Refresh()


class NextButton(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, size=(80, 25), pos=(style.width*2.1,style.height*6.3))

		self.BackgroundColour = style.accent1

		self.fill = wx.Panel(self, size=(76, 19))
		self.fill.BackgroundColour = style.accent1

		self.text = wx.StaticText(self, label='    Next   ')
		self.text.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.LIGHT))
		self.text.SetForegroundColour(wx.WHITE)

		sizer = wx.BoxSizer()
		sizer.Add(self.text, flag=wx.CENTER)
		self.fill.SetSizer(sizer)

		sizer = wx.GridBagSizer()
		sizer.AddSpacer((2,2), (0,0))
		sizer.Add(self.fill, (1,1))
		sizer.AddSpacer((2,2), (2,2))
		self.SetSizer(sizer)
		self.Fit()

		self.fill.Bind(wx.EVT_LEFT_UP, self.onClick)
		self.fill.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver)
		self.fill.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseLeave)

	def onClick(self, event):
		clickEvent = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, self.GetId())
		clickEvent.SetEventObject(self)
		self.GetEventHandler().ProcessEvent(clickEvent)

	def onMouseOver(self, event):
		self.text.SetForegroundColour(style.accent1)
		self.fill.BackgroundColour = style.mouse_over_colour
		self.Refresh()

	def onMouseLeave(self, event):
		self.text.SetForegroundColour(wx.WHITE)
		self.fill.BackgroundColour = style.accent1
		self.Refresh()

class GenericButton(wx.Panel):
	def __init__(self, parent, label):

		self.disabled = False

		wx.Panel.__init__(self, parent)
		self.BackgroundColour = style.accent1

		self.fill = wx.Panel(self)
		self.fill.BackgroundColour = wx.WHITE

		self.text = wx.StaticText(self.fill, label=label)
		self.text.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.LIGHT))
		self.text.SetForegroundColour(style.accent1)

		sizer = wx.GridBagSizer()
		sizer.AddSpacer((2,2), (0,0))
		sizer.Add(self.fill, (1,1))
		sizer.AddSpacer((2,2), (2,2))
		self.SetSizer(sizer)

		self.fill.Bind(wx.EVT_LEFT_UP, self.onClick)
		self.fill.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver)
		self.fill.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseLeave)

	def onClick(self, event):
		if self.disabled:
			return
		clickEvent = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, self.GetId())
		clickEvent.SetEventObject(self)
		self.GetEventHandler().ProcessEvent(clickEvent)

	def onMouseOver(self, event):
		if self.disabled:
			return
		self.fill.BackgroundColour = style.mouse_over_colour
		self.Refresh()

	def onMouseLeave(self, event):
		if self.disabled:
			return
		self.fill.BackgroundColour = wx.WHITE
		self.Refresh()

	def disable(self):
		self.disabled = True
		self.BackgroundColour = style.accent2
		self.text.SetForegroundColour(style.accent2)
		self.Refresh()

	def enable(self):
		self.disabled = False
		self.BackgroundColour = style.accent1
		self.text.SetForegroundColour(style.accent1)
		self.Refresh()
