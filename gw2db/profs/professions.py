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

"""professions enpoint mapping

This module gives access to v2/professions enpoint.
For more informations about this endpoint, see:
    <https://wiki.guildwars2.com/wiki/API:2/professions>
    <https://github.com/arenanet/api-cdi/blob/master/v2/professions.js>
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship

from gw2db.common import Base, endpoint_def, rel_json, col_json


class _Gw2TrainingTrack(Base):
    __tablename__ = "gw2_pro_training_track"

    train_id = Column(Integer, ForeignKey("gw2_pro_training.id"), primary_key=True)
    cost = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    skill_id = Column(Integer, ForeignKey("gw2_pro_skill.id"), nullable=True)
    trait_id = Column(Integer, ForeignKey("gw2_pro_trait.id"), nullable=True)

    skill = relationship("Gw2Skill", uselist=False)
    trait = relationship("Gw2Trait", uselist=False)


class _Gw2Training(Base):
    __tablename__ = "gw2_pro_training"

    id = Column(Integer, primary_key=True)
    profession = Column(String, ForeignKey("gw2_pro_profession.id"), primary_key=True)
    category = Column(String, nullable=False)
    name = Column(String, nullable=False)

    track = relationship("_Gw2TrainingTrack",
                         uselist=True,
                         info=rel_json(_Gw2TrainingTrack,
                                       fn=lambda j, pj: [dict(train_id=pj['id'], **x) for x in j]))


class _Gw2ProfWeaponSkill(Base):
    __tablename__ = "gw2_pro_profession_weapon_skill"

    prof_id = Column(Integer, ForeignKey("gw2_pro_profession.pkid"), primary_key=True)
    id = Column(Integer, ForeignKey("gw2_pro_skill.id"), primary_key=True)
    weapon = Column(String, ForeignKey("gw2_pro_profession_weapon.name"), primary_key=True)
    slot = Column(String, nullable=False)
    offhand = Column(String)
    attunement = Column(String)

    skill = relationship("Gw2Skill", uselist=False)


class _Gw2ProfWeapon(Base):
    __tablename__ = "gw2_pro_profession_weapon"

    prof_id = Column(Integer, ForeignKey("gw2_pro_profession.pkid"), primary_key=True)
    name = Column(String, primary_key=True)
    spec_id = Column(Integer, ForeignKey("gw2_pro_specialization.id"), nullable=True,
                     info=col_json(fn='specialization'))

    specialization = relationship("Gw2Specialization", uselist=False)
    skills = relationship("_Gw2ProfWeaponSkill",
                          uselist=True,
                          info=rel_json(_Gw2ProfWeaponSkill,
                                        fn=lambda j, pj: [dict(prof_id=pj['prof_id'], weapon=pj['name'], **x) for x in j]))


class Gw2Profession(Base):
    """Map the professions endpoint

    This endpoint shows information about professions
    """
    __tablename__ = "gw2_pro_profession"
    __table_args__ = endpoint_def('professions', locale=True, workers=1)

    pkid = Column(Integer, primary_key=True)
    id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    icon_big = Column(String, nullable=False)

    specializations = relationship("Gw2Specialization",
                                   uselist=True)
    training = relationship("_Gw2Training",
                            uselist=True,
                            info=rel_json(_Gw2Training,
                                          fn=lambda j, pj: [dict(profession=pj['id'], **x) for x in j]))

    weapons = relationship("_Gw2ProfWeapon",
                           uselist=True,
                           info=rel_json(_Gw2ProfWeapon,
                                         fn=lambda j, pj: [dict(prof_id=pj['id'], name=k, **v) for k, v in j.items()]))

    skills = relationship("Gw2Skill",
                          secondary="gw2_pro_profession_skill_rel",
                          uselist=True)
