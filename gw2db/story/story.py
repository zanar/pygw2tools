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


class _Gw2StoryChapter(Base):
    __tablename__ = "gw2_sto_story_chapter"

    # Columns
    id = Column(Integer, ForeignKey("gw2_sto_story.id"), primary_key=True)
    name = Column(String, primary_key=True)


class Gw2Story(Base):
    """Map the stories endpoint

    This class gives access to v2/stories enpoint and subendpoints.
    For more informations about this endpoint, see:
        - https://wiki.guildwars2.com/wiki/API:2/stories
        - https://github.com/arenanet/api-cdi/blob/master/v2/stories/index.js

    This endpoint shows information about stories
    """
    __tablename__ = "gw2_sto_story"
    __table_args__ = endpoint_def('stories', locale=True, workers=1)

    # Columns
    id = Column(Integer, primary_key=True)
    season = Column(String, ForeignKey("gw2_sto_season.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    timeline = Column(String, nullable=False)
    level = Column(Integer, nullable=False)
    order = Column(Integer, nullable=False)
    races = Column(Integer, nullable=True, default='')
    flags = Column(Integer, nullable=True, default='')

    # Relations
    chapters = relationship("_Gw2StoryChapter", uselist=True,
                            info=rel_json(_Gw2StoryChapter, fn=lambda j, pj: [dict(id=pj['id'], **x) for x in j]))


class Gw2Season(Base):
    """Map the stories/seasons endpoint

    This class gives access to v2/stories/seasons enpoint and subendpoints.
    For more informations about this endpoint, see:
        - https://wiki.guildwars2.com/wiki/API:2/stories/seasons
        - https://github.com/arenanet/api-cdi/blob/master/v2/stories/seasons.js

    This endpoint shows information about stories seasons
    """
    __tablename__ = "gw2_sto_season"
    __table_args__ = endpoint_def('stories/seasons', locale=True, workers=1)

    # Columns
    pkid = Column(Integer, primary_key=True)
    id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=True)
    order = Column(Integer, nullable=True)

    # Relations
    stories = relationship("Gw2Story", uselist=True)
