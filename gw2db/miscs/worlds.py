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
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship

from gw2db.common import Base, endpoint_def, rel_json, col_json


class Gw2World(Base):
    """Map the worlds endpoint

    This class gives access to v2/worlds enpoint.
    For more informations about this endpoint, see:
        - https://wiki.guildwars2.com/wiki/API:2/worlds
        - https://github.com/arenanet/api-cdi/blob/master/v2/worlds.js

    This endpoint shows information about server worlds
    """
    __tablename__ = "gw2_misc_world"
    __table_args__ = endpoint_def('worlds', locale=True, workers=2)

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    population = Column(String, nullable=False)
