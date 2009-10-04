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

from itertools import count
__c = count()

# it's like an enum
ESTRUTURA_DE_ARAME = __c.next()
SOMBREAMENTO_PLANO = __c.next()
ESTRUTURA_DE_ARAME_E_POLIGONOS = __c.next()
SOMBREAMENTO_SUAVE = __c.next()
SILHUETA = __c.next()
SILHUETA_AUX = __c.next()  # used on SILHUETA
SILHUETA_E_SOMBREAMENTO = __c.next()
