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

"""currencies enpoint mapping

This module gives access to v2/currencies enpoint.
For more informations about this endpoint, see:
    <https://wiki.guildwars2.com/wiki/API:2/currencies>
    <https://github.com/arenanet/api-cdi/blob/master/v2/currencies.js>
"""

from sqlalchemy import Column, Integer, String

from gw2db.common import Base, endpoint_def


class Gw2Currency(Base):
    """Map the currencies endpoint

    This endpoint shows information about currencies
    """
    __tablename__ = "gw2_misc_currencies"
    __table_args__ = endpoint_def('currencies', locale=True, workers=1)

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    order = Column(Integer, nullable=False)
