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

"""guild/upgrades enpoint mapping

This module gives access to v2/guild/upgrades enpoint.
For more informations about this endpoint, see:
    <https://wiki.guildwars2.com/wiki/API:2/guild/upgrades>
    <https://github.com/arenanet/api-cdi/blob/master/v2/guild/upgrades.js>
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship

from gw2db.common import Base, endpoint_def, rel_json


class _Gw2GuildUpgradeReq(Base):
    __tablename__ = "gw2_item_guild_upgrade_req_rel"

    # Columns
    id = Column(Integer, ForeignKey("gw2_item_guild_upgrade.id"), primary_key=True)
    req_id = Column(Integer, ForeignKey("gw2_item_guild_upgrade.id"), primary_key=True)


class _Gw2GuildUpgradeCost(Base):
    __tablename__ = "gw2_item_guild_upgrade_cost"

    # Columns
    pkid = Column(Integer, primary_key=True)
    id = Column(Integer, ForeignKey("gw2_item_guild_upgrade.id"), nullable=False)
    type = Column(String, nullable=False)
    name = Column(String, nullable=True)
    count = Column(Integer, nullable=False)
    item_id = Column(Integer, ForeignKey("gw2_item_item.id"), nullable=True)

    # Relations
    item = relationship("Gw2Item", uselist=False)


class Gw2GuildUpgrade(Base):
    __tablename__ = "gw2_item_guild_upgrade"
    __table_args__ = endpoint_def('guild/upgrades', locale=True)

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    type = Column(String, nullable=False)
    icon = Column(String, nullable=False)

    bag_max_items = Column(Integer, nullable=True)
    bag_max_coins = Column(Integer, nullable=True)

    build_time = Column(Integer, nullable=False)
    required_level = Column(Integer, nullable=False)
    experience = Column(Integer, nullable=False)

    # Relations
    prerequisites = relationship("Gw2GuildUpgrade",
                                 secondary="gw2_item_guild_upgrade_req_rel",
                                 primaryjoin="_Gw2GuildUpgradeReq.id == Gw2GuildUpgrade.id",
                                 secondaryjoin="_Gw2GuildUpgradeReq.req_id == Gw2GuildUpgrade.id",
                                 uselist=True,
                                 info=rel_json(_Gw2GuildUpgradeReq, fn=lambda j, pj: [dict(id=pj['id'], req_id=x) for x in j]))

    costs = relationship("_Gw2GuildUpgradeCost",
                         uselist=True,
                         info=rel_json(_Gw2GuildUpgradeCost, fn=lambda j, pj: [dict(id=pj['id'], **x) for x in j]))
