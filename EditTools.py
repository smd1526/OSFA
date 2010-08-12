import Tkinter
from Tkinter import *
from Constants import *
from PIL import Image, ImageTk

MODE = RED_TOOL
BRUSH_SIZE = 1

# TODO: make tools options class with MODE and BRUSH_SIZE

##################
def setBrushRed():
##################
	global MODE
	MODE = RED_TOOL
	
#####################
def setBrushOrange():
#####################
	global MODE
	MODE = ORANGE_TOOL
	
#####################
def setBrushYellow():
#####################
	global MODE
	MODE = YELLOW_TOOL
	
####################
def setModeSphere():
####################
	global MODE
	MODE = SPHERE_TOOL
	
##################
def setModeCone():
##################
	global MODE
	MODE = CONE_TOOL

######################
def setModeCylinder():
######################
	global MODE
	MODE = CYLINDER_TOOL

###################
def setModeSweep():
###################
	global MODE
	MODE = SWEEP_TOOL

###################
def setModeLabel():
###################
	global MODE
	MODE = LABEL_TOOL
	
###################
def setModeErase():
###################
	global MODE
	MODE = ERASE_TOOL
	
################
def setBrush1():
################
	global BRUSH_SIZE
	BRUSH_SIZE = 1
	
################
def setBrush2():
################
	global BRUSH_SIZE
	BRUSH_SIZE = 2

################
def setBrush3():
################
	global BRUSH_SIZE
	BRUSH_SIZE = 3
	
##############
def getMODE():
##############
	return MODE
	
####################
def getBRUSH_SIZE():
####################
	return BRUSH_SIZE

# TODO: create one method for all color buttons to call
##################
class toolsWindow:
##################
	##########################
	def __init__(self,master):
	##########################
		self.frame = Tkinter.Toplevel(master)
		self.frame.title('Tools')
		self.frame.geometry('300x300+650+0')
		#self.frame.resizable(0,0)
		self.frame.protocol('WM_DELETE_WINDOW',self.quit)
		self.mode = RED_TOOL
		self.brushSize = 1
		self.initButtons()
		self.packButtons()
	######################
	def initButtons(self):
	######################
		self.tier3 = ImageTk.PhotoImage(Image.open("Gallery/Tier3.jpg"))
		self.tier2 = ImageTk.PhotoImage(Image.open("Gallery/Tier2.jpg"))
		self.tier1 = ImageTk.PhotoImage(Image.open("Gallery/Tier1.jpg"))
		self.sphere = ImageTk.PhotoImage(Image.open("Gallery/Sphere.jpg"))
		self.cone = ImageTk.PhotoImage(Image.open("Gallery/Cone.jpg"))
		self.cylinder = ImageTk.PhotoImage(Image.open("Gallery/Cylinder.jpg"))
		self.sweep = ImageTk.PhotoImage(Image.open("Gallery/Sweep.jpg"))
		self.label = ImageTk.PhotoImage(Image.open("Gallery/Label.jpg"))
		self.eraser = ImageTk.PhotoImage(Image.open("Gallery/Eraser.jpg"))
		self.brush1 = ImageTk.PhotoImage(Image.open("Gallery/BSize1.jpg"))
		self.brush2 = ImageTk.PhotoImage(Image.open("Gallery/BSize2.jpg"))
		self.brush3 = ImageTk.PhotoImage(Image.open("Gallery/BSize3.jpg"))
		
		self.redButton = Tkinter.Button(self.frame, image=self.tier3, bg="red", command=setBrushRed)
		self.orangeButton = Tkinter.Button(self.frame, image=self.tier2, bg="orange", command=setBrushOrange)
		self.yellowButton = Tkinter.Button(self.frame, image=self.tier1, bg="yellow", command=setBrushYellow)
		self.sphereButton = Tkinter.Button(self.frame, image=self.sphere, bg="green", command=setModeSphere)
		self.coneButton = Tkinter.Button(self.frame, image=self.cone, bg="blue", command=setModeCone)
		self.cylinderButton = Tkinter.Button(self.frame, image=self.cylinder, bg="purple", command=setModeCylinder)
		self.sweepButton = Tkinter.Button(self.frame, image=self.sweep, command=setModeSweep)
		self.labelButton = Tkinter.Button(self.frame, image=self.label, bg="black", fg="white", command=setModeLabel)
		self.eraseButton = Tkinter.Button(self.frame, image=self.eraser, bg="white", command = setModeErase)
		# TODO: depress brush button that is currently selected
		self.brush1Button = Tkinter.Button(self.frame, image=self.brush1, command=setBrush1)
		self.brush2Button = Tkinter.Button(self.frame, image=self.brush2, command=setBrush2)
		self.brush3Button = Tkinter.Button(self.frame, image=self.brush3, command=setBrush3)
	######################
	def packButtons(self):
	######################
		self.redButton.grid(row=0, column=0)
		self.orangeButton.grid(row=0, column=1)
		self.yellowButton.grid(row=0, column=2)
		self.sphereButton.grid(row=1, column=0)
		self.coneButton.grid(row=1, column=1)
		self.cylinderButton.grid(row=1, column=2)
		self.sweepButton.grid(row=2, column=0)
		self.labelButton.grid(row=2, column=1)
		self.eraseButton.grid(row=2, column=2)
		self.brush1Button.grid(row=3, column=0)
		self.brush2Button.grid(row=3, column=1)
		self.brush3Button.grid(row=3, column=2)
	###############	
	def quit(self):
	###############
		self.frame.destroy()
