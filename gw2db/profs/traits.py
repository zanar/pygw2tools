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

"""traits enpoint mapping

This module gives access to v2/traits enpoint.
For more informations about this endpoint, see:
    <https://wiki.guildwars2.com/wiki/API:2/traits>
    <https://github.com/arenanet/api-cdi/blob/master/v2/traits/traits.md>
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship

from gw2db.common import Base, endpoint_def, rel_json
from gw2db.profs.facts import Gw2Fact


class Gw2Trait(Base):
    """Map the traits endpoint

    This endpoint shows information about traits
    """
    __tablename__ = "gw2_pro_trait"
    __table_args__ = endpoint_def('traits', locale=True)

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    specialization = Column(Integer, ForeignKey("gw2_pro_specialization.id"), nullable=False)
    tier = Column(Integer, nullable=False)
    order = Column(Integer, nullable=False)
    slot = Column(String, nullable=False)

    facts = relationship("Gw2Fact",
                         primaryjoin="Gw2Trait.id == Gw2Fact.trait_id and Gw2Fact.requires_trait == None",
                         uselist=True,
                         info=rel_json(Gw2Fact,
                                       fn=lambda j, pj: [dict(trait_id=pj['id'], is_traited=False, ord=i, **x) for i, x in enumerate(j)]))

    traited_facts = relationship("Gw2Fact",
                                 primaryjoin="Gw2Trait.id == Gw2Fact.trait_id and Gw2Fact.requires_trait != None",
                                 uselist=True,
                                 info=rel_json(Gw2Fact,
                                               fn=lambda j, pj: [dict(trait_id=pj['id'], is_traited=True, ord=i, **x) for i, x in enumerate(j)]))

    Gw2Fact.trait_id.append_foreign_key(ForeignKey("gw2_pro_trait.id"))
