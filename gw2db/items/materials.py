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


class _Gw2MaterialItem(Base):
    """Store items of this material"""
    __tablename__ = "gw2_item_material_item_rel"

    # Columns
    material_id = Column(Integer, ForeignKey("gw2_item_material.id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("gw2_item_item.id"), primary_key=True)


class Gw2Material(Base):
    """Map the materials endpoint

    This class gives access to v2/colors enpoint.
    For more informations about this endpoint, see:
        - https://wiki.guildwars2.com/wiki/API:2/materials
        - https://github.com/arenanet/api-cdi/blob/master/v2/materials.js

    This endpoint shows information about materials
    """
    __tablename__ = "gw2_item_material"
    __table_args__ = endpoint_def('materials', locale=True, workers=1)

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    order = Column(Integer, nullable=False)

    # Relations
    items = relationship("Gw2Item",
                         secondary="gw2_item_material_item_rel",
                         uselist=True,
                         info=rel_json(_Gw2MaterialItem,
                                       fn=lambda j, pj: [dict(material_id=pj['id'], item_id=x) for x in j]))
