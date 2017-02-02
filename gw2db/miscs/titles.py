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


class Gw2Title(Base):
    """Map the titles endpoint

    This class gives access to v2/titles enpoint.
    For more informations about this endpoint, see:
        - https://wiki.guildwars2.com/wiki/API:2/titles
        - https://github.com/arenanet/api-cdi/blob/master/v2/titles.js

    This endpoint shows information about titles
    """
    __tablename__ = "gw2_misc_title"
    __table_args__ = endpoint_def('titles', locale=True, workers=1)

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ap_required = Column(Integer, nullable=True)
    achievement_id = Column(Integer, ForeignKey("gw2_misc_achievement.id"), nullable=True, info=col_json(keys='achievement'))

    achievement = relationship("Gw2Achievement", uselist=False)
