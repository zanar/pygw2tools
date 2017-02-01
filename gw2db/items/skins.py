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

"""skins enpoint mapping

This module gives access to v2/skins enpoint.
For more informations about this endpoint, see:
    <https://wiki.guildwars2.com/wiki/API:2/skins>
    <https://github.com/arenanet/api-cdi/blob/master/v2/skins.js>
"""

from sqlalchemy import Column
from sqlalchemy import Integer, String

from gw2db.common import Base, endpoint_def, col_json


class Gw2Skin(Base):
    """Map the skins endpoint

    This endpoint shows information about skins
    """
    __tablename__ = "gw2_item_skin"
    __table_args__ = endpoint_def('skins', locale=True)

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    flags = Column(String, nullable=True)
    restrictions = Column(String, nullable=True)
    icon = Column(String, nullable=True)
    rarity = Column(String, nullable=False)
    description = Column(String, nullable=True)
    slot = Column(String, nullable=True, info=col_json(keys=['details', 'type']))
    weight_class = Column(String, nullable=True, info=col_json(keys=['details', 'weight_class']))
    damage_type = Column(String, nullable=True, info=col_json(keys=['details', 'damage_type']))
