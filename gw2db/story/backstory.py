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

"""backstory enpoint mapping

This module gives access to v2/backstory enpoint.
For more informations about this endpoint, see:
    <https://wiki.guildwars2.com/wiki/API:2/backstory/*>
    <https://github.com/arenanet/api-cdi/tree/master/v2/backstory>
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship

from gw2db.common import Base, endpoint_def, col_json


class Gw2BackstoryQuestion(Base):
    """Map the backstory/questions endpoint

    This endpoint shows information about backstory questions
    """
    __tablename__ = "gw2_sto_backstory_question"
    __table_args__ = endpoint_def('backstory/questions', locale=True, workers=1)

    # Columns
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    order = Column(Integer, nullable=False)
    races = Column(String, nullable=True)
    professions = Column(String, nullable=True)

    # Relations
    answers = relationship("Gw2BackstoryAnswer", uselist=True)


class Gw2BackstoryAnswer(Base):
    """Map the backstory/answers endpoint

    This endpoint shows information about backstory answers
    """
    __tablename__ = "gw2_sto_backstory_answer"
    __table_args__ = endpoint_def('backstory/answers', locale=True, workers=1)

    # Columns
    pkid = Column(Integer, primary_key=True)
    id = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    journal = Column(String, nullable=False)
    description = Column(String, nullable=False)
    question_id = Column(Integer, ForeignKey("gw2_sto_backstory_question.id"), nullable=False,
                         info=col_json(keys='question'))
    races = Column(String, nullable=True)
    professions = Column(String, nullable=True)

    # Relations
    question = relationship("Gw2BackstoryQuestion", uselist=False)
