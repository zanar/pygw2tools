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


from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship

from gw2db.common import Base, endpoint_def, col_json


class Gw2Legend(Base):
    """Map the Revenant's legends endpoint

    This class gives access to v2/legends enpoint.
    For more informations about this endpoint, see:
        - https://wiki.guildwars2.com/wiki/API:2/legends
        - https://github.com/arenanet/api-cdi/blob/master/v2/legends.js

    This endpoint shows information about legends
    """
    __tablename__ = "gw2_pro_legend"
    __table_args__ = endpoint_def('legends', workers=1)

    pkid = Column(Integer, primary_key=True)
    id = Column(String, unique=True, nullable=False)
    swap_id = Column(Integer, ForeignKey("gw2_pro_skill.id"), nullable=False, info=col_json(keys='swap'))
    heal_id = Column(Integer, ForeignKey("gw2_pro_skill.id"), nullable=False, info=col_json(keys='heal'))
    elite_id = Column(Integer, ForeignKey("gw2_pro_skill.id"), nullable=False, info=col_json(keys='elite'))
    util0_id = Column(Integer, ForeignKey("gw2_pro_skill.id"), nullable=False, info=col_json(keys='utilities', fn=lambda j, pj: j[0]))
    util1_id = Column(Integer, ForeignKey("gw2_pro_skill.id"), nullable=False, info=col_json(keys='utilities', fn=lambda j, pj: j[1]))
    util2_id = Column(Integer, ForeignKey("gw2_pro_skill.id"), nullable=False, info=col_json(keys='utilities', fn=lambda j, pj: j[2]))

    swap = relationship("Gw2Skill", foreign_keys=[swap_id], uselist=False)
    heal = relationship("Gw2Skill", foreign_keys=[heal_id], uselist=False)
    elite = relationship("Gw2Skill", foreign_keys=[elite_id], uselist=False)
    util0 = relationship("Gw2Skill", foreign_keys=[util0_id], uselist=False)
    util1 = relationship("Gw2Skill", foreign_keys=[util1_id], uselist=False)
    util2 = relationship("Gw2Skill", foreign_keys=[util2_id], uselist=False)
