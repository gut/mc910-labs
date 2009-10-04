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
from OpenGL.GLUT import *
from OpenGL.GLU import *
from itertools import izip
from views_definition import *
from auxiliar import *

class Obj:
	def __init__(self, filename):
		"""Loads a Wavefront OBJ file. """
		self.__obj_vertices = []
		self.__obj_faces = []

		for line in open(filename, "r"):
			values = line.split()
			if not values: continue
			if values[0] == 'v':
				v = map(float, values[1:4])
				v[2] -= 4
				self.__obj_vertices.append(v)
			elif values[0] == 'f':
				face = []
				texcoords = []
				norms = []
				for v in values[1:]:
					w = v.split('/')
					face.append(int(w[0]))
					texcoords.append(0)
					norms.append(0)
				self.__obj_faces.append(face)
		self.generateDerivatedGeometry()
	
	def generateDerivatedGeometry(self):
		"""Calculate before showing the object some more atributes"""
		self.normals = []  # the vector for each face 
		self.faces = []  # tuple of 3 vertices
		for three_vertices in self.__obj_faces:
			face = [self.__obj_vertices[vertex-1] for vertex in three_vertices]
			self.faces.append(tuple(face))
			v1 = getVectorFrom2Vertices(face[0], face[1])
			v2 = getVectorFrom2Vertices(face[1], face[2])
			normal = crossProduct(v1, v2)
			self.normals.append(normal)
	
	def show(self, scales, view):
		# default mode, fallback
		mode = GL_TRIANGLES
		glLineWidth(2.0)

		if view is ESTRUTURA_DE_ARAME:
			self.light([0,1,0])  # green
			mode = GL_LINE_STRIP
		elif view is SOMBREAMENTO_PLANO:
			self.light([0.1,0.1,0.1])  # grey
		elif view is ESTRUTURA_DE_ARAME_E_POLIGONOS:
			self.show(scales, ESTRUTURA_DE_ARAME)
			self.light([0.1,0.1,0.1])  # grey
		elif view is SOMBREAMENTO_SUAVE:
			self.light([1,0,0])  # red
			mode = GL_POLYGON
		elif view is SILHUETA:
			self.show(scales, SILHUETA_AUX)  # draws the non-ortogonal polys
			self.light([1,1,1])  # white
			glPolygonMode(GL_BACK, GL_LINE)
			glLineWidth(5.0)
		elif view is SILHUETA_AUX:
			self.light([0,0,0])  # black
			glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
		elif view is SILHUETA_E_SOMBREAMENTO:
			self.show(scales, SILHUETA)
			self.light([1,1,0])  # yellow

		for vertices, normal_vector in izip(self.faces, self.normals):
			if view is SOMBREAMENTO_SUAVE:
				drawVertices(mode, vertices, scales, normal_vector)
			else:
				drawVertices(mode, vertices, scales)

	def light(self, color, alpha = 1.0):
		"""Setup light 0 and enable lighting"""
		glColor3f(*color)
		return
		color.append(alpha)
		glLightfv(GL_LIGHT0, GL_AMBIENT, GLfloat_4(*color))
		glLightfv(GL_LIGHT0, GL_DIFFUSE, GLfloat_4(1.0, 1.0, 1.0, alpha))
		glLightfv(GL_LIGHT0, GL_SPECULAR, GLfloat_4(1.0, 1.0, 1.0, alpha))
		glLightfv(GL_LIGHT0, GL_POSITION, GLfloat_4(1.0, 1.0, 1.0, 0.0))
		glLightModelfv(GL_LIGHT_MODEL_AMBIENT, GLfloat_4(0.2, 0.2, 0.2, alpha))
		glEnable(GL_LIGHTING)
		glEnable(GL_LIGHT0)

