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

"""itemstats enpoint mapping

This module gives access to v2/itemstats enpoint.
For more informations about this endpoint, see:
    <https://wiki.guildwars2.com/wiki/API:2/itemstats>
    <https://github.com/arenanet/api-cdi/blob/master/v2/itemstats.js>
"""

from sqlalchemy import Column
from sqlalchemy import Integer, String

from gw2db.common import Base, endpoint_def, col_json


class Gw2Itemstat(Base):
    """Map the itemstats endpoint

    This endpoint shows information about items stats
    """
    __tablename__ = "gw2_item_item_stat"
    __table_args__ = endpoint_def('itemstats', locale=True, workers=3)

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    agony_resistance = Column(Integer, nullable=False, default=0, info=col_json(keys=['attributes', 'AgonyResistance']))
    boon_duration = Column(Integer, nullable=False, default=0, info=col_json(keys=['attributes', 'BoonDuration']))
    condition_damage = Column(Integer, nullable=False, default=0, info=col_json(keys=['attributes', 'ConditionDamage']))
    condition_duration = Column(Integer, nullable=False, default=0, info=col_json(keys=['attributes', 'ConditionDuration']))
    crit_damage = Column(Integer, nullable=False, default=0, info=col_json(keys=['attributes', 'CritDamage']))
    healing = Column(Integer, nullable=False, default=0, info=col_json(keys=['attributes', 'Healing']))
    power = Column(Integer, nullable=False, default=0, info=col_json(keys=['attributes', 'Power']))
    precision = Column(Integer, nullable=False, default=0, info=col_json(keys=['attributes', 'Precision']))
    thoughness = Column(Integer, nullable=False, default=0, info=col_json(keys=['attributes', 'Thoughness']))
    vitality = Column(Integer, nullable=False, default=0, info=col_json(keys=['attributes', 'Vitality']))
