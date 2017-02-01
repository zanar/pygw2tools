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

"""masteries enpoint mapping

This module gives access to v2/masteries enpoint.
For more informations about this endpoint, see:
    <https://wiki.guildwars2.com/wiki/API:2/masteries>
    <https://github.com/arenanet/api-cdi/blob/master/v2/masteries.js>
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship

from gw2db.common import Base, endpoint_def, rel_json


class _Gw2MasteryLevel(Base):
    __tablename__ = "gw2_pro_mastery_level"

    pkid = Column(Integer, primary_key=True)
    mastery_id = Column(Integer, ForeignKey("gw2_pro_mastery.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    instruction = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    point_cost = Column(Integer, nullable=False)
    exp_cost = Column(Integer, nullable=False)


class Gw2Mastery(Base):
    """Map the masteries endpoint

    This endpoint shows information about masteries
    """
    __tablename__ = "gw2_pro_mastery"
    __table_args__ = endpoint_def('masteries', locale=True, workers=1)

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    requirement = Column(String, nullable=False)
    order = Column(Integer, nullable=False)
    background = Column(String, nullable=False)
    region = Column(String, nullable=False)

    levels = relationship("_Gw2MasteryLevel",
                          uselist=True,
                          info=rel_json(_Gw2MasteryLevel,
                                        fn=lambda j, pj: [dict(mastery_id=pj['id'], **x) for x in j]))
