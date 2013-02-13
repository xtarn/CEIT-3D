import wx
import style

from gui.customControls import ToggleSwitch, GenericButton

class AdvancedPanel(wx.ScrolledWindow):
	def __init__(self, parent):
		wx.ScrolledWindow.__init__(self, parent)

		self.SetScrollRate(0,5)


		heading_font = wx.Font(16, wx.SWISS, wx.NORMAL, wx.LIGHT)
		small_font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.LIGHT)

		#---accuracy---
		head1_panel = wx.Panel(self)
		head1 = Text(head1_panel, 'Accuracy', heading_font, style.accent1)

		head1_1 = Text(head1_panel, 'Layer height (mm)', small_font)
		head1_2 = Text(head1_panel, 'Wall thickness (mm)', small_font)
		head1_3 = Text(head1_panel, 'Initial layer thickness (mm)', small_font)
		head1_4 = Text(head1_panel, 'Extra top/bottom wall (mm)', small_font)
		head1_5 = Text(head1_panel, "Enable 'skin'", small_font)

		self.layer_height = wx.TextCtrl(head1_panel)
		self.wall_thickness = wx.TextCtrl(head1_panel)
		self.initial_thickness = wx.TextCtrl(head1_panel)
		self.extra_wall = wx.TextCtrl(head1_panel)
		self.skin = wx.CheckBox(head1_panel)

		sizer = wx.GridBagSizer()
		sizer.Add(head1, (0,0), span=(1,4))
		sizer.AddSpacer((20,10), (1,0))
		sizer.AddSpacer((200,0), (1,1), span=(1,2))
		sizer.AddSpacer((0,25), (2,0))
		sizer.AddSpacer((0,25), (3,0))
		sizer.AddSpacer((0,25), (4,0))
		sizer.AddSpacer((0,25), (5,0))

		sizer.Add(head1_1, (2,1))
		sizer.Add(head1_2, (3,1))
		sizer.Add(head1_3, (4,1))
		sizer.Add(head1_4, (5,1))
		sizer.Add(head1_5, (6,1))

		sizer.Add(self.layer_height, (2,3))
		sizer.Add(self.wall_thickness, (3,3))
		sizer.Add(self.initial_thickness, (4,3))
		sizer.Add(self.extra_wall, (5,3))
		sizer.Add(self.skin, (6,3))
		head1_panel.SetSizer(sizer)

		#---fill---
		head2_panel = wx.Panel(self)
		head2 = Text(head2_panel, 'Fill', heading_font, style.accent1)

		head2_1 = Text(head2_panel, 'Bottom/Top thickness (mm)', small_font)
		head2_2 = Text(head2_panel, 'Fill density (&%)', small_font)
		head2_3 = Text(head2_panel, 'Infill pattern', small_font)
		head2_4 = Text(head2_panel, 'Infill overlap (&%)', small_font)
		head2_5 = Text(head2_panel, 'Solid infill top', small_font)
		head2_6 = Text(head2_panel, 'Print order sequence', small_font)

		self.bottom_top_thickness = wx.TextCtrl(head2_panel)
		self.fill_density = wx.TextCtrl(head2_panel)
		self.infill_pattern = wx.ComboBox(head2_panel, size=(120,25), style=wx.CB_READONLY, 
			choices=['Line', 'Grid Circular', 'Grid Hexagonal', 'Grid Rectangular'])
		self.infill_overlap = wx.TextCtrl(head2_panel)
		self.solid_top = wx.CheckBox(head2_panel)
		self.sequence = wx.ComboBox(head2_panel, size=(120,25), style=wx.CB_READONLY, 
			choices=['Loops > Perimeter > Infill', 'Loops > Infill > Perimeter', 'Infill > Loops > Perimeter', 
			'Infill > Perimeter > Loops', 'Perimeter > Infill > Loops', 'Perimeter > Loops > Infill'])

		sizer = wx.GridBagSizer()
		sizer.Add(head2, (0,0), span=(1,4))
		sizer.AddSpacer((20,10), (1,0))
		sizer.AddSpacer((200,0), (1,1), span=(1,2))
		sizer.AddSpacer((0,25), (2,0))
		sizer.AddSpacer((0,25), (3,0))
		sizer.AddSpacer((0,25), (4,0))
		sizer.AddSpacer((0,25), (5,0))
		sizer.AddSpacer((0,25), (6,0))

		sizer.Add(head2_1, (2,1))
		sizer.Add(head2_2, (3,1))
		sizer.Add(head2_3, (4,1))
		sizer.Add(head2_4, (5,1))
		sizer.Add(head2_5, (6,1))
		sizer.Add(head2_6, (7,1))

		sizer.Add(self.bottom_top_thickness, (2,3))
		sizer.Add(self.fill_density, (3,3))
		sizer.Add(self.infill_pattern, (4,3))
		sizer.Add(self.infill_overlap, (5,3))
		sizer.Add(self.solid_top, (6,3))
		sizer.Add(self.sequence, (7,3))
		head2_panel.SetSizer(sizer)

		#---speed---
		head3_panel = wx.Panel(self)
		head3 = Text(head3_panel, 'Speed', heading_font, style.accent1)

		head3_1 = Text(head3_panel, 'Print speed (mm/s)', small_font)
		head3_2 = Text(head3_panel, 'Travel speed (mm/s)', small_font)
		head3_3 = Text(head3_panel, 'Max Z speed (mm/s)', small_font)
		head3_4 = Text(head3_panel, 'Bottom layer speed (mm/s)', small_font)

		self.print_speed = wx.TextCtrl(head3_panel)
		self.travel_speed = wx.TextCtrl(head3_panel)
		self.max_z_speed = wx.TextCtrl(head3_panel)
		self.bottom_speed = wx.TextCtrl(head3_panel)

		sizer = wx.GridBagSizer()
		sizer.Add(head3, (0,0), span=(1,4))
		sizer.AddSpacer((20,10), (1,0))
		sizer.AddSpacer((200,0), (1,1), span=(1,2))
		sizer.AddSpacer((0,25), (2,0))
		sizer.AddSpacer((0,25), (3,0))
		sizer.AddSpacer((0,25), (4,0))

		sizer.Add(head3_1, (2,1))
		sizer.Add(head3_2, (3,1))
		sizer.Add(head3_3, (4,1))
		sizer.Add(head3_4, (5,1))
		sizer.Add(self.print_speed, (2,3))
		sizer.Add(self.travel_speed, (3,3))
		sizer.Add(self.max_z_speed, (4,3))
		sizer.Add(self.bottom_speed, (5,3))
		head3_panel.SetSizer(sizer)

		#---support---
		head4_panel = wx.Panel(self)
		head4 = Text(head4_panel, 'Support Structure', heading_font, style.accent1)
		
		head4_1 = Text(head4_panel, 'Support type', small_font)
		head4_2 = Text(head4_panel, 'Material amount (&%)', small_font)
		head4_3 = Text(head4_panel, 'Distance from object (mm)', small_font)

		self.support_type = wx.ComboBox(head4_panel, size=(120,25), style=wx.CB_READONLY, 
			choices=['None', 'Exterior Only', 'Everywhere'])
		self.support_material_amount = wx.TextCtrl(head4_panel)
		self.support_distance = wx.TextCtrl(head4_panel)

		sizer = wx.GridBagSizer()
		sizer.Add(head4, (0,0), span=(1,4))
		sizer.AddSpacer((20,10), (1,0))
		sizer.AddSpacer((200,0), (1,1), span=(1,2))
		sizer.AddSpacer((0,25), (2,0))
		sizer.AddSpacer((0,25), (3,0))

		sizer.Add(head4_1, (2,1))
		sizer.Add(head4_2, (3,1))
		sizer.Add(head4_3, (4,1))

		sizer.Add(self.support_type, (2,3))
		sizer.Add(self.support_material_amount, (3,3))
		sizer.Add(self.support_distance, (4,3))
		head4_panel.SetSizerAndFit(sizer)

		#---skirt---
		head5_panel = wx.Panel(self)
		head5 = Text(head5_panel, 'Skirt', heading_font, style.accent1)

		head5_1 = Text(head5_panel, 'Line count', small_font)
		head5_2 = Text(head5_panel, 'Start distance (mm)', small_font)

		self.skirt_count = wx.TextCtrl(head5_panel)
		self.skirt_distance = wx.TextCtrl(head5_panel)

		sizer = wx.GridBagSizer()
		sizer.Add(head5, (0,0), span=(1,4))
		sizer.AddSpacer((20,10), (1,0))
		sizer.AddSpacer((200,0), (1,1), span=(1,2))
		sizer.AddSpacer((0,25), (2,0))

		sizer.Add(head5_1, (2,1))
		sizer.Add(head5_2, (3,1))

		sizer.Add(self.skirt_count, (2,3))
		sizer.Add(self.skirt_distance, (3,3))
		head5_panel.SetSizer(sizer)

		#---fillament---
		head6_panel = wx.Panel(self)
		head6 = Text(head6_panel, 'Fillament', heading_font, style.accent1)

		head6_1 = Text(head6_panel, 'Diameter (mm)', small_font)
		head6_2 = Text(head6_panel, 'Packing density', small_font)
		head6_3 = Text(head6_panel, 'Printing temperature', small_font)

		self.fillament_diameter = wx.TextCtrl(head6_panel)
		self.packing_density = wx.TextCtrl(head6_panel)
		self.print_temperature = wx.TextCtrl(head6_panel)

		sizer = wx.GridBagSizer()
		sizer.Add(head6, (0,0), span=(1,4))
		sizer.AddSpacer((20,10), (1,0))
		sizer.AddSpacer((200,0), (1,1), span=(1,2))
		sizer.AddSpacer((0,25), (2,0))
		sizer.AddSpacer((0,25), (3,0))

		sizer.Add(head6_1, (2,1))
		sizer.Add(head6_2, (3,1))
		sizer.Add(head6_3, (4,1))
		sizer.Add(self.fillament_diameter, (2,3))
		sizer.Add(self.packing_density, (3,3))
		sizer.Add(self.print_temperature, (4,3))
		head6_panel.SetSizer(sizer)

		#---machine size---
		head7_panel = wx.Panel(self)
		head7 = Text(head7_panel, 'Machine Size', heading_font, style.accent1)

		head7_1 = Text(head7_panel, 'Nozzle size (mm)', small_font)
		head7_2 = Text(head7_panel, 'Machine center X (mm)', small_font)
		head7_3 = Text(head7_panel, 'Machine center Y (mm)', small_font)

		self.nozzle_size = wx.TextCtrl(head7_panel)
		self.machine_x_center = wx.TextCtrl(head7_panel)
		self.machine_y_center = wx.TextCtrl(head7_panel)

		sizer = wx.GridBagSizer()
		sizer.Add(head7, (0,0), span=(1,4))
		sizer.AddSpacer((20,10), (1,0))
		sizer.AddSpacer((200,0), (1,1), span=(1,2))
		sizer.AddSpacer((0,25), (2,0))
		sizer.AddSpacer((0,25), (3,0))

		sizer.Add(head7_1, (2,1))
		sizer.Add(head7_2, (3,1))
		sizer.Add(head7_3, (4,1))

		sizer.Add(self.nozzle_size, (2,3))
		sizer.Add(self.machine_x_center, (3,3))
		sizer.Add(self.machine_y_center, (4,3))
		head7_panel.SetSizer(sizer)

		#---Retraction---
		head8_panel = wx.Panel(self)
		head8 = Text(head8_panel, 'Retraction', heading_font, style.accent1)

		head8_1 = Text(head8_panel, 'Enable retraction', small_font)
		head8_2 = Text(head8_panel, 'Retract on jumps only', small_font)
		head8_3 = Text(head8_panel, 'Minimal travel (mm)', small_font)
		head8_4 = Text(head8_panel, 'Speed (mm/s)', small_font)
		head8_5 = Text(head8_panel, 'Distance (mm)', small_font)
		head8_6 = Text(head8_panel, 'Extra length on start (mm)', small_font)

		self.retraction = wx.CheckBox(head8_panel)
		self.retract_on_jumps = wx.CheckBox(head8_panel)
		self.retract_min_travel = wx.TextCtrl(head8_panel)
		self.retract_speed = wx.TextCtrl(head8_panel)
		self.retract_distance = wx.TextCtrl(head8_panel)
		self.retract_extra = wx.TextCtrl(head8_panel)

		sizer = wx.GridBagSizer()
		sizer.Add(head8, (0,0), span=(1,4))
		sizer.AddSpacer((20,10), (1,0))
		sizer.AddSpacer((200,0), (1,1), span=(1,2))
		sizer.AddSpacer((0,25), (2,0))
		sizer.AddSpacer((0,25), (3,0))
		sizer.AddSpacer((0,25), (4,0))
		sizer.AddSpacer((0,25), (5,0))
		sizer.AddSpacer((0,25), (6,0))

		sizer.Add(head8_1, (2,1))
		sizer.Add(head8_2, (3,1))
		sizer.Add(head8_3, (4,1))
		sizer.Add(head8_4, (5,1))
		sizer.Add(head8_5, (6,1))
		sizer.Add(head8_6, (7,1))

		sizer.Add(self.retraction, (2,3))
		sizer.Add(self.retract_on_jumps, (3,3))
		sizer.Add(self.retract_min_travel, (4,3))
		sizer.Add(self.retract_speed, (5,3))
		sizer.Add(self.retract_distance, (6,3))
		sizer.Add(self.retract_extra, (7,3))
		head8_panel.SetSizer(sizer)

		#---cooling---
		head9_panel = wx.Panel(self)
		head9 = Text(head9_panel, 'Cooling', heading_font, style.accent1)

		head9_1 = Text(head9_panel, 'Minimal layer time (s)', small_font)
		head9_2 = Text(head9_panel, 'Enable cooling fan', small_font)
		head9_3 = Text(head9_panel, 'Minimum feedrate (mm/s)', small_font)
		head9_4 = Text(head9_panel, 'Fan on layer number', small_font)
		head9_5 = Text(head9_panel, 'Fan speed min (&%)', small_font)
		head9_6 = Text(head9_panel, 'Fan speed max (&%)', small_font)

		self.min_layer_time = wx.TextCtrl(head9_panel)
		self.enable_fan = wx.CheckBox(head9_panel)
		self.min_feedrate = wx.TextCtrl(head9_panel)
		self.fan_layer = wx.TextCtrl(head9_panel)
		self.fan_min_speed = wx.TextCtrl(head9_panel)
		self.fan_max_speed = wx.TextCtrl(head9_panel)

		sizer = wx.GridBagSizer()
		sizer.Add(head9, (0,0), span=(1,4))
		sizer.AddSpacer((20,10), (1,0))
		sizer.AddSpacer((200,0), (1,1), span=(1,2))
		sizer.AddSpacer((0,25), (2,0))
		sizer.AddSpacer((0,25), (3,0))
		sizer.AddSpacer((0,25), (4,0))
		sizer.AddSpacer((0,25), (5,0))
		sizer.AddSpacer((0,25), (6,0))

		sizer.Add(head9_1, (2,1))
		sizer.Add(head9_2, (3,1))
		sizer.Add(head9_3, (4,1))
		sizer.Add(head9_4, (5,1))
		sizer.Add(head9_5, (6,1))
		sizer.Add(head9_6, (7,1))

		sizer.Add(self.min_layer_time, (2,3))
		sizer.Add(self.enable_fan, (3,3))
		sizer.Add(self.min_feedrate, (4,3))
		sizer.Add(self.fan_layer, (5,3))
		sizer.Add(self.fan_min_speed, (6,3))
		sizer.Add(self.fan_max_speed, (7,3))
		head9_panel.SetSizer(sizer)

		#---raft---
		head10_panel = wx.Panel(self)
		head10 = Text(head10_panel, 'Raft', heading_font, style.accent1)

		head10_1 = Text(head10_panel, 'Add raft', small_font)
		head10_2 = Text(head10_panel, 'Extra margin (mm)', small_font)
		head10_3 = Text(head10_panel, 'Base material amount (&%)', small_font)
		head10_4 = Text(head10_panel, 'Interface amount (&%)', small_font)

		self.add_raft = wx.CheckBox(head10_panel)
		self.raft_margin = wx.TextCtrl(head10_panel)
		self.raft_base = wx.TextCtrl(head10_panel)
		self.raft_interface = wx.TextCtrl(head10_panel)

		sizer = wx.GridBagSizer()
		sizer.Add(head9, (0,0), span=(1,4))
		sizer.AddSpacer((20,10), (1,0))
		sizer.AddSpacer((200,0), (1,1), span=(1,2))
		sizer.AddSpacer((0,25), (2,0))
		sizer.AddSpacer((0,25), (3,0))
		sizer.AddSpacer((0,25), (4,0))

		sizer.Add(head10_1, (2,1))
		sizer.Add(head10_2, (3,1))
		sizer.Add(head10_3, (4,1))
		sizer.Add(head10_4, (5,1))

		sizer.Add(self.add_raft, (2,3))
		sizer.Add(self.raft_margin, (3,3))
		sizer.Add(self.raft_base, (4,3))
		sizer.Add(self.raft_interface, (5,3))
		head10_panel.SetSizer(sizer)

		#---reset---
		reset = GenericButton(self, 'Reset All')
		reset.Bind(wx.EVT_BUTTON, self.doReset)	

		# # ---scroll sizer----
		sizer = wx.GridBagSizer()
		sizer.AddSpacer((30,20), (0,0))
		sizer.Add(head1_panel, (1,1))
		sizer.AddSpacer((1,20), (2,1))
		sizer.Add(head2_panel, (3,1))
		sizer.AddSpacer((1,20), (4,1))
		sizer.Add(head3_panel, (5,1))
		sizer.AddSpacer((1,20), (6,1))
		sizer.Add(head4_panel, (7,1))
		sizer.AddSpacer((1,20), (8,1))
		sizer.Add(head5_panel, (9,1))
		sizer.AddSpacer((1,20), (10,1))
		sizer.Add(head6_panel, (11,1))
		sizer.AddSpacer((1,20), (12,1))
		sizer.Add(head7_panel, (13,1))
		sizer.AddSpacer((1,20), (14,1))
		sizer.Add(head8_panel, (15,1))
		sizer.AddSpacer((1,20), (16,1))
		sizer.Add(head9_panel, (17,1))
		sizer.AddSpacer((1,20), (18,1))
		sizer.Add(head10_panel, (19,1))
		sizer.AddSpacer((1,20), (20,1))
		sizer.Add(reset, (21,1))
		sizer.AddSpacer((1,20), (22,1))

		self.SetSizerAndFit(sizer)

		self.initSettings()

	def initSettings(self):
		self.layer_height.SetValue('0.2')
		self.wall_thickness.SetValue('0.8')
		self.initial_thickness.SetValue('0.0')
		self.extra_wall.SetValue('0.0')
		self.skin.SetValue(False)
		self.bottom_top_thickness.SetValue('0.6')
		self.fill_density.SetValue('20')
		self.infill_pattern.SetValue('Line')
		self.infill_overlap.SetValue('20')
		self.solid_top.SetValue(True)
		self.sequence.SetValue('Loops > Perimeter > Infill')
		self.print_speed.SetValue('50')
		self.travel_speed.SetValue('150')
		self.max_z_speed.SetValue('3.0')
		self.bottom_speed.SetValue('25')
		self.support_type.SetValue('None')
		self.support_material_amount.SetValue('50')
		self.support_distance.SetValue('0.5')
		self.skirt_count.SetValue('1')
		self.skirt_distance.SetValue('6.0')
		self.fillament_diameter.SetValue('2.7')
		self.packing_density.SetValue('1.00')
		self.print_temperature.SetValue('225')
		self.nozzle_size.SetValue('0.4')
		self.machine_x_center.SetValue('100')
		self.machine_y_center.SetValue('100')
		self.retraction.SetValue(False)
		self.retract_on_jumps.SetValue(False)
		self.retract_min_travel.SetValue('5.0')
		self.retract_speed.SetValue('40.0')
		self.retract_distance.SetValue('4.5')
		self.retract_extra.SetValue('0.0')
		self.min_layer_time.SetValue('10')
		self.enable_fan.SetValue(True)
		self.min_feedrate.SetValue('5')
		self.fan_layer.SetValue('1')
		self.fan_min_speed.SetValue('100')
		self.fan_max_speed.SetValue('100')
		self.add_raft.SetValue(False)
		self.raft_margin.SetValue('5')
		self.raft_base.SetValue('100')
		self.raft_interface.SetValue('100')

	def doSettings(self, settings = {}):

		try: self.layer_height.SetValue(settings['layer_height'])
		except: pass

		try: self.wall_thickness.SetValue(settings['wall_thickness'])
		except: pass

		try: self.initial_thickness.SetValue(settings['initial_thickness'])
		except: pass

		try: self.extra_wall.SetValue(settings['extra_wall'])
		except: pass

		try: self.skin.SetValue(settings['skin'])
		except: pass

		try: self.bottom_top_thickness.SetValue(settings['bottom_top_thickness'])
		except: pass

		try: self.fill_density.SetValue(settings['fill_density'])
		except: pass

		try: self.infill_pattern.SetValue(settings['infill_pattern'])
		except: pass

		try: self.infill_overlap.SetValue(settings['infill_overlap'])
		except: pass

		try: self.solid_top.SetValue(settings['solid_top'])
		except: pass

		try: self.sequence.SetValue(settings['sequence'])
		except: pass

		try: self.print_speed.SetValue(settings['print_speed'])
		except: pass

		try: self.travel_speed.SetValue(settings['travel_speed'])
		except: pass

		try: self.max_z_speed.SetValue(settings['max_z_speed'])
		except: pass

		try: self.bottom_speed.SetValue(settings['bottom_speed'])
		except: pass

		try: self.support_type.SetValue(settings['support_type'])
		except: pass

		try: self.support_material_amount.SetValue(settings['support_material_amount'])
		except: pass

		try: self.support_distance.SetValue(settings['support_distance'])
		except: pass

		try: self.skirt_count.SetValue(settings['skirt_count'])
		except: pass

		try: self.skirt_distance.SetValue(settings['skirt_distance'])
		except: pass

		try: self.fillament_diameter.SetValue(settings['fillament_diameter'])
		except: pass

		try: self.packing_density.SetValue(settings['packing_density'])
		except: pass

		try: self.print_temperature.SetValue(settings['print_temperature'])
		except: pass

		try: self.nozzle_size.SetValue(settings['nozzle_size'])
		except: pass

		try: self.machine_x_center.SetValue(settings['machine_x_center'])
		except: pass

		try: self.machine_y_center.SetValue(settings['machine_y_center'])
		except: pass

		try: self.retraction.SetValue(settings['retraction'])
		except: pass

		try: self.retract_on_jumps.SetValue(settings['retract_on_jumps'])
		except: pass

		try: self.retract_min_travel.SetValue(settings['retract_min_travel'])
		except: pass

		try: self.retract_speed.SetValue(settings['retract_speed'])
		except: pass

		try: self.retract_distance.SetValue(settings['retract_distance'])
		except: pass

		try: self.retract_extra.SetValue(settings['retract_extra'])
		except: pass

		try: self.min_layer_time.SetValue(settings['min_layer_time'])
		except: pass

		try: self.enable_fan.SetValue(settings['enable_fan'])
		except: pass

		try: self.min_feedrate.SetValue(settings['min_feedrate'])
		except: pass

		try: self.fan_layer.SetValue(settings['fan_layer'])
		except: pass

		try: self.fan_min_speed.SetValue(settings['fan_min_speed'])
		except: pass

		try: self.fan_max_speed.SetValue(settings['fan_max_speed'])
		except: pass

		try: self.add_raft.SetValue(settings['add_raft'])
		except: pass

		try: self.raft_margin.SetValue(settings['raft_margin'])
		except: pass

		try: self.raft_base.SetValue(settings['raft_base'])
		except: pass

		try: self.raft_interface.SetValue(settings['raft_interface'])
		except: pass

		self.Refresh()
		return
		
	def doReset(self, event):
		self.initSettings()

		basic = self.GetParent().GetParent().GetParent().step3_panel

		settings = {}

		if basic.low_button.isSelected():
			settings['wall_thickness'] = '0.4'
			settings['layer_height'] = '0.25'
			settings['fill_density'] = '10'
			settings['bottom_top_thickness'] = '0.5'
		elif basic.med_button.isSelected():
			settings['wall_thickness'] = '0.8'
			settings['layer_height'] = '0.2'
			settings['fill_density'] = '30'
			settings['bottom_top_thickness'] = '0.6'
		elif basic.high_button.isSelected():
			settings['wall_thickness'] = '0.8'
			settings['layer_height'] = '0.1'
			settings['fill_density'] = '40'
			settings['bottom_top_thickness'] = '0.4'
		elif basic.ultra_button.isSelected():
			settings['wall_thickness'] = '1.2'
			settings['layer_height'] = '0.1'
			settings['fill_density'] = '50'
			settings['bottom_top_thickness'] = '0.6'
			settings['skin'] = True
			settings['infill_pattern'] = 'Grid Hexagonal'
			
		if basic.hollow_button.isSelected():
			settings['fill_density'] = '0'
		elif basic.solid_button.isSelected():
			settings['fill_density'] = '100'

		if basic.getSelectedMaterial() != None:
			settings['print_temperature'] = basic.getSelectedMaterial()[3]
			settings['fillament_diameter'] = basic.getSelectedMaterial()[4]

		if basic.support_button.isSelected():
			settings['support_type'] = 'Exterior Only'

		self.doSettings(settings)

class Text(wx.StaticText):
	def __init__(self, parent, label, font, colour=wx.BLACK):
		wx.StaticText.__init__(self, parent, label=label)
		self.SetFont(font)
		self.SetForegroundColour(colour)


