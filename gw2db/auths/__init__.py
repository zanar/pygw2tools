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

"""Authenticated enpoints table mapping

This subpackage provides classes which map WebAPI endpoints to tables. To access authenticated endpoints, you need
an access token provided here: https://account.arena.net/applications.

Here is the list of accessible endpoints from this package:
    - v2/account
    - v2/account/achievements
    - v2/account/bank
    - v2/account/dyes
    - v2/account/finishers
    - v2/account/inventory
    - v2/account/masteries
    - v2/account/materials
    - v2/account/minis
    - v2/account/outfits
    - v2/account/recipes
    - v2/account/skins
    - v2/account/titles
    - v2/account/wallet
    - v2/characters
    - v2/guild/:id
    - v2/tokeninfo
"""

from .accounts import Gw2Account
from .characters import Gw2Character
from .guilds import Gw2Guild
from .token import Gw2Token