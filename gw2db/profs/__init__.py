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

"""Professions related enpoints table mapping

This subpackage provides classes which map WebAPI endpoints to tables

Here is the list of accessible endpoints from this package:
    - v2/legends
    - v2/masteries
    - v2/pets
    - v2/professions
    - v2/skills
    - v2/specializations
    - v2/traits
"""

from .legends import Gw2Legend
from .masteries import Gw2Mastery
from .pets import Gw2Pet
from .professions import Gw2Profession
from .skills import Gw2Skill
from .specializations import Gw2Specialization
from .traits import Gw2Trait
