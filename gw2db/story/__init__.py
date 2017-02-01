# -*- coding: utf-8 -*-

# This file is part of pyGw2Tools.
#
# pyGw2Tools is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# pyGw2Tools is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with gw2db.
# If not, see <http://www.gnu.org/licenses/>.

"""Stories related enpoints table mapping

This subpackage provides classes which map WebAPI endpoints to tables

Here is the list of accessible endpoints from this package:
    - v2/backstory
    - v2/stories
    - v2/stories/seasons
"""

from .story import Gw2Story, Gw2Season
from .backstory import Gw2BackstoryQuestion, Gw2BackstoryAnswer
