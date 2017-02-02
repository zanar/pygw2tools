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

from gw2db.common import Base, endpoint_def, rel_json


class _Gw2EmblemForegroundLayer(Base):
    __tablename__ = "gw2_misc_emblem_fore_layer"

    # Columns
    emblem_id = Column(Integer, ForeignKey("gw2_misc_emblem_fore.id"), primary_key=True)
    layer = Column(String, primary_key=True)


class Gw2EmblemForeground(Base):
    """Map the emblem/foregrounds endpoint

    This class gives access to v2/emblem/foregrounds enpoint.
    For more informations about this endpoint, see:
        - https://wiki.guildwars2.com/wiki/API:2/emblem
        - https://github.com/arenanet/api-cdi/blob/master/v2/emblems/emblems.js

    This endpoint shows information about emblems foregrounds
    """
    __tablename__ = "gw2_misc_emblem_fore"
    __table_args__ = endpoint_def('emblem/foregrounds', workers=1)

    # Columns
    id = Column(Integer, primary_key=True)

    # Relations
    layers = relationship("_Gw2EmblemForegroundLayer", uselist=True,
                          info=rel_json(_Gw2EmblemForegroundLayer,
                                        fn=lambda j, pj: [dict(emblem_id=pj['id'], layer=x) for x in j]))


class _Gw2EmblemBackgroundLayer(Base):
    __tablename__ = "gw2_misc_emblem_back_layer"

    # Columns
    emblem_id = Column(Integer, ForeignKey("gw2_misc_emblem_back.id"), primary_key=True)
    layer = Column(String, primary_key=True)


class Gw2EmblemBackground(Base):
    """Map the emblem/backgrounds endpoint

    This class gives access to v2/emblem/backgrounds enpoint.
    For more informations about this endpoint, see:
        - https://wiki.guildwars2.com/wiki/API:2/emblem
        - https://github.com/arenanet/api-cdi/blob/master/v2/emblems/emblems.js

    This endpoint shows information about emblems backgrounds
    """
    __tablename__ = "gw2_misc_emblem_back"
    __table_args__ = endpoint_def('emblem/backgrounds', workers=1)

    # Columns
    id = Column(Integer, primary_key=True)

    # Relations
    layers = relationship("_Gw2EmblemBackgroundLayer", uselist=True,
                          info=rel_json(_Gw2EmblemBackgroundLayer,
                                        fn=lambda j, pj: [dict(emblem_id=pj['id'], layer=x) for x in j]))
