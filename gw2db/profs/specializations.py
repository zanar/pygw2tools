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

"""specializations enpoint mapping

This module gives access to v2/specializations enpoint.
For more informations about this endpoint, see:
    <https://wiki.guildwars2.com/wiki/API:2/specializations>
    <https://github.com/arenanet/api-cdi/blob/master/v2/specializations/specializations.js>
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship

from gw2db.common import Base, endpoint_def


class Gw2Specialization(Base):
    """Map the specializations endpoint

    This endpoint shows information about specializations
    """
    __tablename__ = "gw2_pro_specialization"
    __table_args__ = endpoint_def('specializations', locale=True, workers=3)

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    profession = Column(String, ForeignKey("gw2_pro_profession.id"), nullable=False)
    elite = Column(Boolean, nullable=False, default=False)
    icon = Column(String, nullable=False)
    background = Column(String, nullable=False)
    profession_icon = Column(String, nullable=True, default='')
    profession_icon_big = Column(String, nullable=True, default='')
    weapon_trait = Column(Integer, ForeignKey("gw2_pro_trait.id"), nullable=True)

    elite_trait = relationship("Gw2Trait", foreign_keys=[weapon_trait], uselist=False)

    minors = relationship("Gw2Trait",
                          primaryjoin="Gw2Trait.specialization == Gw2Specialization.id and Gw2Trait.slot == 'Minor'",
                          uselist=True)
    majors = relationship("Gw2Trait",
                          primaryjoin="Gw2Trait.specialization == Gw2Specialization.id and Gw2Trait.slot == 'Major'",
                          uselist=True)
