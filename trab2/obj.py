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

# Based on: http://www.pygame.org/wiki/OBJFileLoader

from OpenGL.GL import *

class Obj:
	def __init__(self, filename):
		"""Loads a Wavefront OBJ file. """
		self.vertices = []
		self.faces = []

		for line in open(filename, "r"):
			values = line.split()
			if not values: continue
			if values[0] == 'v':
				v = map(float, values[1:4])
				self.vertices.append(v)
			elif values[0] == 'f':
				face = []
				texcoords = []
				norms = []
				for v in values[1:]:
					w = v.split('/')
					face.append(int(w[0]))
					texcoords.append(0)
					norms.append(0)
				self.faces.append(face)
	
	def show(self):
		self.gl_list = glGenLists(1)
		glNewList(self.gl_list, GL_COMPILE)
		glFrontFace(GL_CCW)
		for vertices in self.faces:
			glBegin(GL_POLYGON)
			for i in range(0, len(vertices)):
				glVertex3fv(self.vertices[vertices[i] - 1])
			glEnd()
		glDisable(GL_TEXTURE_2D)
		glEndList()
