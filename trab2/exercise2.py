#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) 2009 - Gustavo Serra Scalet <gsscalet@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__AUTHOR__ = "Gustavo Serra Scalet <gsscalet@gmail.com>"
__VERSION__ = 0.1

MIN_ARGS = 1

# Based on the 5th tutorial of Richard Cambell, with the python port of John Ferguson and Tony Colston
# http://nehe.gamedev.net/data/lessons/lesson.asp?lesson=05

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from obj import Obj
import sys

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'
SPACE = '\040'
BIGGER = '+'
SMALLER = '-'
ROT_X_PLUS = 'R'
ROT_X_MINUS = 'r'
ROT_Y_PLUS = 'Y'
ROT_Y_MINUS = 'y'
ROT_Z_PLUS = 'P'
ROT_Z_MINUS = 'p'


# Number of the glut window.
window = 0

# Properties
scales = 0.5
positions = [0, 0, 0]  # moving to the right
rotations = [0, 0, 0]
background_color = (0.9, 0.8, 0.7, 0.0)

# The object
obj = None
# views availables
from views_definition import *
views = [
		ESTRUTURA_DE_ARAME,
		SOMBREAMENTO_PLANO,
		ESTRUTURA_DE_ARAME_E_POLIGONOS,
		SOMBREAMENTO_SUAVE,
		SILHUETA,
		SILHUETA_E_SOMBREAMENTO,
	]
current_view = views[0]

# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):				# We call this right after our OpenGL window is created.
	glClearColor(*background_color)	# This Will Clear The Background Color To Orange
	glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
	glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
	glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
	glEnable(GL_NORMALIZE)				# Avoid wrong scale behaviour
	glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading
	
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()					# Reset The Projection Matrix
										# Calculate The Aspect Ratio Of The Window
	ratio = float(Width)/float(Height)
	gluPerspective(45.0, ratio, 0.1, 100.0)

	glMatrixMode(GL_MODELVIEW)

# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
	if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small 
		Height = 1

	glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	ratio = float(Width)/float(Height)
	gluPerspective(45.0, ratio, 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)

# The main drawing function. 
def DrawGLScene():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)	# Clear The Screen And The Depth Buffer
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()  # Reset The View
	glScale(scales, scales, scales)
	glTranslate(*positions)  # Move
	glRotate(rotations[0], 1.0,0.0,0.0)  # Rotate On It's X Axis
	glRotate(rotations[1], 0.0,1.0,0.0)  # Rotate On It's Y Axis
	glRotate(rotations[2], 0.0,0.0,1.0)  # Rotate On It's Z Axis
	# loads our object
	obj.show(current_view, background_color)
	# since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)  
def keyPressed(*args):
	# If escape is pressed, kill everything.
	global scales, current_view
	if args[0] == ESCAPE:
		glutDestroyWindow(window)
		sys.exit()
	elif args[0] == SPACE:
		# cicle through views
		current_view = (views.index(current_view) + 1) % len(views)
		print " Switching view to: %s" % views_name[current_view]
	elif args[0] == BIGGER:
		scales += .1
	elif args[0] == SMALLER:
		if scales >= 0.4:
			scales -= .1
	elif args[0] == ROT_X_PLUS:
		rotations[0] += 20
	elif args[0] == ROT_X_MINUS:
		rotations[0] -= 20
	elif args[0] == ROT_Y_PLUS:
		rotations[1] += 20
	elif args[0] == ROT_Y_MINUS:
		rotations[1] -= 20
	elif args[0] == ROT_Z_PLUS:
		rotations[2] += 20
	elif args[0] == ROT_Z_MINUS:
		rotations[2] -= 20
	elif args[0] == GLUT_KEY_UP:
		positions[1] += .1
	elif args[0] == GLUT_KEY_RIGHT:
		positions[0] += .1
	elif args[0] == GLUT_KEY_DOWN:
		positions[1] -= .1
	elif args[0] == GLUT_KEY_LEFT:
		positions[0] -= .1

def mouseMoved(x,y):
	# Unfortunatelly I wasn't able to implement this feature :'(
	pass

def main(filename):
	"""Exercise #2 of mc930. Loading a obj file"""
	global window, obj

	glutInit(sys.argv)

	# Select type of Display mode:   
	#  Double buffer 
	#  RGBA color
	# Alpha components supported 
	# Depth buffer
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
	
	# get a 640 x 480 window 
	glutInitWindowSize(640, 480)
	
	# the window starts at the upper left corner of the screen 
	glutInitWindowPosition(0, 0)
	
	# Okay, like the C version we retain the window id to use when closing, but for those of you new
	# to Python (like myself), remember this assignment would make the variable local and not global
	# if it weren't for the global declaration at the start of main.
	window = glutCreateWindow("MC930 2nd Exercise - Gustavo Serra Scalet")

	# Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
	# set the function pointer and invoke a function to actually register the callback, otherwise it
	# would be very much like the C version of the code.	
	glutDisplayFunc(DrawGLScene)
	#glutDisplayFunc()
	
	# Uncomment this line to get full screen.
	# glutFullScreen()

	# When we are doing nothing, redraw the scene.
	glutIdleFunc(DrawGLScene)
		
	# Register the function called when our window is resized.
	glutReshapeFunc(ReSizeGLScene)
	
	
	# Register the function called when the keyboard is pressed.  
	glutKeyboardFunc(keyPressed)
	glutSpecialFunc(keyPressed)
	# Register mouse events for rotating the perspective
	glutMotionFunc(mouseMoved)
	
	# Initialize our window. 
	InitGL(640, 480)

	# Intialize our obj model
	obj = Obj(filename)
	
if __name__ == "__main__":
	from os import sep
	from optparse import OptionParser

	try:
		GLU_VERSION_1_2
	except:
		print "Need GLU 1.2 to run this exercise"
		sys.exit(1)

	options = {
		# 'one_letter_option' : ['full_option_name',
			# "Help",
			# default_value],
	}
	
	options_list = ' '.join(["[-%s --%s]" % (o, options[o][0]) for o in options])
	desc = main.__doc__.replace('\t','')
	parser = OptionParser("%%prog %s OBJ_FILENAME" % options_list,
			description=desc,
			version="%%prog %s" % __VERSION__)

	for o in options:
		shorter = '-' + o
		longer = '--' + options[o][0]
		if type(options[o][2]) is bool:
			parser.add_option(shorter, longer, dest=o, help=options[o][1],
				action="store_true", default=options[o][2])
		elif type(options[o][2]) is str:
			parser.add_option(shorter, longer, dest=o, help=options[o][1],
				action="store", type="string", default=options[o][2])

	(opt, args) = parser.parse_args(sys.argv)
	if len(args) < MIN_ARGS + 1:
		# not enough arguments
		print """ERROR: not enough arguments.
Try `%s --help' for more information""" % args[0].split(sep)[-1]
		exit(1)

	main(args[1])

	# Print message to console, and kick off the main to get it rolling.
	print "Commands:"
	print "========="
	print "ESC key: Quit."
	print "SPACE key: Switches the view."
	print "+ key: Makes the object bigger."
	print "- key: Makes the object smaller."
	print "ARROW keys: Moves the object."
	print "R key: +Rolls the object (through the X axis)."
	print "r key: -Rolls the object (through the X axis)."
	print "Y key: +Yaws the object (through the Y axis)."
	print "y key: -Yaws the object (through the Y axis)."
	print "P key: +Piches  the object (through the Z axis)."
	print "p key: -Piches the object (through the Z axis)."
	# print """Mouse's "click and drag": Moves the camera through the Z axis."""  # TODO
	print ""

	glutMainLoop()

