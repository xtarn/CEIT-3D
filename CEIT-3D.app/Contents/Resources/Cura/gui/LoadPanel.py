import wx
import style

from gui.customControls import GenericButton
from util import meshLoader
from util import profile

class LoadPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, size=(style.width*3+1, style.height*7+1))

		load_model = GenericButton(self, label='Load Model\t\t\t')
		load_model.Bind(wx.EVT_BUTTON, self.onLoad)

		load_gcode = GenericButton(self, label='Load Gcode\t\t\t')
		#load_gcode.Bind

		load_web = GenericButton(self, label='Load From Thingiverse\t')
		#load_web.Bind

		#load_settings = GenericButton(self, label='Load Custom Settings\t')
		#load_settings.Bind

		load_gcode.disable()
		load_web.disable()


		sizer = wx.GridBagSizer()
		sizer.AddSpacer((30,20), (0,0))
		sizer.Add(load_model, (1,1))
		sizer.AddSpacer((0,20), (2,1))
		sizer.Add(load_gcode, (3,1))
		sizer.AddSpacer((0,20), (4,1))
		sizer.Add(load_web, (5,1))

		self.SetSizerAndFit(sizer)

	def onLoad(self, event):

		dlg = wx.FileDialog(self, "Open file to print", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		dlg.SetWildcard(meshLoader.wildcardFilter())

		if dlg.ShowModal() == wx.ID_OK:
			frame = self.GetParent().GetParent().GetParent()
			frame.filename = dlg.GetPath() 
			frame.step5_panel.ClearPrintSummary()
			profile.putPreference('lastFile', frame.filename)
			transform = frame.step2_panel
			transform.load(frame.filename)
			frame.onNext(None)
		dlg.Destroy()