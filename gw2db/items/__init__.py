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

"""Items related enpoints table mapping

This subpackage provides classes which map WebAPI endpoints to tables

Here is the list of accessible endpoints from this package:
    - v2/colors
    - v2/guild/upgrades
    - v2/items
    - v2/itemstats
    - v2/materials
    - v2/minis
    - v2/recipes
    - v2/skins
"""

from .colors import Gw2Dye
from .guild import Gw2GuildUpgrade
from .items import Gw2Item, Gw2ArmorItem, Gw2BackItem, Gw2BagItem, Gw2ConsumableItem, Gw2ContainerItem, \
    Gw2CraftingMaterialItem, Gw2GatheringItem, Gw2GizmoItem, Gw2MiniatureItem, Gw2SalvageItem, Gw2TraitItem, \
    Gw2TrinketItem, Gw2UpgradeItem, Gw2WeaponItem
from .itemstats import Gw2Itemstat
from .materials import Gw2Material
from .minipets import Gw2MiniPet
from .recipes import Gw2Recipe
from .skins import Gw2Skin
