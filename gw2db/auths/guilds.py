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

from gw2db.common import Base, endpoint_def, rel_json, col_json, EPType


class _Gw2GuildEmblemBackColor(Base):
    """Store colors defined for the background emblem"""
    __tablename__ = "gw2_auth_guild_emblem_back_color"

    guild_pkid = Column(String, ForeignKey("gw2_auth_guild.pkid"), primary_key=True)
    order = Column(Integer, primary_key=True)
    color_id = Column(Integer, ForeignKey("gw2_item_dye.id"), primary_key=True)


class _Gw2GuildEmblemForeColor(Base):
    """Store colors defined for the background emblem"""
    __tablename__ = "gw2_auth_guild_emblem_fore_color"

    guild_pkid = Column(String, ForeignKey("gw2_auth_guild.pkid"), primary_key=True)
    order = Column(Integer, primary_key=True)
    color_id = Column(Integer, ForeignKey("gw2_item_dye.id"), primary_key=True)


class Gw2Guild(Base):
    """Map the guild/:id endpoint

    This class gives access to v2/guild/:id enpoint.
    For more informations about this endpoint, see:
        - https://wiki.guildwars2.com/wiki/API:2/guild/:id
        - https://github.com/arenanet/api-cdi/blob/master/v2/guild/details.js

    This endpoint shows the informations of a guild
    """
    __tablename__ = "gw2_auth_guild"
    __table_args__ = endpoint_def('guild/%s', EPType.psac, workers=3, parent='Gw2Account')

    pkid = Column(Integer, primary_key=True)
    id = Column(String, primary_key=True)
    api_key = Column(String, ForeignKey("gw2_auth_account.api_key"), primary_key=True)
    name = Column(String, nullable=False)
    tag = Column(String, nullable=False)
    level = Column(Integer)
    motd = Column(String)
    influence = Column(Integer)
    aetherium = Column(Integer)
    favor = Column(Integer)
    emblem_bid = Column(Integer, ForeignKey("gw2_misc_emblem_back_layer.emblem_id"), nullable=False,
                        info=col_json(keys=['emblem', 'background', 'id']))
    emblem_fid = Column(Integer, ForeignKey("gw2_misc_emblem_fore_layer.emblem_id"), nullable=False,
                        info=col_json(keys=['emblem', 'foreground', 'id']))
    emblem_flags = Column(String, nullable=False, info=col_json(keys=['emblem', 'flags']))

    emblem_back = relationship("_Gw2EmblemBackgroundLayer", uselist=True)
    emblem_back_colors = relationship("Gw2Dye",
                                      secondary="gw2_auth_guild_emblem_back_color",
                                      info=rel_json(_Gw2GuildEmblemBackColor,
                                                    keys=['emblem', 'background', 'colors'],
                                                    fn=lambda j, pj: [{'color_id': x,
                                                                       'order': i,
                                                                       'guild_pkid': pj['pkid']} for i, x in enumerate(j)]))
    emblem_fore = relationship("_Gw2EmblemForegroundLayer", uselist=True)
    emblem_fore_colors = relationship("Gw2Dye",
                                      secondary="gw2_auth_guild_emblem_fore_color",
                                      info=rel_json(_Gw2GuildEmblemForeColor,
                                                    keys=['emblem', 'foreground', 'colors'],
                                                    fn=lambda j, pj: [{'color_id': x,
                                                                       'order': i,
                                                                       'guild_pkid': pj['pkid']} for i, x in enumerate(j)]))

    @staticmethod
    def from_parent(_pjson):
        ids = [(x,) for x in _pjson['guild_leader']]
        ids .extend([(x,) for x in _pjson['guilds'] if x not in _pjson['guild_leader']])
        return (ids, None)