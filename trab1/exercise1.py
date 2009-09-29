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

# Based on the 5th tutorial of Richard Cambell, with the python port of John Ferguson and Tony Colston
# http://nehe.gamedev.net/data/lessons/lesson.asp?lesson=05

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

SLICES_STACKS = 20  # Resolution of the subdivisions numbers around and along the Z axis

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
objects = ['cone', 'sphere', 'cube', 'teapot',]
scales = {}
positions = {}
rotations = {}
for obj in objects:
	scales[obj] = 0.5
	positions[obj] = [(-1.5 + objects.index(obj))*2, 0, -7]  # moving to the right
	rotations[obj] = [0,0,0]

# Selected object index
selected = 0

def light(color, obj, alpha = 1.0):
	"""Setup light 0 and enable lighting"""
	if obj == objects[selected]: # let's paint the selected one with white!
		color = [1,1,1]
	color.append(alpha)
	glLightfv(GL_LIGHT0, GL_AMBIENT, GLfloat_4(*color))
	glLightfv(GL_LIGHT0, GL_DIFFUSE, GLfloat_4(1.0, 1.0, 1.0, alpha))
	glLightfv(GL_LIGHT0, GL_SPECULAR, GLfloat_4(1.0, 1.0, 1.0, alpha))
	glLightfv(GL_LIGHT0, GL_POSITION, GLfloat_4(1.0, 1.0, 1.0, 0.0))
	glLightModelfv(GL_LIGHT_MODEL_AMBIENT, GLfloat_4(0.2, 0.2, 0.2, alpha))
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)

# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):				# We call this right after our OpenGL window is created.
	glClearColor(0.0, 0.0, 0.0, 0.0)	# This Will Clear The Background Color To Black
	glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
	glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
	glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
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
	for obj in objects:
		glLoadIdentity()               # Reset The View
		glTranslatef(*positions[obj])         #   Move
		glRotatef(rotations[obj][0], 1.0,0.0,0.0)     # Rotate On It's X Axis
		glRotatef(rotations[obj][1], 0.0,1.0,0.0)     # Rotate On It's Y Axis
		glRotatef(rotations[obj][2], 0.0,0.0,1.0)     # Rotate On It's Z Axis
		glPushMatrix()
		if obj is 'cone':
			light([1.0,0,0], obj)  # red
			glutSolidCone(scales[obj], scales[obj], SLICES_STACKS, SLICES_STACKS)
		elif obj is 'sphere':
			light([0,0,1.0], obj)  # blue
			glutSolidSphere(scales[obj], SLICES_STACKS, SLICES_STACKS)
		elif obj is 'cube':
			light([0,1.0,0], obj)  # green
			glutSolidCube(scales[obj])
		elif obj is 'teapot':
			glEnable(GL_BLEND)
			glBlendFunc(GL_SRC_ALPHA, GL_ONE)
			light([1.0,1.0,0], obj, alpha=0.2)  # transparent yellow
			glutSolidTeapot(scales[obj])
			glDisable(GL_BLEND)
		glPopMatrix()
		#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)  
def keyPressed(*args):
	global selected
	selected_object = objects[selected]
	# If escape is pressed, kill everything.
	if args[0] == ESCAPE:
		glutDestroyWindow(window)
		sys.exit()
	elif args[0] == SPACE:
		# cicle through objects
		selected = (selected + 1) % len(objects)
	elif args[0] == BIGGER:
		scales[selected_object] += .1
	elif args[0] == SMALLER:
		if scales[selected_object] >= 0.4:
			scales[selected_object] -= .1
	elif args[0] == ROT_X_PLUS:
		rotations[selected_object][0] += 20
	elif args[0] == ROT_X_MINUS:
		rotations[selected_object][0] -= 20
	elif args[0] == ROT_Y_PLUS:
		rotations[selected_object][1] += 20
	elif args[0] == ROT_Y_MINUS:
		rotations[selected_object][1] -= 20
	elif args[0] == ROT_Z_PLUS:
		rotations[selected_object][2] += 20
	elif args[0] == ROT_Z_MINUS:
		rotations[selected_object][2] -= 20
	elif args[0] == GLUT_KEY_UP:
		positions[selected_object][1] += .1
	elif args[0] == GLUT_KEY_RIGHT:
		positions[selected_object][0] += .1
	elif args[0] == GLUT_KEY_DOWN:
		positions[selected_object][1] -= .1
	elif args[0] == GLUT_KEY_LEFT:
		positions[selected_object][0] -= .1

def mouseMoved(x,y):
	# Unfortunatelly I wasn't able to implement this feature :'(
	pass

def main():
	"""Exercise #1 of mc930"""
	global window

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
	window = glutCreateWindow("MC930 1st Exercise - Gustavo Serra Scalet")

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

	
if __name__ == "__main__":
	from os import sep
	try:
		GLU_VERSION_1_2
	except:
		print "Need GLU 1.2 to run this exercise"
		sys.exit(1)
	main()

	# Print message to console, and kick off the main to get it rolling.
	print "Commands:"
	print "========="
	print "ESC key: Quit."
	print "+ key: Makes the object bigger."
	print "- key: Makes the object smaller."
	print "ARROW keys: Moves the object."
	print "SPACE key: Cycles through the objects (selected object is drawn in white!)."
	print "R key: +Rolls the object (through the X axis)."
	print "r key: -Rolls the object (through the X axis)."
	print "Y key: +Yaws the object (through the Y axis)."
	print "y key: -Yaws the object (through the Y axis)."
	print "P key: +Piches  the object (through the Z axis)."
	print "p key: -Piches the object (through the Z axis)."
	# print """Mouse's "click and drag": Moves the camera through the Z axis."""  # TODO
	print ""

	glutMainLoop()

