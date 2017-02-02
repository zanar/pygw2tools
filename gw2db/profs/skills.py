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
from gw2db.profs.facts import Gw2Fact


class _Gw2ProfSkill(Base):
    __tablename__ = "gw2_pro_profession_skill_rel"

    prof_id = Column(String, ForeignKey("gw2_pro_profession.id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("gw2_pro_skill.id"), primary_key=True)


class _Gw2BundleSkill(Base):
    __tablename__ = "gw2_pro_skill_bundle_skill_rel"

    skill_id = Column(Integer, ForeignKey("gw2_pro_skill.id"), primary_key=True)
    bundle_id = Column(Integer, ForeignKey("gw2_pro_skill.id"), primary_key=True)


class _Gw2TransformSkill(Base):
    __tablename__ = "gw2_pro_skill_transform_skill_rel"

    skill_id = Column(Integer, ForeignKey("gw2_pro_skill.id"), primary_key=True)
    trans_id = Column(Integer, ForeignKey("gw2_pro_skill.id"), primary_key=True)


class Gw2Skill(Base):
    """Map the skills endpoint

    This class gives access to v2/skills enpoint.
    For more informations about this endpoint, see:
        - https://wiki.guildwars2.com/wiki/API:2/skills
        - https://github.com/arenanet/api-cdi/blob/master/v2/skills/skills.js

    This endpoint shows information about skills
    """
    __tablename__ = "gw2_pro_skill"
    __table_args__ = endpoint_def('skills', locale=True)

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    icon = Column(String, nullable=False)
    chat_link = Column(String, nullable=False)
    type = Column(String, nullable=False)
    weapon_type = Column(String, nullable=False)
    slot = Column(String, nullable=False)
    flags = Column(String, nullable=True)
    attunement = Column(String, nullable=True)
    cost = Column(Integer, nullable=True)
    categories = Column(String, nullable=True)
    initiative = Column(Integer, nullable=True)
    dual_wield = Column(String, nullable=True)
    flip_skill = Column(Integer, ForeignKey("gw2_pro_skill.id"), nullable=True)
    next_chain = Column(Integer, ForeignKey("gw2_pro_skill.id"), nullable=True)
    prev_chain = Column(Integer, ForeignKey("gw2_pro_skill.id"), nullable=True)
    toolbelt_skill = Column(Integer, ForeignKey("gw2_pro_skill.id"), nullable=True)

    professions = relationship("Gw2Profession",
                               secondary="gw2_pro_profession_skill_rel",
                               uselist=True,
                               info=rel_json(_Gw2ProfSkill,
                                             fn=lambda j, pj: [dict(skill_id=pj['id'], prof_id=x) for x in j]))

    flip = relationship("Gw2Skill", foreign_keys=[flip_skill], remote_side=[id], uselist=False)

    next = relationship("Gw2Skill", foreign_keys=[next_chain], remote_side=[id], uselist=False)

    facts = relationship("Gw2Fact",
                         primaryjoin="Gw2Skill.id == Gw2Fact.skill_id and Gw2Fact.requires_trait == None",
                         uselist=True,
                         info=rel_json(Gw2Fact,
                                       fn=lambda j, pj: [dict(skill_id=pj['id'], is_traited=False, ord=i, **x) for i, x in enumerate(j)]))

    traited_facts = relationship("Gw2Fact",
                                 primaryjoin="Gw2Skill.id == Gw2Fact.skill_id and Gw2Fact.requires_trait != None",
                                 uselist=True,
                                 info=rel_json(Gw2Fact,
                                               fn=lambda j, pj: [dict(skill_id=pj['id'], is_traited=True, ord=i, **x) for i, x in enumerate(j)]))

    bundle_skills = relationship("Gw2Skill",
                                 secondary="gw2_pro_skill_bundle_skill_rel",
                                 primaryjoin="_Gw2BundleSkill.skill_id == Gw2Skill.id",
                                 secondaryjoin="_Gw2BundleSkill.bundle_id == Gw2Skill.id",
                                 uselist=True,
                                 info=rel_json(_Gw2BundleSkill,
                                               fn=lambda j, pj: [dict(skill_id=pj['id'], bundle_id=x) for x in list(set(j))]))

    transform_skills = relationship("Gw2Skill",
                                    secondary="gw2_pro_skill_transform_skill_rel",
                                    primaryjoin="_Gw2TransformSkill.skill_id == Gw2Skill.id",
                                    secondaryjoin="_Gw2TransformSkill.trans_id == Gw2Skill.id",
                                    uselist=True,
                                    info=rel_json(_Gw2TransformSkill,
                                                  fn=lambda j, pj: [dict(skill_id=pj['id'], trans_id=x) for x in list(set(j))]))

    toolbelt = relationship("Gw2Skill",
                            foreign_keys=[toolbelt_skill],
                            remote_side=[id],
                            uselist=False)

    Gw2Fact.skill_id.append_foreign_key(ForeignKey("gw2_pro_skill.id"))
