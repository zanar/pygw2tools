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

"""Miscellaneous enpoints table mapping

This subpackage provides classes which map WebAPI endpoints to tables

Here is the list of accessible endpoints from this package:
    - v2/achievements
    - v2/achievements/categories
    - v2/achievements/groups
    - v2/currencies
    - v2/emblem/backgrounds
    - v2/emblem/foregrounds
    - v2/finishers
    - v2/outfits
    - v2/titles
    - v2/worlds
"""

from .achievements import Gw2Achievement, Gw2AchievementCategory, Gw2AchievementGroup
from .currency import Gw2Currency
from .emblem import Gw2EmblemBackground, Gw2EmblemForeground
from .finishers import Gw2Finisher
from .outfits import Gw2Outfit
from .titles import Gw2Title
from .worlds import Gw2World