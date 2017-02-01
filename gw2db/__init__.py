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

"""Database manager, ORM mapping classes

The gw2db package provides an ORM over SQLite mapper for GuildWars2 WebAPI.

The entry point is ``Gw2Db``
It also provides
"""

from .auths import Gw2Account, Gw2Character, Gw2Guild, Gw2Token

from .items import Gw2Dye, Gw2GuildUpgrade, Gw2Itemstat, Gw2Material, Gw2MiniPet, Gw2Recipe, Gw2Skin
from .items import Gw2Item, Gw2ArmorItem, Gw2BackItem, Gw2BagItem, Gw2ConsumableItem, Gw2ContainerItem, \
    Gw2CraftingMaterialItem, Gw2GatheringItem, Gw2GizmoItem, Gw2MiniatureItem, Gw2SalvageItem, Gw2TraitItem, \
    Gw2TrinketItem, Gw2UpgradeItem, Gw2WeaponItem

from .miscs import Gw2Achievement, Gw2AchievementCategory, Gw2AchievementGroup, Gw2Currency, Gw2EmblemBackground, \
    Gw2EmblemForeground, Gw2Finisher, Gw2Outfit, Gw2Title, Gw2World

from .profs import Gw2Legend, Gw2Mastery, Gw2Pet, Gw2Profession, Gw2Skill, Gw2Specialization, Gw2Trait

from .story import Gw2Story, Gw2Season, Gw2BackstoryQuestion, Gw2BackstoryAnswer

from .gw2db import Gw2Db, DbUpgradeStatus, EndpointUpgradeStatus
