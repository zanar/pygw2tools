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

"""pets enpoint mapping
"""

from sqlalchemy import Column
from sqlalchemy import Integer, String

from gw2db.common import Base, endpoint_def


class Gw2Pet(Base):
    """Map the Ranger's pets endpoint

    This class gives access to v2/pets enpoint.
    For more informations about this endpoint, see:
        - https://wiki.guildwars2.com/wiki/API:2/pets
        - https://github.com/arenanet/api-cdi/blob/master/v2/pets.js

    This endpoint shows information about pets
    """
    __tablename__ = "gw2_pro_pet"
    __table_args__ = endpoint_def('pets', locale=True, workers=2)

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    icon = Column(String, nullable=False)
