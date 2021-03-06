# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012 Kozea
#
# This library is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pygal. If not, see <http://www.gnu.org/licenses/>.
"""
Stacked Line chart

"""
from __future__ import division
from pygal.graph.line import Line
from pygal.adapters import none_to_zero


class StackedLine(Line):
    """Stacked Line graph"""

    _adapters = [none_to_zero]

    def __init__(self, *args, **kwargs):
        self._previous_line = None
        super(StackedLine, self).__init__(*args, **kwargs)

    def _fill(self, values):
        if not self._previous_line:
            self._previous_line = values
            return super(StackedLine, self)._fill(values)
        new_values = values + list(reversed(self._previous_line))
        self._previous_line = values
        return new_values

    def _points(self, x_pos):
        accumulation = [0] * self._len
        for serie in self.series:
            accumulation = map(sum, zip(accumulation, serie.values))
            serie.points = [
                (x_pos[i], v)
                for i, v in enumerate(accumulation)]
            print serie.points
            if self.interpolate:
                serie.interpolated = self._interpolate(accumulation, x_pos)
