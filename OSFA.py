import sys
from Tkinter import *
import tkFileDialog
from tkFileDialog import *
import tkMessageBox
import tkSimpleDialog
from PIL import Image as IM
from Numeric import *
from view3D import *
from EditTools import *
from Constants import *
import os

#################################
#
# Global Variables
#
#################################

# TODO: organize globals; make universals?
# TODO: put all error messages into a separate error log instead of printing to stout

vertices = None #Output File

SHRINK = 10 #Amount to shrink output coordinates
# TODO: make dot size (font size?) configurable
DOT_SIZE = 4 #Diameter of Braille dots

root = Tk() #Main GUI window
yScrollBar = Scrollbar(root) #y-axis scroll bar
xScrollBar = Scrollbar(root, orient=HORIZONTAL) #x-axis scroll bar
splash = ImageTk.PhotoImage(Image.open("Gallery/Splash.jpg")) #Intro splash screen image
splashPanel = Label(root, image=splash) #Intro splash screen

menuBar = Menu(root) #Main menu bar
fileMenu = Menu(menuBar, tearoff=0) #File cascade
optionsMenu = Menu(menuBar, tearoff=0) #Options cascade
doneMenu = Menu(menuBar, tearoff=0) #Done cascade

canv = Canvas(root, width=0, height=0, yscrollcommand=yScrollBar.set, xscrollcommand=xScrollBar.set) #Canvas GUI
toolsWin = toolsWindow(root) #Tools window

fileUnsaved = False #Flag for if the current file is saved/unsaved

shapes = None #ShapeTable (Table to hold all current 3D shapes)
image = None #WorkingImage (Holds info/functions for GUI grid)
prefs = None #Preferences

#################################
#
# Classes
#
#################################

###################
###################
class WorkingImage:
# Holds info and
# functions for
# GUI grid
###################
	##############################
	def __init__(self):
	##############################
		pass
	###############################
	def openImage(self, imageFile):
	# opens a new image from file
	# imageFile = file containing
	#  image to work with
	###############################
		dummyImage = IM.open(imageFile)
		w,h = dummyImage.size
		self.image = IM.new("RGB", (w + prefs.SP_SIZE + (prefs.SP_SIZE - (w % prefs.SP_SIZE)), h + prefs.SP_SIZE + (prefs.SP_SIZE - (h % prefs.SP_SIZE))), RGBS[WHITE])
		self.image.paste(dummyImage, (prefs.SP_SIZE+1,prefs.SP_SIZE+1))
		self.imdata = self.image.load()
		self.width,self.height = self.image.size
		self.shaderize()
		self.collectSprinkleData()
	#########################
	def newImage(self, size):
	# creates a new image
	# using given size
	# size = size of new
	#	image
	#########################
		w,h = size
		self.image = IM.new("RGB", (w + (prefs.SP_SIZE - (w % prefs.SP_SIZE)), h + (prefs.SP_SIZE - (h % prefs.SP_SIZE))), RGBS[WHITE])
		self.imdata = self.image.load()
		self.width,self.height = self.image.size
		self.sprinkleData = zeros([self.width/prefs.SP_SIZE,self.height/prefs.SP_SIZE], Int)
	####################
	def shaderize(self):
	# change image to
	# pixels of red,
	# orange, or yellow
	####################
		for s in range(self.width):
			for t in range(self.height):
				r,g,b = self.imdata[s,t]
				luminance = (float)(11 * r + 16 * g + 5 * b)/32
				if(luminance >=0 and luminance < 64):
					self.imdata[s,t] = RGBS[RED]
				elif(luminance >= 64 and luminance < 127):
					self.imdata[s,t] = RGBS[ORANGE]
				elif(luminance >=127 and luminance < 190):
					self.imdata[s,t] = RGBS[YELLOW]
				else:
					self.imdata[s,t] = RGBS[WHITE]
	##############################
	def collectSprinkleData(self):
	# determines which sprinkles
	# to use and which color;
	# puts data into sprinkle
	# matrix
	##############################
		# TODO: coverage percent as configurable? or a constant?
		coveragePercent = 10
		self.sprinkleData = zeros([self.width/prefs.SP_SIZE,self.height/prefs.SP_SIZE], Int)
		#print "sprinkledata size = (" + str(self.width/prefs.SP_SIZE) + ", " + str(self.height/prefs.SP_SIZE) + ")"
		for i in range(0, len(self.sprinkleData)):
			for j in range(0, len(self.sprinkleData[0])):
				# for each sprinkle:
				redPixels = 0
				orangePixels = 0
				yellowPixels = 0
				for pixI in range(i*prefs.SP_SIZE, i*prefs.SP_SIZE + prefs.SP_SIZE - 1):
					for pixJ in range(j*prefs.SP_SIZE, j*prefs.SP_SIZE + prefs.SP_SIZE - 1):
						# for each pixel
						# TODO: Can we eradicate RGBS?
						if(self.imdata[pixI, pixJ] == RGBS[RED]):
							redPixels = redPixels + 1
						if(self.imdata[pixI, pixJ] == RGBS[ORANGE]):
							orangePixels = orangePixels + 1
						if(self.imdata[pixI, pixJ] == RGBS[YELLOW]):
							yellowPixels = yellowPixels + 1
				coveredPixels = redPixels + orangePixels + yellowPixels
				if((coveredPixels*100)/(prefs.SP_SIZE ** 2) >= coveragePercent):
					if(redPixels >= orangePixels and redPixels >= yellowPixels):
						self.sprinkleData[i][j] = XXRED
					elif(orangePixels >= yellowPixels):
						self.sprinkleData[i][j] = XXORANGE
					else:
						self.sprinkleData[i][j] = XXYELLOW
				else:
					self.sprinkleData[i][j] = XXWHITE
	##########################################
	def updateSprinkleData(self, i, j, color):
	# Helper method to change the color of a
	# sprinkle on the GUI
	##########################################
		maxI,maxJ = self.sprinkleData.shape
		if i >= maxI:
			print "ERROR: index " + str(i) + " is larger than matrix size " + str(maxI)
		elif j >= maxJ:
			print "ERROR: index " + str(j) + " is larger than matrix size " + str(maxJ)
		else:
			self.sprinkleData[i][j] = color
			self.updateGUI(i,j)
	#####################################
	def getSprinkleNeighbors(self, i, j):
	# Determine which of the surrounding
	# sprinkles are to be used
	# i,j = sprinkle coords
	#####################################
		neighbors = " "
		sprinkleLevel = self.sprinkleData[i][j]
		# Position 1
		if(sprinkleLevel <= self.sprinkleData[i][j-1]):
			neighbors = neighbors + "0"
		else:
			neighbors = neighbors + "1"
		# Position 2
		if(sprinkleLevel <= self.sprinkleData[i+1][j]):
			neighbors = neighbors + "0"
		else:
			neighbors = neighbors + "2"
		# Position 3
		if(sprinkleLevel <= self.sprinkleData[i][j+1]):
			neighbors = neighbors + "0"
		else:
			neighbors = neighbors + "3"
		# Position 4
		if(sprinkleLevel <= self.sprinkleData[i-1][j]):
			neighbors = neighbors + "0"
		else:
			neighbors = neighbors + "4"
		return neighbors
	######################
	def buildCanvas(self):
	######################
		# TODO: is this the best place to change root geometry?
		root.geometry("%dx%d+0+0" % (int(canv.cget("width"))+130, int(canv.cget("height"))+130))
		for i in range(0, len(self.sprinkleData)):
			for j in range(0, len(self.sprinkleData[0])):
				color = self.sprinkleData[int(i)][int(j)]
				# TODO: change to config if !showGrid
				if prefs.showGrid:
					if color == XXRED:
						obj = canv.create_rectangle(i*prefs.SP_SIZE, j*prefs.SP_SIZE, i*prefs.SP_SIZE+prefs.SP_SIZE, j*prefs.SP_SIZE+prefs.SP_SIZE, fill=RED, outline=BLACK)
					elif color == XXORANGE:
						obj = canv.create_rectangle(i*prefs.SP_SIZE, j*prefs.SP_SIZE, i*prefs.SP_SIZE+prefs.SP_SIZE, j*prefs.SP_SIZE+prefs.SP_SIZE, fill=ORANGE, outline=BLACK)
					elif color == XXYELLOW:
						obj = canv.create_rectangle(i*prefs.SP_SIZE, j*prefs.SP_SIZE, i*prefs.SP_SIZE+prefs.SP_SIZE, j*prefs.SP_SIZE+prefs.SP_SIZE, fill=YELLOW, outline=BLACK)
					elif color == XXWHITE:
						obj = canv.create_rectangle(i*prefs.SP_SIZE, j*prefs.SP_SIZE, i*prefs.SP_SIZE+prefs.SP_SIZE, j*prefs.SP_SIZE+prefs.SP_SIZE, fill=WHITE, outline=BLACK)
					elif color == XXBLACK:
						obj = canv.create_rectangle(i*prefs.SP_SIZE, j*prefs.SP_SIZE, i*prefs.SP_SIZE+prefs.SP_SIZE, j*prefs.SP_SIZE+prefs.SP_SIZE, fill=BLACK, outline=BLACK)
				else:
					if color == XXRED:
						obj = canv.create_rectangle(i*prefs.SP_SIZE, j*prefs.SP_SIZE, i*prefs.SP_SIZE+prefs.SP_SIZE, j*prefs.SP_SIZE+prefs.SP_SIZE, fill=RED, outline=RED)
					elif color == XXORANGE:
						obj = canv.create_rectangle(i*prefs.SP_SIZE, j*prefs.SP_SIZE, i*prefs.SP_SIZE+prefs.SP_SIZE, j*prefs.SP_SIZE+prefs.SP_SIZE, fill=ORANGE, outline=ORANGE)
					elif color == XXYELLOW:
						obj = canv.create_rectangle(i*prefs.SP_SIZE, j*prefs.SP_SIZE, i*prefs.SP_SIZE+prefs.SP_SIZE, j*prefs.SP_SIZE+prefs.SP_SIZE, fill=YELLOW, outline=YELLOW)
					elif color == XXWHITE:
						obj = canv.create_rectangle(i*prefs.SP_SIZE, j*prefs.SP_SIZE, i*prefs.SP_SIZE+prefs.SP_SIZE, j*prefs.SP_SIZE+prefs.SP_SIZE, fill=WHITE, outline=WHITE)
					elif color == XXBLACK:
						obj = canv.create_rectangle(i*prefs.SP_SIZE, j*prefs.SP_SIZE, i*prefs.SP_SIZE+prefs.SP_SIZE, j*prefs.SP_SIZE+prefs.SP_SIZE, fill=BLACK, outline=BLACK)
				canv.tag_bind(obj, "<Button-1>", onMouse1Click)
				canv.tag_bind(obj, "<B1-Motion>", onMouseDrag)
				canv.tag_bind(obj, "<ButtonRelease-1>", onMouseRelease)
		canv.configure(width=int(canv.cget("width"))+1, height=int(canv.cget("height"))+1)
		canv.config(scrollregion=(0, 0, int(canv.cget("width")), int(canv.cget("height"))))
	###############################
	def renderSprinkleOutput(self):
	###############################
		for i in range(0, len(self.sprinkleData)-1):
			for j in range(0, len(self.sprinkleData[0])-1):
				if(self.sprinkleData[i][j]):
					if self.sprinkleData[i][j] == XXBLACK:
						self.sprinkleData[i][j] = XXWHITE
					vertices.write(str(float(i*prefs.SP_SIZE)/SHRINK) + " " + str((self.height-float(j*prefs.SP_SIZE))/SHRINK) + " " + str(self.sprinkleData[i][j]) + self.getSprinkleNeighbors(i,j) + "\n")
	############################
	def updateGUI(self, i, j):
	############################
		# TODO: Does fill=color work?
		maxI,maxJ = self.sprinkleData.shape
		if i > maxI:
			print "ERROR: index " + str(i) + " is larger than matrix size " + str(maxI)
		elif j > maxJ:
			print "ERROR: index " + str(j) + " is larger than matrix size " + str(maxJ)
		else:
			color = self.sprinkleData[int(i)][int(j)]
			obj = canv.find_enclosed(i*prefs.SP_SIZE-prefs.SP_SIZE, j*prefs.SP_SIZE-prefs.SP_SIZE, i*prefs.SP_SIZE+prefs.SP_SIZE+1, j*prefs.SP_SIZE+prefs.SP_SIZE+1)
			if(canv.itemcget(obj, "fill") == BLUE) or (canv.itemcget(obj, "fill") == GREEN) or (canv.itemcget(obj, "fill") == BLACK):
				pass
			else:
				if prefs.showGrid:
					if color == XXRED:
						canv.itemconfig(obj,fill=RED,outline=BLACK)
					elif color == XXORANGE:
						canv.itemconfig(obj,fill=ORANGE,outline=BLACK)
					elif color == XXYELLOW:
						canv.itemconfig(obj,fill=YELLOW,outline=BLACK)
					elif color == XXWHITE:
						canv.itemconfig(obj,fill=WHITE,outline=BLACK)
					elif color == XXBLACK:
						canv.itemconfig(obj,fill=BLACK,outline=BLACK)
				else:
					if color == XXRED:
						canv.itemconfig(obj,fill=RED,outline=RED)
					elif color == XXORANGE:
						canv.itemconfig(obj,fill=ORANGE,outline=ORANGE)
					elif color == XXYELLOW:
						canv.itemconfig(obj,fill=YELLOW,outline=YELLOW)
					elif color == XXWHITE:
						canv.itemconfig(obj,fill=WHITE,outline=WHITE)
					elif color == XXBLACK:
						canv.itemconfig(obj,fill=BLACK,outline=BLACK)

###################
###################
class CreatedShape:
###################
	##########################
	def __init__(self, s):
	##########################
	# TODO: give 3D shapes a height, default is 3, set to level of tier supporting it
		self.shape = s
		if(self.shape == SPHERE or self.shape == CONE or self.shape == CYLINDER):
			self.calcCenterAndRadius()
			if(int(self.centerX+self.radius) > int(canv.cget("width"))) or (int(self.centerX-self.radius) < 0):
				print "Shape out of bounds (X)"
				tkMessageBox.showerror("Out of bounds", "The shape is too wide.")
			elif(int(self.centerY+self.radius) > int(canv.cget("height"))) or (int(self.centerY-self.radius) < 0):
				print "Shape out of bounds (Y)"
				tkMessageBox.showerror("Out of bounds", "The shape is too tall.")
			else:
				self.updateCanv()
				shapes.addEntry(self.objID, self.shape, self.centerX, self.centerY, self.radius)
		if(self.shape == LABEL):
			self.updateCanv()
	##############################
	def calcCenterAndRadius(self):
	##############################
		farRight = 0
		farLeft = canv.cget("width")
		highest = canv.cget("height")
		lowest = 0
		total = 0
		for obj in canv.find_withtag(SELECTED):
			x1cor, y1cor, x2cor, y2cor = canv.coords(obj)
			if(x2cor > farRight):
				farRight = x2cor
			if(x1cor < farLeft):
				farLeft = x1cor
			if(y2cor > lowest):
				lowest = y2cor
			if(y1cor < highest):
				highest = y1cor
			image.updateGUI(int(x1cor/prefs.SP_SIZE),int(y1cor/prefs.SP_SIZE))
			canv.dtag(obj, SELECTED)
		self.centerX = (farLeft + farRight)/2
		self.centerY = (highest + lowest)/2
		self.radius = max((farRight - self.centerX), (lowest - self.centerY))
	#######################################
	def calcBrailleDots(self, objID, brailleText):
	#######################################
		tag = "Ltag" + str(objID)
		self.radius = (DOT_SIZE/2)*prefs.SP_SIZE
		addon = ((2*DOT_SIZE)+3)*prefs.SP_SIZE
		count = 0
		for letter in brailleText:
			for dot in BRAILLE[letter]:
				if dot == 1:
					self.centerX = self.i+self.radius+(count*addon)
					self.centerY = self.j+self.radius
				elif dot == 2:
					self.centerX = self.i+self.radius+(count*addon)
					self.centerY = self.j+(3*self.radius)+prefs.SP_SIZE
				elif dot == 3:
					self.centerX = self.i+self.radius+(count*addon)
					self.centerY = self.j+(5*self.radius)+(2*prefs.SP_SIZE)
				elif dot == 4:
					self.centerX = self.i+(3*self.radius)+prefs.SP_SIZE+(count*addon)
					self.centerY = self.j+self.radius
				elif dot == 5:
					self.centerX = self.i+(3*self.radius)+prefs.SP_SIZE+(count*addon)
					self.centerY = self.j+(3*self.radius)+prefs.SP_SIZE
				elif dot == 6:
					self.centerX = self.i+(3*self.radius)+prefs.SP_SIZE+(count*addon)
					self.centerY = self.j+(5*self.radius)+(2*prefs.SP_SIZE)
				shapes.addEntry(tag, SPHERE, self.centerX, self.centerY, self.radius)
			count = count + 1
	#####################
	def updateCanv(self):
	#####################
		if self.shape == LABEL:
			brailleText = tkSimpleDialog.askstring("Insert Label", "Enter label text");
			# TODO: make sure dots will be big enough
			brailleText = brailleText.upper()
			letters = len(brailleText)
			self.i,self.j,k,l = canv.coords(canv.find_withtag(SELECTED)[0])
			
			letterWidth = (2*DOT_SIZE + 1)*prefs.SP_SIZE
			addon = (2*(letters-1))*prefs.SP_SIZE
			labelHeight = (3*DOT_SIZE + 2)*prefs.SP_SIZE
			labelWidth = (letterWidth)*letters + addon
			if(self.i+labelWidth > image.width):
				print "Label out of bounds (X): " + str(self.i+labelWidth) + " exceeds " + str(image.width)
				tkMessageBox.showerror("Out of bounds", "The label is too wide.")
			elif(self.j+labelHeight > image.height):
				print "Label out of bounds (Y): " + str(self.j+labelWidth) + " exceeds " + str(image.width)
				tkMessageBox.showerror("Out of bounds", "The label is too tall.")
			else:
				# TODO: put brailleText on rectangle
				obj = canv.create_rectangle(self.i,self.j,self.i+labelWidth,self.j+labelHeight,fill=BLACK)
				canv.tag_bind(obj, "<Button-1>", onMouse1Click)
				canv.tkraise(obj)
				self.calcBrailleDots(obj, brailleText)
		elif self.shape == SPHERE:
			self.objID = canv.create_oval(self.centerX-self.radius,self.centerY-self.radius,self.centerX+self.radius,self.centerY+self.radius,fill=GREEN)
			canv.tag_bind(self.objID, "<Button-1>", onMouse1Click)
			canv.tkraise(self.objID)
		elif self.shape == CONE:
			self.objID = canv.create_oval(self.centerX-self.radius,self.centerY-self.radius,self.centerX+self.radius,self.centerY+self.radius,fill=BLUE)
			canv.tag_bind(self.objID, "<Button-1>", onMouse1Click)
			canv.tkraise(self.objID)
		elif self.shape == CYLINDER:
			self.objID = canv.create_oval(self.centerX-self.radius,self.centerY-self.radius,self.centerX+self.radius,self.centerY+self.radius,fill=PURPLE)
			canv.tag_bind(self.objID, "<Button-1>", onMouse1Click)
			canv.tkraise(self.objID)

#################
#################
class ShapeTable:
#################
	###################
	def __init__(self):
	###################
		self.objIDs = list()
		self.shapes = list()
		self.centerXs = list()
		self.centerYs = list()
		self.heights = list()
		self.radii = list()
		self.numEntries = 0
	###################################################################
	def addEntry(self, objID, shape, centerX, centerY, radius):
	###################################################################
		if(str(objID)[0] == "L"):
			print "addEntry object is tagged"
		self.objIDs.append(objID)
		self.shapes.append(shape)
		self.centerXs.append(centerX)
		self.centerYs.append(centerY)
		self.radii.append(radius)
		self.numEntries = self.numEntries + 1
	##########################
	def delEntry(self, objID):
	##########################
		print "Deleting " + str(objID[0])
		entry = self.findEntry(objID)
		if entry < 0:
			# TODO: handle objID not found
			print "objID " + str(objID) + " not found"
		else:
			del self.objIDs[entry]
			del self.shapes[entry]
			del self.centerXs[entry]
			del self.centerYs[entry]
			del self.radii[entry]
			self.numEntries = self.numEntries - 1
	############################
	def delLabelDots(self, tag):
	############################
		print "Deleting tag " + str(tag)
		i = 0
		while (i < self.numEntries) and (self.objIDs[i] == tag):
			print "Deleting entry" 
			del self.objIDs[i]
			del self.shapes[i]
			del self.centerXs[i]
			del self.centerYs[i]
			del self.radii[i]
			self.numEntries = self.numEntries - 1
	###########################
	def findEntry(self, objID):
	###########################
		for i in range(0, self.numEntries):
			if(self.objIDs[i] == objID[0]):
				return i
		return -1
	################
	def clear(self):
	################
		for i in range(0, self.numEntries):
			del self.objIDs[0]
			del self.shapes[0]
			del self.centerXs[0]
			del self.centerYs[0]
			del self.radii[0]
		self.numEntries = 0
	##############################
	def render3DShapeOutput(self):
	##############################
		for i in range(0, self.numEntries):
			vertices.write(self.shapes[i] + " " + str((float(self.centerXs[i]/SHRINK))) + " " + str((float(canv.cget("height"))-float(self.centerYs[i]))/SHRINK) + " " + str((float(self.radii[i]/SHRINK))) + "\n")

##################
##################
class Preferences:
##################
	###################
	def __init__(self):
	###################
		self.showGridVar = BooleanVar()
		self.showGridVar.set(True)
		self.showGrid = self.showGridVar.get()
		self.SP_SIZE = 10
		self.outline = BLACK
	############################
	def openPrefs(self, master):
	############################
		self.frame = Tkinter.Toplevel(master)
		self.frame.title('Preferences')
		self.frame.geometry('200x100+100+100')
		self.frame.resizable(0,0)
		self.frame.protocol('WM_DELETE_WINDOW',self.okClicked)
		Label(self.frame, text="Sprinkle size:").grid(row=0)
		self.entry = Entry(self.frame)
		self.entry.insert(0, str(self.SP_SIZE))
		self.entry.grid(row=0, column=1)
		cb = Checkbutton(self.frame, text="Show grid", onvalue=True, offvalue=False, variable=self.showGridVar)
		cb.grid(row=2, columnspan=2, sticky=W)
		button = Button(self.frame, text="OK", command=self.okClicked)
		button.grid(row=3, columnspan=2)
	####################
	def okClicked(self):
	####################
		self.SP_SIZE = int(self.entry.get())
		self.showGrid = self.showGridVar.get()
		toggleGrid()
		self.frame.destroy()

#################
class SizeWindow:
#################
	###########################
	def __init__(self, master):
	###########################
		# TODO: allow user to select units
		self.x = 0
		self.y = 0
		self.ok = False
		self.frame = Tkinter.Toplevel(master)
		self.frame.title('Size')
		self.frame.geometry('200x100+100+100')
		self.frame.resizable(0,0)
		self.frame.protocol('WM_DELETE_WINDOW', self.frame.destroy)
		Label(self.frame, text="Enter new image size in pixels").grid(row=0, columnspan=2)
		Label(self.frame, text="X:").grid(row=1)
		self.xEntry = Entry(self.frame)
		self.xEntry.insert(0, str(self.x))
		self.xEntry.grid(row=1, column=1)
		Label(self.frame, text="Y:").grid(row=2)
		self.yEntry = Entry(self.frame)
		self.yEntry.insert(0, str(self.y))
		self.yEntry.grid(row=2, column=1)
		okButton = Button(self.frame, text="OK", command=self.okClicked)
		okButton.grid(row=3)
		cancelButton = Button(self.frame, text="Cancel", command=self.frame.destroy)
		cancelButton.grid(row=3, column=1)
	####################
	def okClicked(self):
	####################
		self.x = int(self.xEntry.get())
		self.y = int(self.yEntry.get())
		self.ok = True
		self.frame.destroy()

#####################################
#
# Helper Functions
#
#####################################

######################
def toggleGrid(*args):
######################
	if prefs.showGrid:
		for obj in canv.find_all():
			canv.itemconfig(obj, outline=BLACK)
	else:
		for obj in canv.find_all():
			canv.itemconfig(obj, outline=canv.itemcget(obj, "fill"))

#########################
def onMouse1Click(event):
#########################
	global fileUnsaved
	fileUnsaved = True
	obj = event.widget.find_closest(canv.canvasx(event.x), canv.canvasy(event.y))
	c1,c2,c3,c4 = canv.coords(obj)
	i = int(c1/prefs.SP_SIZE)
	j = int(c2/prefs.SP_SIZE)
	if(canv.itemcget(obj, "fill") == BLUE) or (canv.itemcget(obj, "fill") == GREEN) or (canv.itemcget(obj, "fill") == PURPLE) or (canv.itemcget(obj, "fill") == BLACK):
		if(getMODE() == ERASE_TOOL):
			if(canv.itemcget(obj, "fill") == BLACK):
				shapes.delLabelDots("Ltag" + str(obj[0]))
			else:
				shapes.delEntry(obj)
			canv.delete(obj)
	else:
		if(getMODE() == RED_TOOL):
			paint(i,j,XXRED)
		elif(getMODE() == ORANGE_TOOL):
			paint(i,j,XXORANGE)
		elif(getMODE() == YELLOW_TOOL):
			paint(i,j,XXYELLOW)
		elif(getMODE() == SPHERE_TOOL) or (getMODE() == CONE_TOOL) or (getMODE() == CYLINDER_TOOL):
			# TODO: handle if over other shape
			canv.itemconfigure(obj, fill=DGRAY)
			canv.addtag_withtag(SELECTED, obj)
		elif(getMODE() == SWEEP_TOOL):
			if tkMessageBox.askyesno("Sweep", "Are you sure you want to clear all?"):
				canv.delete('all')
			else:
				pass
		elif(getMODE() == LABEL_TOOL):
			# TODO: handle if over other shape
			canv.addtag_withtag(SELECTED, obj)
			newLabel = CreatedShape(LABEL)
			canv.dtag(obj, SELECTED)
		elif(getMODE() == ERASE_TOOL):
			paint(i,j,XXWHITE)

#######################
def onMouseDrag(event):
#######################
	global fileUnsaved
	fileUnsaved = True
	obj = event.widget.find_closest(canv.canvasx(event.x), canv.canvasy(event.y))
	c1,c2,c3,c4 = canv.coords(obj)
	i = int(c1/prefs.SP_SIZE)
	j = int(c2/prefs.SP_SIZE)
	if(canv.itemcget(obj, "fill") == BLUE) or (canv.itemcget(obj, "fill") == GREEN) or (canv.itemcget(obj, "fill") == PURPLE) or (canv.itemcget(obj, "fill") == BLACK):
		pass
	else:
		if(getMODE() == RED_TOOL):
			paint(i,j,XXRED)
		elif(getMODE() == ORANGE_TOOL):
			paint(i,j,XXORANGE)
		elif(getMODE() == YELLOW_TOOL):
			paint(i,j,XXYELLOW)
		elif(getMODE() == SPHERE_TOOL) or (getMODE() == CONE_TOOL) or (getMODE() == CYLINDER_TOOL):
			# TODO: handle if over other shape
			canv.itemconfigure(obj, fill=DGRAY)
			canv.addtag_withtag(SELECTED, obj)
		elif(getMODE() == ERASE_TOOL):
			paint(i,j,XXWHITE)
			
##########################
def onMouseRelease(event):
##########################
	global fileUnsaved
	fileUnsaved = True
	obj = event.widget.find_closest(event.x, event.y)
	if(getMODE() == SPHERE_TOOL):
		newSphere = CreatedShape(SPHERE)
	if(getMODE() == CONE_TOOL):
		newCone = CreatedShape(CONE)
	if(getMODE() == CYLINDER_TOOL):
		newCylinder = CreatedShape(CYLINDER)
			
#####################
def paint(i,j,color):
#####################
	if(getBRUSH_SIZE >= 1):
		image.updateSprinkleData(i,j,color)
	if (getBRUSH_SIZE() >= 2):
		image.updateSprinkleData(i+1,j,color)
		image.updateSprinkleData(i,j+1,color)
		image.updateSprinkleData(i+1,j+1,color)
	if (getBRUSH_SIZE() >= 3):
		image.updateSprinkleData(i-1,j-1,color)
		image.updateSprinkleData(i,j-1,color)
		image.updateSprinkleData(i+1,j-1,color)
		image.updateSprinkleData(i-1,j,color)
		image.updateSprinkleData(i-1,j+1,color)

#########################
def getObjectCoords(obj):
#########################
	i,j,k,l = canv.coords(obj)
	result = list()
	result.append(i)
	result.append(j)
	return result

############################################
#
# Button Listeners
#
############################################

##############
def newFile():
##############
	# TODO: can user import vertices file?
	global image
	global canv
	global fileUnsaved
	
	if fileUnsaved:
		result = tkMessageBox._show("File Unsaved", "Save before closing?", tkMessageBox.QUESTION, tkMessageBox.YESNOCANCEL)
	else:
		result = None
		
	if str(result) == tkMessageBox.CANCEL:
		pass
	else:
		if str(result) == tkMessageBox.YES:
			saveButtonClicked()
		imageSize = SizeWindow(root)
		root.wait_window(imageSize.frame)
		if imageSize.ok:
			fileUnsaved = True
			size = (imageSize.x, imageSize.y)
			image = WorkingImage()
			image.newImage(size)
			splashPanel.destroy()
			canv.delete('all')
			canv.configure(width=image.width, height=image.height)
			image.buildCanvas()
			canv.pack(pady=50)

#################
def filePicker():
#################
	global canv
	global image
	global fileUnsaved

	if fileUnsaved:
		result = tkMessageBox._show("File Unsaved", "Save before closing?", tkMessageBox.QUESTION, tkMessageBox.YESNOCANCEL)
	else:
		result = None
		
	if str(result) == tkMessageBox.CANCEL:
			pass
	else:
		if str(result) == tkMessageBox.YES:
			saveButtonClicked()
		imageFile = tkFileDialog.askopenfilename()
		if(str(imageFile) == "()"):
				pass
		else:
			image = WorkingImage()
			image.openImage(imageFile)
			fileUnsaved = True
			splashPanel.destroy()
			canv.delete('all')
			canv.configure(width=image.width, height=image.height)
			image.buildCanvas()
			canv.pack(pady=50)

########################
def saveButtonClicked():
########################
	# TODO: rename vertices to something more relevant, change file destination
	global vertices
	global fileUnsaved
	#vertices = open(VERTICES, 'w')
	vertices = asksaveasfile(mode='w')
	if vertices == None:
		pass
	else:
		print "Saving to: " + vertices.name
		vertices.write(str(float(prefs.SP_SIZE)/SHRINK) + "\n")
		image.renderSprinkleOutput()
		shapes.render3DShapeOutput()
		vertices.close()
		fileUnsaved = False
	
##################	
def preferences():
##################
	prefs.openPrefs(root)
		
###################
def startBlender():
###################
	if fileUnsaved: # File not saved
		result = tkMessageBox._show("File Unsaved", "The file is unsaved. It must be saved before opening Blender. Save now?", tkMessageBox.QUESTION, tkMessageBox.YESNOCANCEL)
	else: 
		result = None
	if (str(result) == tkMessageBox.CANCEL) or (str(result) == tkMessageBox.NO):
		pass
	else:
		if str(result) == tkMessageBox.YES:
			saveButtonClicked()
		root.quit()
		os.system(BLENDER_SCRIPT + ' ' + vertices.name)
	
#################
def closeImage():
#################
	global fileUnsaved
	if fileUnsaved: # File not saved
		result = tkMessageBox._show("File Unsaved", "Save before closing?", tkMessageBox.QUESTION, tkMessageBox.YESNOCANCEL)
	else:
		result = None
	if str(result) == tkMessageBox.CANCEL:
		pass
	else:
		if str(result) == tkMessageBox.YES:
			saveButtonClicked()
		canv.delete('all')
		canv.configure(width=0,height=0)
		canv.pack(pady=0)
		root.geometry("600x600+0+0")
		splashPanel = Label(root, image=splash)
		splashPanel.pack(side='top', fill='both', expand='yes')
		shapes.clear()
		fileUnsaved = False
	
###############
def exitOSFA():
###############
	if fileUnsaved: # File not saved
		result = tkMessageBox._show("File Unsaved", "Save before closing?", tkMessageBox.QUESTION, tkMessageBox.YESNOCANCEL)
	else:
		result = None
	if str(result) == tkMessageBox.CANCEL:
		pass
	else:
		if str(result) == tkMessageBox.YES:
			saveButtonClicked()
		root.quit()

#######################################
#
# main
#
#######################################

###########
def main():
###########
	global shapes
	global prefs
	shapes = ShapeTable()
	prefs = Preferences()
	
	# TODO: zooming
	root.geometry("600x600+0+0")
	root.title("Operation: Stick Figure Army")
	splashPanel.pack(side='top', fill='both', expand='yes')
	yScrollBar.pack(side=RIGHT, fill=Y)
	yScrollBar.config(command=canv.yview)
	xScrollBar.pack(side=BOTTOM, fill=X)
	xScrollBar.config(command=canv.xview)
	#root.delete(splashPanel)
	
	fileMenu.add_command(label="Let There Be Sprinkles", command=newFile)
	fileMenu.add_command(label="Choose your destiny", command=filePicker)
	fileMenu.add_command(label="Save", command=saveButtonClicked)
	menuBar.add_cascade(label="File", menu=fileMenu)

	optionsMenu.add_command(label="Preferences", command=preferences)
	menuBar.add_cascade(label="Options", menu=optionsMenu)
	
	doneMenu.add_command(label="to Blender", command=startBlender)
	doneMenu.add_command(label="Close Image", command=closeImage)
	doneMenu.add_command(label="Exit", command=exitOSFA)
	menuBar.add_cascade(label="Done!", menu=doneMenu)
	
	#mainWin = mainWindowClass(root)
	#mainWin.canvas.create_text(10,10,anchor='nw',font=('Helvetica',10),text=mainWin.getFile())
	
	root.config(menu=menuBar)
	root.mainloop()

# Start:
main()
