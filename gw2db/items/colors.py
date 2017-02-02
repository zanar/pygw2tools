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
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import relationship

from gw2db.common import Base, endpoint_def, rel_json, col_json


_dye_hue = ['Gray', 'Brown', 'Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple']
_dye_mat = ['Vibrant', 'Leather', 'Metal']
_dye_rar = ['Starter', 'Common', 'Uncommon', 'Rare']


def _intersect(json, std):
    return str(list(set(json).intersection(std)))[1: -1].replace('\'', '')


class _Gw2DyeDetail(Base):
    """Store details about dye for each armor classes"""
    __tablename__ = "gw2_item_dye_detail"

    # Columns
    id = Column(Integer, ForeignKey("gw2_item_dye.id"), primary_key=True)
    type = Column(String, primary_key=True)

    brightness = Column(Integer, nullable=False)
    contrast = Column(Float, nullable=False)
    hue = Column(Integer, nullable=False)
    saturation = Column(Float, nullable=False)
    lightness = Column(Float, nullable=False)

    red = Column(Integer, nullable=False, info=col_json(keys='rgb', fn=lambda j, pj: j[0]), default=0)
    green = Column(Integer, nullable=False, info=col_json(keys='rgb', fn=lambda j, pj: j[1]), default=0)
    blue = Column(Integer, nullable=False, info=col_json(keys='rgb', fn=lambda j, pj: j[2]), default=0)


class Gw2Dye(Base):
    """Map the colors endpoint

    This class gives access to v2/colors enpoint.
    For more informations about this endpoint, see:
        - https://wiki.guildwars2.com/wiki/API:2/colors
        - https://github.com/arenanet/api-cdi/blob/master/v2/colors.js

    This endpoint shows information about a dye
    """
    __tablename__ = "gw2_item_dye"
    __table_args__ = endpoint_def('colors', locale=True, workers=1)

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    item = Column(Integer, ForeignKey("gw2_item_item.id"), nullable=True)

    red = Column(Integer, nullable=False, info=col_json(keys='base_rgb', fn=lambda j, pj: j[0]), default=0)
    green = Column(Integer, nullable=False, info=col_json(keys='base_rgb', fn=lambda j, pj: j[1]), default=0)
    blue = Column(Integer, nullable=False, info=col_json(keys='base_rgb', fn=lambda j, pj: j[2]), default=0)

    hue = Column(String, info=col_json(keys='categories', fn=lambda j, pj: _intersect(j, _dye_hue)), nullable=True)
    material = Column(String, info=col_json(keys='categories', fn=lambda j, pj: _intersect(j, _dye_mat)), nullable=True)
    rarity = Column(String, info=col_json(keys='categories', fn=lambda j, pj: _intersect(j, _dye_rar)), nullable=True)

    # Relations
    cloth = relationship("_Gw2DyeDetail",
                         primaryjoin="_Gw2DyeDetail.id == Gw2Dye.id and _Gw2DyeDetail.type == 'cloth'",
                         uselist=False,
                         info=rel_json(_Gw2DyeDetail, fn=lambda j, pj: dict(id=pj['id'], type='cloth', **j)))

    leather = relationship("_Gw2DyeDetail",
                           primaryjoin="_Gw2DyeDetail.id == Gw2Dye.id and _Gw2DyeDetail.type == 'leather'",
                           uselist=False,
                           info=rel_json(_Gw2DyeDetail, fn=lambda j, pj: dict(id=pj['id'], type='leather', **j)))

    metal = relationship("_Gw2DyeDetail",
                         primaryjoin="_Gw2DyeDetail.id == Gw2Dye.id and _Gw2DyeDetail.type == 'metal'",
                         uselist=False,
                         info=rel_json(_Gw2DyeDetail, fn=lambda j, pj: dict(id=pj['id'], type='metal', **j)))
