import wx

from gui.customControls import NextButton

from gui import LoadPanel, TransformPanel, SettingsPanel, AdvancedPanel, PrintPanel, StatusPanel
import style


class MyFrame(wx.Frame):
	def __init__(self, parent, id, title):

		noResize_frameStyle = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION
		wx.Frame.__init__(self, parent, id, title, size=(880, 60*7+22), style=noResize_frameStyle)

		self.panel = wx.Panel(self)

		self.heading_panel = wx.Panel(self.panel, size=(style.width, style.height))
		self.heading_panel.BackgroundColour = style.mouse_off_colour

		heading = wx.StaticText(self.heading_panel, label='\tSteps:')
		heading.SetFont(wx.Font(30, wx.SWISS, wx.NORMAL, wx.LIGHT))
		heading.SetForegroundColour(style.accent1)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.AddSpacer(5)
		sizer.Add(heading)
		self.heading_panel.SetSizer(sizer)

		self.step1_tab = wx.Panel(self.panel, size=(style.width, style.height))
		self.step1_tab.BackgroundColour = style.accent1
		self.step1_tab.Bind(wx.EVT_LEFT_UP, self.onTabClick)
		self.step1_tab.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver)
		self.step1_tab.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseLeave)

		self.step1_heading = wx.StaticText(self.step1_tab, label='\t Load')
		self.step1_heading.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.LIGHT))
		self.step1_heading.SetForegroundColour(wx.WHITE)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.AddSpacer(10)
		sizer.Add(self.step1_heading)
		self.step1_tab.SetSizer(sizer)

		self.step2_tab = wx.Panel(self.panel, size=(style.width, style.height))
		self.step2_tab.BackgroundColour = style.mouse_off_colour
		self.step2_tab.Bind(wx.EVT_LEFT_UP, self.onTabClick)
		self.step2_tab.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver)
		self.step2_tab.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseLeave)

		self.step2_heading = wx.StaticText(self.step2_tab, label='\t Position')
		self.step2_heading.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.LIGHT))

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.AddSpacer(10)
		sizer.Add(self.step2_heading)
		self.step2_tab.SetSizer(sizer)

		self.step3_tab = wx.Panel(self.panel, size=(style.width, style.height))
		self.step3_tab.BackgroundColour = style.mouse_off_colour
		self.step3_tab.Bind(wx.EVT_LEFT_UP, self.onTabClick)
		self.step3_tab.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver)
		self.step3_tab.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseLeave)

		self.step3_heading = wx.StaticText(self.step3_tab, label='\t Slicer Settings')
		self.step3_heading.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.LIGHT))


		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.AddSpacer(10)
		sizer.Add(self.step3_heading)
		self.step3_tab.SetSizer(sizer)

		self.step4_tab = wx.Panel(self.panel, size=(style.width, style.height))
		self.step4_tab.BackgroundColour = style.mouse_off_colour
		self.step4_tab.Bind(wx.EVT_LEFT_UP, self.onTabClick)
		self.step4_tab.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver)
		self.step4_tab.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseLeave)

		self.step4_heading = wx.StaticText(self.step4_tab, label='\t Advanced Settings')
		self.step4_heading.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.LIGHT))

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.AddSpacer(10)
		sizer.Add(self.step4_heading)
		self.step4_tab.SetSizer(sizer)


		self.step5_tab = wx.Panel(self.panel, size=(style.width, style.height))
		self.step5_tab.BackgroundColour = style.mouse_off_colour
		self.step5_tab.Bind(wx.EVT_LEFT_UP, self.onTabClick)
		self.step5_tab.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver)
		self.step5_tab.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseLeave)

		self.step5_heading = wx.StaticText(self.step5_tab, label='\t Slice && Print')
		self.step5_heading.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.LIGHT))

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.AddSpacer(10)
		sizer.Add(self.step5_heading)
		self.step5_tab.SetSizer(sizer)

		self.step6_tab = wx.Panel(self.panel, size=(style.width, style.height))
		self.step6_tab.BackgroundColour = style.mouse_off_colour
		self.step6_tab.Bind(wx.EVT_LEFT_UP, self.onTabClick)
		self.step6_tab.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver)
		self.step6_tab.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseLeave)

		self.step6_heading = wx.StaticText(self.step6_tab, label='\t Printer Status')
		self.step6_heading.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.LIGHT))

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.AddSpacer(10)
		sizer.Add(self.step6_heading)
		self.step6_tab.SetSizer(sizer)

		input_panel = wx.Panel(self.panel, size=(880-style.width, 421))
		input_panel.BackgroundColour = wx.WHITE

		self.step1_panel = LoadPanel.LoadPanel(input_panel)
		self.step2_panel = TransformPanel.TransformPanel(input_panel)
		self.step3_panel = SettingsPanel.SettingsPanel(input_panel)
		self.step4_panel = AdvancedPanel.AdvancedPanel(input_panel)
		self.step5_panel = PrintPanel.PrintPanel(input_panel)
		self.step6_panel = StatusPanel.StatusPanel(input_panel)

		self.step2_panel.Hide()
		self.step3_panel.Hide()
		self.step4_panel.Hide()
		self.step5_panel.Hide()
		self.step6_panel.Hide()

		self.next = NextButton(input_panel)
		self.next.Bind(wx.EVT_BUTTON, self.onNext)

		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.step1_panel, flag=wx.EXPAND)
		self.sizer.Add(self.step2_panel, flag=wx.EXPAND)
		self.sizer.Add(self.step3_panel, flag=wx.EXPAND)
		self.sizer.Add(self.step4_panel, flag=wx.EXPAND)
		self.sizer.Add(self.step5_panel, flag=wx.EXPAND)
		self.sizer.Add(self.step6_panel, flag=wx.EXPAND)
		input_panel.SetSizer(self.sizer)

		sizer = wx.GridBagSizer()
		sizer.Add(self.heading_panel, (0,0))
		sizer.Add(self.step1_tab, (1,0))
		sizer.Add(self.step2_tab , (2,0))
		sizer.Add(self.step3_tab, (3,0))
		sizer.Add(self.step4_tab, (4,0))
		sizer.Add(self.step5_tab, (5,0))
		sizer.Add(self.step6_tab, (6,0))
		sizer.Add(input_panel, (0,1), span=(8,1))

		self.panel.SetSizerAndFit(sizer)
		self.step2_heading.SetForegroundColour(style.accent2)
		self.step3_heading.SetForegroundColour(style.accent2)
		self.step4_heading.SetForegroundColour(style.accent2)
		self.step5_heading.SetForegroundColour(style.accent2)

		self.filename = None
		

	def onTabClick(self, event, tab=None): 
		if tab == None:
			tab = event.GetEventObject()
			if tab == self.step1_tab and self.step1_heading.ForegroundColour == style.accent2:
				return
			elif tab == self.step2_tab and self.step2_heading.ForegroundColour == style.accent2:
				return
			elif tab == self.step3_tab and self.step3_heading.ForegroundColour == style.accent2:
				return
			elif tab == self.step4_tab and self.step4_heading.ForegroundColour == style.accent2:
				return
			elif tab == self.step5_tab and self.step5_heading.ForegroundColour == style.accent2:
				return
			elif tab == self.step6_tab and self.step6_heading.ForegroundColour == style.accent2:
				return

		if tab == self.step5_tab:
			self.step5_panel.UpdateSettingSummary() #raises exception

		if tab == self.step2_tab and self.filename == None:
			raise Exception

		self.step1_tab.BackgroundColour = style.mouse_off_colour
		self.step2_tab.BackgroundColour = style.mouse_off_colour
		self.step3_tab.BackgroundColour = style.mouse_off_colour
		self.step4_tab.BackgroundColour = style.mouse_off_colour
		self.step5_tab.BackgroundColour = style.mouse_off_colour
		self.step6_tab.BackgroundColour = style.mouse_off_colour

		if self.step1_heading.ForegroundColour == wx.WHITE:
			self.step1_heading.SetForegroundColour(wx.BLACK)
		if self.step2_heading.ForegroundColour == wx.WHITE:
			self.step2_heading.SetForegroundColour(wx.BLACK)
		if self.step3_heading.ForegroundColour == wx.WHITE:
			self.step3_heading.SetForegroundColour(wx.BLACK)
		if self.step4_heading.ForegroundColour == wx.WHITE:
			self.step4_heading.SetForegroundColour(wx.BLACK)
		if self.step5_heading.ForegroundColour == wx.WHITE:
			self.step5_heading.SetForegroundColour(wx.BLACK)
		if self.step6_heading.ForegroundColour == wx.WHITE:
			self.step6_heading.SetForegroundColour(wx.BLACK)

		self.step1_panel.Hide()
		self.step2_panel.Hide()
		self.step3_panel.Hide()
		self.step4_panel.Hide()
		self.step5_panel.Hide()
		self.step6_panel.Hide()
		self.next.Show()

		if tab == self.step1_tab:
			self.step1_heading.SetForegroundColour(wx.WHITE)
			self.step1_panel.Show()
		elif tab == self.step2_tab:
			self.step2_heading.SetForegroundColour(wx.WHITE)
			self.step2_panel.Show()
		elif tab == self.step3_tab:
			self.step3_heading.SetForegroundColour(wx.WHITE)
			self.step3_panel.Show()
		elif tab == self.step4_tab:
			self.step4_heading.SetForegroundColour(wx.WHITE)
			self.step4_panel.Show()
		elif tab == self.step5_tab:
			self.step5_heading.SetForegroundColour(wx.WHITE)
			self.step5_panel.Show()
		elif tab == self.step6_tab: 
			self.step6_heading.SetForegroundColour(wx.WHITE)
			self.step6_panel.Show()
			self.next.Hide()
			self.next.onMouseLeave(None)

		self.sizer.Layout()
		tab.BackgroundColour = style.accent1
		self.Refresh()
	

	def onMouseOver(self, event):
		tab = event.GetEventObject()
		if tab.BackgroundColour == style.accent1:
			return
		tab.BackgroundColour = style.mouse_over_colour
		self.Refresh()

	def onMouseLeave(self, event):
		tab = event.GetEventObject()
		if tab.BackgroundColour == style.accent1:
			return

		tab.BackgroundColour = style.mouse_off_colour
		self.Refresh()

	def onNext(self, event):
		if self.step1_tab.BackgroundColour == style.accent1:
			try:
				self.onTabClick(None, self.step2_tab)
			except:
				wx.MessageDialog(self, 'You need to load a file first.', caption='Load Error', style=wx.OK|wx.CENTRE).ShowModal()
				return
			self.step3_heading.SetForegroundColour(wx.BLACK)
		elif self.step2_tab.BackgroundColour == style.accent1:
			self.onTabClick(None, self.step3_tab)
		elif self.step3_tab.BackgroundColour == style.accent1:
			try:
				self.onTabClick(None, self.step5_tab)
			except:
				wx.MessageDialog(self, 'You need to pick a quality and material first.', caption='Setting Error', style=wx.OK|wx.CENTRE).ShowModal()
				return
			self.step4_heading.SetForegroundColour(wx.BLACK)
		elif self.step4_tab.BackgroundColour == style.accent1:
			try:
				self.onTabClick(None, self.step5_tab)
			except:
				wx.MessageDialog(self, 'You need to pick a quality and material first.', caption='Setting Error', style=wx.OK|wx.CENTRE).ShowModal()
				return
		elif self.step5_tab.BackgroundColour == style.accent1:
			self.onTabClick(None, self.step6_tab)


class MyApp(wx.App):
	def OnInit(self):
		frame = MyFrame(None, -1, 'Cura v2')
		frame.Show(True)
		self.SetTopWindow(frame)
		return True


def main():
	app = MyApp(0)
	app.MainLoop()

if __name__ == '__main__':
	main()