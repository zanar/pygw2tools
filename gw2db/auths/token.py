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


from sqlalchemy import Column
from sqlalchemy import Integer, String

from gw2db.common import Base, endpoint_def, EPType


class Gw2Token(Base):
    """Map the tokeninfo endpoint

    This class gives access to v2/tokeninfo enpoint.
    For more informations about this endpoint, see:
        - https://wiki.guildwars2.com/wiki/API:2/tokeninfo
        - https://github.com/arenanet/api-cdi/blob/master/v2/tokeninfo/tokeninfo.js

    This endpoint shows the READ permissions given by an access token
    """
    __tablename__ = "gw2_auth_token"
    __table_args__ = endpoint_def('tokeninfo', ep_type=EPType.sa, workers=1)

    pkid = Column(Integer, primary_key=True)
    api_key = Column(String, unique=True, nullable=False)
    permissions = Column(String, nullable=False)

    @staticmethod
    def to_child(ch, key, _json):
        if len(set(ch.rights).intersection(_json['permissions'])) == len(ch.rights):
            ch.set_params(key, _json)
