from __future__ import division

import sys, math, threading, re, time, os
import numpy

from wx import glcanvas
import wx
try:
	import OpenGL
	OpenGL.ERROR_CHECKING = False
	from OpenGL.GLU import *
	from OpenGL.GL import *
	hasOpenGLlibs = True
except:
	print "Failed to find PyOpenGL: http://pyopengl.sourceforge.net/"
	hasOpenGLlibs = False

from gui import opengl
from util import profile
from util import meshLoader
from util import util3d

class previewObject():
	def __init__(self):
		self.mesh = None
		self.filename = None
		self.displayList = None
		self.dirty = False

class previewPanel(wx.Panel):
	def __init__(self, parent):
		super(previewPanel, self).__init__(parent,-1)
		
		self.SetMinSize((380,320))

		self.objectList = []
		self.errorList = []
		self.gcode = None
		self.objectsMinV = None
		self.objectsMaxV = None
		self.loadThread = None
		self.machineSize = util3d.Vector3(205, 205, 200)
		self.machineCenter = util3d.Vector3(100, 100.0, 0)

		self.glCanvas = PreviewGLCanvas(self)
		self.OnViewChange()
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.glCanvas, 1, flag=wx.EXPAND)
		self.SetSizer(sizer)

		self.scale = 1.0
		self.mirrorx = False
		self.mirrory = False
		self.mirrorz = False
		self.flipxy = False
		self.flipyz = False

	def OnScale(self, scale):
		self.scale = scale
		profile.putProfileSetting('model_scale', scale)
		self.glCanvas.Refresh()
	
	def OnScaleMax(self, e):
		if self.objectsMinV == None:
			return
		vMin = self.objectsMinV
		vMax = self.objectsMaxV
		scaleX1 = (self.machineSize.x - self.machineCenter.x) / ((vMax[0] - vMin[0]) / 2)
		scaleY1 = (self.machineSize.y - self.machineCenter.y) / ((vMax[1] - vMin[1]) / 2)
		scaleX2 = (self.machineCenter.x) / ((vMax[0] - vMin[0]) / 2)
		scaleY2 = (self.machineCenter.y) / ((vMax[1] - vMin[1]) / 2)
		scaleZ = self.machineSize.z / (vMax[2] - vMin[2])
		self.scale = min(scaleX1, scaleY1, scaleX2, scaleY2, scaleZ)
		self.glCanvas.Refresh()

	
	def loadModelFiles(self, filelist, showWarning = False):
		while len(filelist) > len(self.objectList):
			self.objectList.append(previewObject())
		for idx in xrange(len(filelist), len(self.objectList)):
			self.objectList[idx].mesh = None
			self.objectList[idx].filename = None
		for idx in xrange(0, len(filelist)):
			obj = self.objectList[idx]
			if obj.filename != filelist[idx]:
				obj.fileTime = None
				self.logFileTime = None
			obj.filename = filelist[idx]
		
		#Do the STL file loading in a background thread so we don't block the UI.
		if self.loadThread != None and self.loadThread.isAlive():
			self.loadThread.join()
		self.loadThread = threading.Thread(target=self.doFileLoadThread)
		self.loadThread.daemon = True
		self.loadThread.start()
		
	
	def doFileLoadThread(self):
		for obj in self.objectList:
			if obj.filename != None and os.path.isfile(obj.filename) and obj.fileTime != os.stat(obj.filename).st_mtime:
				obj.ileTime = os.stat(obj.filename).st_mtime
				mesh = meshLoader.loadMesh(obj.filename)
				obj.dirty = False
				obj.mesh = mesh
				self.updateModelTransform()
				scale = self.scale
				size = (self.objectsMaxV - self.objectsMinV) * scale
				if size[0] > self.machineSize.x or size[1] > self.machineSize.y or size[2] > self.machineSize.z:
					self.OnScaleMax(None)
				self.glCanvas.zoom = numpy.max(size) * 2.5
				self.errorList = []
				wx.CallAfter(self.glCanvas.Refresh)
	
	
	def OnViewChange(self):	
		self.glCanvas.viewMode = "Normal"
		self.glCanvas.drawBorders = False
		self.glCanvas.Refresh()
	
	def updateModelTransform(self, f=0):
		if len(self.objectList) < 1 or self.objectList[0].mesh == None:
			return
		
		rotate = 0
		mirrorX = self.mirrorx
		mirrorY = self.mirrory
		mirrorZ = self.mirrorz
		swapXZ = self.flipxy
		swapYZ = self.flipyz

		profile.putProfileSetting('model_scale', self.scale)
		profile.putProfileSetting('model_rotate_base', '0')
		profile.putProfileSetting('flip_x', mirrorX)
		profile.putProfileSetting('flip_y', mirrorY)
		profile.putProfileSetting('flip_z', mirrorZ)
		profile.putProfileSetting('swap_xz', swapXZ)
		profile.putProfileSetting('swap_yz', swapYZ)

		for obj in self.objectList:
			if obj.mesh == None:
				continue
			obj.mesh.setRotateMirror(rotate, mirrorX, mirrorY, mirrorZ, swapXZ, swapYZ)
		
		minV = self.objectList[0].mesh.getMinimum()
		maxV = self.objectList[0].mesh.getMaximum()
		for obj in self.objectList:
			if obj.mesh == None:
				continue

			obj.mesh.getMinimumZ()
			minV = numpy.minimum(minV, obj.mesh.getMinimum())
			maxV = numpy.maximum(maxV, obj.mesh.getMaximum())

		self.objectsMaxV = maxV
		self.objectsMinV = minV
		for obj in self.objectList:
			if obj.mesh == None:
				continue

			obj.mesh.vertexes -= numpy.array([minV[0] + (maxV[0] - minV[0]) / 2, minV[1] + (maxV[1] - minV[1]) / 2, minV[2]])
			obj.mesh.getMinimumZ()
			obj.dirty = True
		self.glCanvas.Refresh()
	

class PreviewGLCanvas(glcanvas.GLCanvas):
	def __init__(self, parent):
		attribList = (glcanvas.WX_GL_RGBA, glcanvas.WX_GL_DOUBLEBUFFER, glcanvas.WX_GL_DEPTH_SIZE, 24, glcanvas.WX_GL_STENCIL_SIZE, 8)
		glcanvas.GLCanvas.__init__(self, parent, attribList = attribList)
		self.parent = parent
		self.context = glcanvas.GLContext(self)
		wx.EVT_PAINT(self, self.OnPaint)
		wx.EVT_SIZE(self, self.OnSize)
		wx.EVT_ERASE_BACKGROUND(self, self.OnEraseBackground)
		wx.EVT_MOTION(self, self.OnMouseMotion)
		wx.EVT_MOUSEWHEEL(self, self.OnMouseWheel)
		self.yaw = 30
		self.pitch = 60
		self.zoom = 300
		self.offsetX = 0
		self.offsetY = 0
		self.view3D = True
		self.gcodeDisplayList = None
		self.gcodeDisplayListMade = None
		self.gcodeDisplayListCount = 0
		self.objColor = [[1.0, 0.8, 0.6, 1.0], [0.2, 1.0, 0.1, 1.0], [1.0, 0.2, 0.1, 1.0], [0.1, 0.2, 1.0, 1.0]]
		self.oldX = 0
		self.oldY = 0
		self.dragType = ''
		self.tempRotate = 0
	

	def OnMouseMotion(self,e):
		cursorXY = 100000
		sizeXY = 0
		if self.parent.objectsMaxV != None:
			size = (self.parent.objectsMaxV - self.parent.objectsMinV)
			sizeXY = math.sqrt((size[0] * size[0]) + (size[1] * size[1]))
			
			p0 = numpy.array(gluUnProject(e.GetX(), self.viewport[1] + self.viewport[3] - e.GetY(), 0, self.modelMatrix, self.projMatrix, self.viewport))
			p1 = numpy.array(gluUnProject(e.GetX(), self.viewport[1] + self.viewport[3] - e.GetY(), 1, self.modelMatrix, self.projMatrix, self.viewport))
			cursorZ0 = p0 - (p1 - p0) * (p0[2] / (p1[2] - p0[2]))
			cursorXY = math.sqrt((cursorZ0[0] * cursorZ0[0]) + (cursorZ0[1] * cursorZ0[1]))
			if cursorXY >= sizeXY * 0.7 and cursorXY <= sizeXY * 0.7 + 3 and False:
				self.SetCursor(wx.StockCursor(wx.CURSOR_SIZING))
			else:
				self.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))

		if e.Dragging() and e.LeftIsDown():
			if self.dragType == '':
				#Define the drag type depending on the cursor position.
				if cursorXY >= sizeXY * 0.7 and cursorXY <= sizeXY * 0.7 + 3 and False:
					self.dragType = 'modelRotate'
					self.dragStart = math.atan2(cursorZ0[0], cursorZ0[1])
				else:
					self.dragType = 'viewRotate'
				
			if self.dragType == 'viewRotate':
				if self.view3D:
					self.yaw += e.GetX() - self.oldX
					self.pitch -= e.GetY() - self.oldY
					if self.pitch > 170:
						self.pitch = 170
					if self.pitch < 10:
						self.pitch = 10
				else:
					self.offsetX += float(e.GetX() - self.oldX) * self.zoom / self.GetSize().GetHeight() * 2
					self.offsetY -= float(e.GetY() - self.oldY) * self.zoom / self.GetSize().GetHeight() * 2
			elif self.dragType == 'modelRotate':
				angle = math.atan2(cursorZ0[0], cursorZ0[1])
				diff = self.dragStart - angle
				self.tempRotate = diff * 180 / math.pi
			#Workaround for buggy ATI cards.
			size = self.GetSizeTuple()
			self.SetSize((size[0]+1, size[1]))
			self.SetSize((size[0], size[1]))
			self.Refresh()
		else:
			if self.tempRotate != 0:
				#profile.putProfileSetting('model_rotate_base', profile.getProfileSettingFloat('model_rotate_base') + self.tempRotate)
				self.parent.updateModelTransform()
				self.tempRotate = 0
				
			self.dragType = ''
		if e.Dragging() and e.RightIsDown():
			self.zoom += e.GetY() - self.oldY
			if self.zoom < 1:
				self.zoom = 1
			if self.zoom > 500:
				self.zoom = 500
			self.Refresh()
		self.oldX = e.GetX()
		self.oldY = e.GetY()

		#self.Refresh()
		
	
	def OnMouseWheel(self,e):
		self.zoom *= 1.0 - float(e.GetWheelRotation() / e.GetWheelDelta()) / 10.0
		if self.zoom < 1.0:
			self.zoom = 1.0
		if self.zoom > 500:
			self.zoom = 500
		self.Refresh()
	
	def OnEraseBackground(self,event):
		#Workaround for windows background redraw flicker.
		pass
	
	def OnSize(self,e):
		self.Refresh()

	def OnPaint(self,e):
		dc = wx.PaintDC(self)
		if not hasOpenGLlibs:
			dc.Clear()
			dc.DrawText("No PyOpenGL installation found.\nNo preview window available.", 10, 10)
			return
		self.SetCurrent(self.context)
		opengl.InitGL(self, self.view3D, self.zoom)
		if self.view3D:
			glTranslate(0,0,-self.zoom)
			glRotate(-self.pitch, 1,0,0)
			glRotate(self.yaw, 0,0,1)
			if self.viewMode == "GCode" or self.viewMode == "Mixed":
				if self.parent.gcode != None and len(self.parent.gcode.layerList) > self.parent.layerSpin.GetValue() and len(self.parent.gcode.layerList[self.parent.layerSpin.GetValue()]) > 0:
					glTranslate(0,0,-self.parent.gcode.layerList[self.parent.layerSpin.GetValue()][0].list[-1].z)
			else:
				if self.parent.objectsMaxV != None:
					glTranslate(0,0,-(self.parent.objectsMaxV[2]-self.parent.objectsMinV[2]) * self.GetParent().scale/2)#profile.getProfileSettingFloat('model_scale') / 2)
		else:
			glTranslate(self.offsetX, self.offsetY, 0)

		self.viewport = glGetIntegerv(GL_VIEWPORT);
		self.modelMatrix = glGetDoublev(GL_MODELVIEW_MATRIX);
		self.projMatrix = glGetDoublev(GL_PROJECTION_MATRIX);

		glTranslate(-self.parent.machineCenter.x, -self.parent.machineCenter.y, 0)

		self.OnDraw()
		self.SwapBuffers()

	def OnDraw(self):
		machineSize = self.parent.machineSize

		if self.parent.gcode != None and self.parent.gcodeDirty:
			if self.gcodeDisplayListCount < len(self.parent.gcode.layerList) or self.gcodeDisplayList == None:
				if self.gcodeDisplayList != None:
					glDeleteLists(self.gcodeDisplayList, self.gcodeDisplayListCount)
				self.gcodeDisplayList = glGenLists(len(self.parent.gcode.layerList));
				self.gcodeDisplayListCount = len(self.parent.gcode.layerList)
			self.parent.gcodeDirty = False
			self.gcodeDisplayListMade = 0
		
		if self.parent.gcode != None and self.gcodeDisplayListMade < len(self.parent.gcode.layerList):
			glNewList(self.gcodeDisplayList + self.gcodeDisplayListMade, GL_COMPILE)
			opengl.DrawGCodeLayer(self.parent.gcode.layerList[self.gcodeDisplayListMade])
			glEndList()
			self.gcodeDisplayListMade += 1
			wx.CallAfter(self.Refresh)
		
		glPushMatrix()
		glTranslate(self.parent.machineCenter.x, self.parent.machineCenter.y, 0)
		for obj in self.parent.objectList:
			if obj.mesh == None:
				continue
			if obj.displayList == None:
				obj.displayList = glGenLists(1);
			if obj.dirty:
				obj.dirty = False
				glNewList(obj.displayList, GL_COMPILE)
				opengl.DrawMesh(obj.mesh)
				glEndList()
			
			if self.viewMode == "Mixed":
				glDisable(GL_BLEND)
				glColor3f(0.0,0.0,0.0)
				self.drawModel(obj)
				glColor3f(1.0,1.0,1.0)
				glClear(GL_DEPTH_BUFFER_BIT)
		
		glPopMatrix()
		
		if self.parent.gcode != None and (self.viewMode == "GCode" or self.viewMode == "Mixed"):
			glEnable(GL_COLOR_MATERIAL)
			glEnable(GL_LIGHTING)
			drawUpToLayer = min(self.gcodeDisplayListMade, self.parent.layerSpin.GetValue() + 1)
			starttime = time.time()
			for i in xrange(drawUpToLayer - 1, -1, -1):
				c = 1.0
				if i < self.parent.layerSpin.GetValue():
					c = 0.9 - (drawUpToLayer - i) * 0.1
					if c < 0.4:
						c = (0.4 + c) / 2
					if c < 0.1:
						c = 0.1
				glLightfv(GL_LIGHT0, GL_DIFFUSE, [0,0,0,0])
				glLightfv(GL_LIGHT0, GL_AMBIENT, [c,c,c,c])
				glCallList(self.gcodeDisplayList + i)
				if time.time() - starttime > 0.1:
					break

			glDisable(GL_LIGHTING)
			glDisable(GL_COLOR_MATERIAL)
			glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0]);
			glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0]);

		glColor3f(1.0,1.0,1.0)
		glPushMatrix()
		glTranslate(self.parent.machineCenter.x, self.parent.machineCenter.y, 0)
		for obj in self.parent.objectList:
			if obj.mesh == None:
				continue
			
			if self.viewMode == "Transparent" or self.viewMode == "Mixed":
				glLightfv(GL_LIGHT0, GL_DIFFUSE, map(lambda x: x / 2, self.objColor[self.parent.objectList.index(obj)]))
				glLightfv(GL_LIGHT0, GL_AMBIENT, map(lambda x: x / 10, self.objColor[self.parent.objectList.index(obj)]))
				#If we want transparent, then first render a solid black model to remove the printer size lines.
				if self.viewMode != "Mixed":
					glDisable(GL_BLEND)
					glColor3f(0.0,0.0,0.0)
					self.drawModel(obj)
					glColor3f(1.0,1.0,1.0)
				#After the black model is rendered, render the model again but now with lighting and no depth testing.
				glDisable(GL_DEPTH_TEST)
				glEnable(GL_LIGHTING)
				glEnable(GL_BLEND)
				glBlendFunc(GL_ONE, GL_ONE)
				glEnable(GL_LIGHTING)
				self.drawModel(obj)
				glEnable(GL_DEPTH_TEST)
			elif self.viewMode == "X-Ray":
				glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)
				glDisable(GL_LIGHTING)
				glDisable(GL_DEPTH_TEST)
				glEnable(GL_STENCIL_TEST)
				glStencilFunc(GL_ALWAYS, 1, 1)
				glStencilOp(GL_INCR, GL_INCR, GL_INCR)
				self.drawModel(obj)
				glStencilOp (GL_KEEP, GL_KEEP, GL_KEEP);
				
				glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
				glStencilFunc(GL_EQUAL, 0, 1)
				glColor(1, 1, 1)
				self.drawModel(obj)
				glStencilFunc(GL_EQUAL, 1, 1)
				glColor(1, 0, 0)
				self.drawModel(obj)

				glPushMatrix()
				glLoadIdentity()
				for i in xrange(2, 15, 2):
					glStencilFunc(GL_EQUAL, i, 0xFF);
					glColor(float(i)/10, float(i)/10, float(i)/5)
					glBegin(GL_QUADS)
					glVertex3f(-1000,-1000,-1)
					glVertex3f( 1000,-1000,-1)
					glVertex3f( 1000, 1000,-1)
					glVertex3f(-1000, 1000,-1)
					glEnd()
				for i in xrange(1, 15, 2):
					glStencilFunc(GL_EQUAL, i, 0xFF);
					glColor(float(i)/10, 0, 0)
					glBegin(GL_QUADS)
					glVertex3f(-1000,-1000,-1)
					glVertex3f( 1000,-1000,-1)
					glVertex3f( 1000, 1000,-1)
					glVertex3f(-1000, 1000,-1)
					glEnd()
				glPopMatrix()

				glDisable(GL_STENCIL_TEST)
				glEnable(GL_DEPTH_TEST)
				
				#Fix the depth buffer
				glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)
				self.drawModel(obj)
				glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
			elif self.viewMode == "Normal":
				glLightfv(GL_LIGHT0, GL_DIFFUSE, self.objColor[self.parent.objectList.index(obj)])
				glLightfv(GL_LIGHT0, GL_AMBIENT, map(lambda x: x * 0.4, self.objColor[self.parent.objectList.index(obj)]))
				glEnable(GL_LIGHTING)
				self.drawModel(obj)

			if self.drawBorders and (self.viewMode == "Normal" or self.viewMode == "Transparent" or self.viewMode == "X-Ray"):
				glEnable(GL_DEPTH_TEST)
				glDisable(GL_LIGHTING)
				glColor3f(1,1,1)
				glPushMatrix()
				modelScale = self.GetParent().scale#profile.getProfileSettingFloat('model_scale')
				glScalef(modelScale, modelScale, modelScale)
				opengl.DrawMeshOutline(obj.mesh)
				glPopMatrix()
		
		glPopMatrix()	
		if self.viewMode == "Normal" or self.viewMode == "Transparent" or self.viewMode == "X-Ray":
			glDisable(GL_LIGHTING)
			glDisable(GL_DEPTH_TEST)
			glDisable(GL_BLEND)
			glColor3f(1,0,0)
			glBegin(GL_LINES)
			for err in self.parent.errorList:
				glVertex3f(err[0].x, err[0].y, err[0].z)
				glVertex3f(err[1].x, err[1].y, err[1].z)
			glEnd()
			glEnable(GL_DEPTH_TEST)

		opengl.DrawMachine(machineSize)

		glPushMatrix()
		glTranslate(self.parent.machineCenter.x, self.parent.machineCenter.y, 0)
		
		#Draw the rotate circle
		if self.parent.objectsMaxV != None and False:
			glDisable(GL_LIGHTING)
			glDisable(GL_CULL_FACE)
			glEnable(GL_BLEND)
			glBegin(GL_TRIANGLE_STRIP)
			size = (self.parent.objectsMaxV - self.parent.objectsMinV)
			sizeXY = math.sqrt((size[0] * size[0]) + (size[1] * size[1]))
			for i in xrange(0, 64+1):
				f = i if i < 64/2 else 64 - i
				glColor4ub(255,int(f*255/(64/2)),0,128)
				glVertex3f(sizeXY * 0.7 * math.cos(i/32.0*math.pi), sizeXY * 0.7 * math.sin(i/32.0*math.pi),0.1)
				glColor4ub(  0,128,0,128)
				glVertex3f((sizeXY * 0.7 + 3) * math.cos(i/32.0*math.pi), (sizeXY * 0.7 + 3) * math.sin(i/32.0*math.pi),0.1)
			glEnd()
			glEnable(GL_CULL_FACE)
		
		glPopMatrix()
		
		glFlush()
	
	def drawModel(self, obj):
		multiX = 1 #int(profile.getProfileSetting('model_multiply_x'))
		multiY = 1 #int(profile.getProfileSetting('model_multiply_y'))
		modelScale = self.GetParent().scale #profile.getProfileSettingFloat('model_scale')
		modelSize = (obj.mesh.getMaximum() - obj.mesh.getMinimum()) * modelScale
		glPushMatrix()
		glRotate(self.tempRotate, 0, 0, 1)
		glTranslate(-(modelSize[0]+10)*(multiX-1)/2,-(modelSize[1]+10)*(multiY-1)/2, 0)
		for mx in xrange(0, multiX):
			for my in xrange(0, multiY):
				glPushMatrix()
				glTranslate((modelSize[0]+10)*mx,(modelSize[1]+10)*my, 0)
				glScalef(modelScale, modelScale, modelScale)
				glCallList(obj.displayList)
				glPopMatrix()
		glPopMatrix()

