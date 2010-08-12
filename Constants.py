################
# STRINGS
################

import os
# TODO: get general location of blender?
BLENDER_SCRIPT = '/usr/bin/blender -P ' + str(os.getcwd()) + '/ThreeDation.py'
# TODO: user can specify saved file name
BLENDER_OUT = os.environ['HOME'] + '/Desktop/blender_out.stl'

################
# TAGS
################

SELECTED = "selected"

################
# DICTIONARIES
################

BRAILLE = {'A':[1], 'B':[1,2], 'C':[1,4], 'D':[1,4,5],
		   'E':[1,5], 'F':[1,2,4], 'G':[1,2,4,5], 'H':[1,2,5],
		   'I':[2,4], 'J':[2,4,5], 'K':[1,3], 'L':[1,2,3],
		   'M':[1,3,4], 'N':[1,3,4,5], 'O':[1,3,5], 'P':[1,2,3,4],
		   'Q':[1,2,3,4,5], 'R':[1,2,3,5], 'S':[2,3,4], 'T':[2,3,4,5],
		   'U':[1,3,6], 'V':[1,2,3,6], 'W':[2,4,5,6], 'X':[1,3,4,6],
		   'Y':[1,3,4,5,6], 'Z':[1,3,5,6]}

RGBS = {'white':(255,255,255), 'lgray':(170,170,170), 'dgray':(85,85,85), 'black':(0,0,0),
			 'red':(255,0,0), 'dark orange':(255,100,0), 'yellow':(255,255,0)}

################
# COLORS
################

RED = "red"
ORANGE = "dark orange"
YELLOW = "yellow"
BLUE = "blue"
GREEN = "green"
PURPLE = "purple"
WHITE = "white"
LGRAY = "gray20"
DGRAY = "gray70"
BLACK = "black"

XXRED = 3
XXORANGE = 2
XXYELLOW = 1
XXWHITE = 0
XXBLACK = 4

################
# SHAPES
################

SPHERE = "sphere"
CONE = "cone"
CYLINDER = "cylinder"
LABEL = "label"

################
# MODES
################

RED_TOOL = 0
ORANGE_TOOL = 1
YELLOW_TOOL = 2
SPHERE_TOOL = 3
CONE_TOOL = 4
CYLINDER_TOOL = 5
SWEEP_TOOL = 6
LABEL_TOOL = 7
ERASE_TOOL = 8
