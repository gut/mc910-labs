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

from OpenGL.GL import *

def getVectorFrom2Vertices(v1, v2):
	"""Generates a vector calculating @v2 - @v1"""
	return map(lambda x, y: y - x, v1, v2)

def crossProduct(v1, v2):
	"""Cross product by definition on 3D"""
	return (
		v1[1] * v2[2] - v1[2] * v2[1],
		v1[2] * v2[0] - v1[0] * v2[2],
		v1[0] * v2[1] - v1[1] * v2[0]
	)

def drawVertices(mode, vertices, scales, normal_vector = False):
	"""Draw the @vertices within the @mode declared on glBegin.
	Also declare a glNormal3fv if @normal_vector is given"""
	glBegin(mode)
	if normal_vector:
		glNormal3fv(normal_vector)
	for vertex in vertices:
		# let's scale it
		vertex_scaled = map(lambda x : x*scales, vertex)
		vertex_to_use = vertex_scaled
		glVertex3fv(vertex_to_use)
	glEnd()

