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
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship

from gw2db.common import Base, col_json


class Gw2Fact(Base):
    """Map the (traited) facts subobjects for skills and traits"""
    __tablename__ = "gw2_pro_fact"

    skill_id = Column(Integer, primary_key=True, default=0)
    trait_id = Column(Integer, primary_key=True, default=0)
    ord = Column(Integer, primary_key=True)
    is_traited = Column(Boolean, primary_key=True, default=False)
    text = Column(String, nullable=True)
    icon = Column(String, nullable=True)
    type = Column(String, nullable=False)

    # traited facts only
    requires_trait = Column(Integer, ForeignKey("gw2_pro_trait.id"), nullable=True)
    overrides = Column(Integer, nullable=True)

    requires = relationship("Gw2Trait", foreign_keys=[requires_trait], uselist=False)

    __mapper_args__ = {'polymorphic_on': type,
                       'polymorphic_identity': 'NoData'}


class _Gw2FactAttributeAdjust(Gw2Fact):
    __tablename__ = "gw2_pro_fact_aa"

    skill_id = Column(Integer, ForeignKey("gw2_pro_fact.skill_id"), primary_key=True, default=0)
    trait_id = Column(Integer, ForeignKey("gw2_pro_fact.trait_id"), primary_key=True, default=0)
    ord = Column(Integer, ForeignKey("gw2_pro_fact.ord"), primary_key=True)
    is_traited = Column(Boolean, ForeignKey("gw2_pro_fact.is_traited"), primary_key=True)
    value = Column(Integer, nullable=False, default=0)
    target = Column(String, nullable=False)

    __mapper_args__ = dict(
        polymorphic_identity='AttributeAdjust',
        inherit_condition=(skill_id == Gw2Fact.skill_id and
                           trait_id == Gw2Fact.trait_id and
                           ord == Gw2Fact.ord and
                           is_traited == Gw2Fact.is_traited)
    )


class _Gw2FactBuff(Gw2Fact):
    __tablename__ = "gw2_pro_fact_buff"

    skill_id = Column(Integer, ForeignKey("gw2_pro_fact.skill_id"), primary_key=True, default=0)
    trait_id = Column(Integer, ForeignKey("gw2_pro_fact.trait_id"), primary_key=True, default=0)
    ord = Column(Integer, ForeignKey("gw2_pro_fact.ord"), primary_key=True)
    is_traited = Column(Boolean, ForeignKey("gw2_pro_fact.is_traited"), primary_key=True)
    status = Column(String, nullable=True)
    description = Column(String, nullable=True)
    apply_count = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=True)

    __mapper_args__ = dict(
        polymorphic_identity='Buff',
        inherit_condition=(skill_id == Gw2Fact.skill_id and
                           trait_id == Gw2Fact.trait_id and
                           ord == Gw2Fact.ord and
                           is_traited == Gw2Fact.is_traited)
    )


class _Gw2FactBuffConversion(Gw2Fact):
    __tablename__ = "gw2_pro_fact_bc"

    skill_id = Column(Integer, ForeignKey("gw2_pro_fact.skill_id"), primary_key=True, default=0)
    trait_id = Column(Integer, ForeignKey("gw2_pro_fact.trait_id"), primary_key=True, default=0)
    ord = Column(Integer, ForeignKey("gw2_pro_fact.ord"), primary_key=True)
    is_traited = Column(Boolean, ForeignKey("gw2_pro_fact.is_traited"), primary_key=True)
    source = Column(String, nullable=False)
    percent = Column(Integer, nullable=False)
    target = Column(String, nullable=False)

    __mapper_args__ = dict(
        polymorphic_identity='BuffConversion',
        inherit_condition=(skill_id == Gw2Fact.skill_id and
                           trait_id == Gw2Fact.trait_id and
                           ord == Gw2Fact.ord and
                           is_traited == Gw2Fact.is_traited)
    )


class _Gw2FactComboField(Gw2Fact):
    __tablename__ = "gw2_pro_fact_cb"

    skill_id = Column(Integer, ForeignKey("gw2_pro_fact.skill_id"), primary_key=True, default=0)
    trait_id = Column(Integer, ForeignKey("gw2_pro_fact.trait_id"), primary_key=True, default=0)
    ord = Column(Integer, ForeignKey("gw2_pro_fact.ord"), primary_key=True)
    is_traited = Column(Boolean, ForeignKey("gw2_pro_fact.is_traited"), primary_key=True)
    field_type = Column(String, nullable=False)

    __mapper_args__ = dict(
        polymorphic_identity='ComboField',
        inherit_condition=(skill_id == Gw2Fact.skill_id and
                           trait_id == Gw2Fact.trait_id and
                           ord == Gw2Fact.ord and
                           is_traited == Gw2Fact.is_traited)
    )


class _Gw2FactComboFinisher(Gw2Fact):
    __tablename__ = "gw2_pro_fact_cf"

    skill_id = Column(Integer, ForeignKey("gw2_pro_fact.skill_id"), primary_key=True, default=0)
    trait_id = Column(Integer, ForeignKey("gw2_pro_fact.trait_id"), primary_key=True, default=0)
    ord = Column(Integer, ForeignKey("gw2_pro_fact.ord"), primary_key=True)
    is_traited = Column(Boolean, ForeignKey("gw2_pro_fact.is_traited"), primary_key=True)
    finisher_type = Column(String, nullable=False)
    percent = Column(Integer, nullable=False)

    __mapper_args__ = dict(
        polymorphic_identity='ComboFinisher',
        inherit_condition=(skill_id == Gw2Fact.skill_id and
                           trait_id == Gw2Fact.trait_id and
                           ord == Gw2Fact.ord and
                           is_traited == Gw2Fact.is_traited)
    )


class _Gw2FactDamage(Gw2Fact):
    __tablename__ = "gw2_pro_fact_damage"

    skill_id = Column(Integer, ForeignKey("gw2_pro_fact.skill_id"), primary_key=True, default=0)
    trait_id = Column(Integer, ForeignKey("gw2_pro_fact.trait_id"), primary_key=True, default=0)
    ord = Column(Integer, ForeignKey("gw2_pro_fact.ord"), primary_key=True)
    is_traited = Column(Boolean, ForeignKey("gw2_pro_fact.is_traited"), primary_key=True)
    hit_count = Column(String, nullable=False)
    dmg_multiplier = Column(Integer, nullable=False)

    __mapper_args__ = dict(
        polymorphic_identity='Damage',
        inherit_condition=(skill_id == Gw2Fact.skill_id and
                           trait_id == Gw2Fact.trait_id and
                           ord == Gw2Fact.ord and
                           is_traited == Gw2Fact.is_traited)
    )


class _Gw2FactDistance(Gw2Fact):
    __tablename__ = "gw2_pro_fact_dist"

    skill_id = Column(Integer, ForeignKey("gw2_pro_fact.skill_id"), primary_key=True, default=0)
    trait_id = Column(Integer, ForeignKey("gw2_pro_fact.trait_id"), primary_key=True, default=0)
    ord = Column(Integer, ForeignKey("gw2_pro_fact.ord"), primary_key=True)
    is_traited = Column(Boolean, ForeignKey("gw2_pro_fact.is_traited"), primary_key=True)
    distance = Column(Integer, nullable=False)

    __mapper_args__ = dict(
        polymorphic_identity='Distance',
        inherit_condition=(skill_id == Gw2Fact.skill_id and
                           trait_id == Gw2Fact.trait_id and
                           ord == Gw2Fact.ord and
                           is_traited == Gw2Fact.is_traited)
    )


class _Gw2FactDuration(Gw2Fact):
    __tablename__ = "gw2_pro_fact_dur"

    skill_id = Column(Integer, ForeignKey("gw2_pro_fact.skill_id"), primary_key=True, default=0)
    trait_id = Column(Integer, ForeignKey("gw2_pro_fact.trait_id"), primary_key=True, default=0)
    ord = Column(Integer, ForeignKey("gw2_pro_fact.ord"), primary_key=True)
    is_traited = Column(Boolean, ForeignKey("gw2_pro_fact.is_traited"), primary_key=True)
    duration = Column(Integer, nullable=False)

    __mapper_args__ = dict(
        polymorphic_identity='Duration',
        inherit_condition=(skill_id == Gw2Fact.skill_id and
                           trait_id == Gw2Fact.trait_id and
                           ord == Gw2Fact.ord and
                           is_traited == Gw2Fact.is_traited)
    )


class _Gw2FactHeal(Gw2Fact):
    __tablename__ = "gw2_pro_fact_heal"

    skill_id = Column(Integer, ForeignKey("gw2_pro_fact.skill_id"), primary_key=True, default=0)
    trait_id = Column(Integer, ForeignKey("gw2_pro_fact.trait_id"), primary_key=True, default=0)
    ord = Column(Integer, ForeignKey("gw2_pro_fact.ord"), primary_key=True)
    is_traited = Column(Boolean, ForeignKey("gw2_pro_fact.is_traited"), primary_key=True)
    hit_count = Column(Integer, nullable=False)

    __mapper_args__ = dict(
        polymorphic_identity='Heal',
        inherit_condition=(skill_id == Gw2Fact.skill_id and
                           trait_id == Gw2Fact.trait_id and
                           ord == Gw2Fact.ord and
                           is_traited == Gw2Fact.is_traited)
    )


class _Gw2FactHealingAdjust(Gw2Fact):
    __tablename__ = "gw2_pro_fact_ha"

    skill_id = Column(Integer, ForeignKey("gw2_pro_fact.skill_id"), primary_key=True, default=0)
    trait_id = Column(Integer, ForeignKey("gw2_pro_fact.trait_id"), primary_key=True, default=0)
    ord = Column(Integer, ForeignKey("gw2_pro_fact.ord"), primary_key=True)
    is_traited = Column(Boolean, ForeignKey("gw2_pro_fact.is_traited"), primary_key=True)
    hit_count = Column(Integer, nullable=False)

    __mapper_args__ = dict(
        polymorphic_identity='HealingAdjust',
        inherit_condition=(skill_id == Gw2Fact.skill_id and
                           trait_id == Gw2Fact.trait_id and
                           ord == Gw2Fact.ord and
                           is_traited == Gw2Fact.is_traited)
    )


class _Gw2FactNumber(Gw2Fact):
    __tablename__ = "gw2_pro_fact_number"

    skill_id = Column(Integer, ForeignKey("gw2_pro_fact.skill_id"), primary_key=True, default=0)
    trait_id = Column(Integer, ForeignKey("gw2_pro_fact.trait_id"), primary_key=True, default=0)
    ord = Column(Integer, ForeignKey("gw2_pro_fact.ord"), primary_key=True)
    is_traited = Column(Boolean, ForeignKey("gw2_pro_fact.is_traited"), primary_key=True)
    value = Column(Integer, nullable=False)

    __mapper_args__ = dict(
        polymorphic_identity='Number',
        inherit_condition=(skill_id == Gw2Fact.skill_id and
                           trait_id == Gw2Fact.trait_id and
                           ord == Gw2Fact.ord and
                           is_traited == Gw2Fact.is_traited)
    )


class _Gw2FactPercent(Gw2Fact):
    __tablename__ = "gw2_pro_fact_pc"

    skill_id = Column(Integer, ForeignKey("gw2_pro_fact.skill_id"), primary_key=True, default=0)
    trait_id = Column(Integer, ForeignKey("gw2_pro_fact.trait_id"), primary_key=True, default=0)
    ord = Column(Integer, ForeignKey("gw2_pro_fact.ord"), primary_key=True)
    is_traited = Column(Boolean, ForeignKey("gw2_pro_fact.is_traited"), primary_key=True)
    percent = Column(Integer, nullable=False)

    __mapper_args__ = dict(
        polymorphic_identity='Percent',
        inherit_condition=(skill_id == Gw2Fact.skill_id and
                           trait_id == Gw2Fact.trait_id and
                           ord == Gw2Fact.ord and
                           is_traited == Gw2Fact.is_traited)
    )


class _Gw2FactPrefixedBuff(Gw2Fact):
    __tablename__ = "gw2_pro_fact_pbuff"

    skill_id = Column(Integer, ForeignKey("gw2_pro_fact.skill_id"), primary_key=True, default=0)
    trait_id = Column(Integer, ForeignKey("gw2_pro_fact.trait_id"), primary_key=True, default=0)
    ord = Column(Integer, ForeignKey("gw2_pro_fact.ord"), primary_key=True)
    is_traited = Column(Boolean, ForeignKey("gw2_pro_fact.is_traited"), primary_key=True)
    status = Column(String, nullable=True)
    description = Column(String, nullable=True)
    apply_count = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=True)
    pre_text = Column(String, nullable=True, info=col_json(keys=['prefix', 'text']))
    pre_icon = Column(String, nullable=True, info=col_json(keys=['prefix', 'icon']))
    pre_status = Column(String, nullable=True, info=col_json(keys=['prefix', 'status']))
    pre_descr = Column(String, nullable=True, info=col_json(keys=['prefix', 'description']))

    __mapper_args__ = dict(
        polymorphic_identity='PrefixedBuff',
        inherit_condition=(skill_id == Gw2Fact.skill_id and
                           trait_id == Gw2Fact.trait_id and
                           ord == Gw2Fact.ord and
                           is_traited == Gw2Fact.is_traited)
    )


class _Gw2FactRadius(Gw2Fact):
    __tablename__ = "gw2_pro_fact_radius"

    skill_id = Column(Integer, ForeignKey("gw2_pro_fact.skill_id"), primary_key=True, default=0)
    trait_id = Column(Integer, ForeignKey("gw2_pro_fact.trait_id"), primary_key=True, default=0)
    ord = Column(Integer, ForeignKey("gw2_pro_fact.ord"), primary_key=True)
    is_traited = Column(Boolean, ForeignKey("gw2_pro_fact.is_traited"), primary_key=True)
    distance = Column(Integer, nullable=False)

    __mapper_args__ = dict(
        polymorphic_identity='Radius',
        inherit_condition=(skill_id == Gw2Fact.skill_id and
                           trait_id == Gw2Fact.trait_id and
                           ord == Gw2Fact.ord and
                           is_traited == Gw2Fact.is_traited)
    )


class _Gw2FactRange(Gw2Fact):
    __tablename__ = "gw2_pro_fact_range"

    skill_id = Column(Integer, ForeignKey("gw2_pro_fact.skill_id"), primary_key=True, default=0)
    trait_id = Column(Integer, ForeignKey("gw2_pro_fact.trait_id"), primary_key=True, default=0)
    ord = Column(Integer, ForeignKey("gw2_pro_fact.ord"), primary_key=True)
    is_traited = Column(Boolean, ForeignKey("gw2_pro_fact.is_traited"), primary_key=True)
    value = Column(Integer, nullable=False)

    __mapper_args__ = dict(
        polymorphic_identity='Range',
        inherit_condition=(skill_id == Gw2Fact.skill_id and
                           trait_id == Gw2Fact.trait_id and
                           ord == Gw2Fact.ord and
                           is_traited == Gw2Fact.is_traited)
    )


class _Gw2FactRecharge(Gw2Fact):
    __tablename__ = "gw2_pro_fact_reload"

    skill_id = Column(Integer, ForeignKey("gw2_pro_fact.skill_id"), primary_key=True, default=0)
    trait_id = Column(Integer, ForeignKey("gw2_pro_fact.trait_id"), primary_key=True, default=0)
    ord = Column(Integer, ForeignKey("gw2_pro_fact.ord"), primary_key=True)
    is_traited = Column(Boolean, ForeignKey("gw2_pro_fact.is_traited"), primary_key=True)
    value = Column(Integer, nullable=False)

    __mapper_args__ = dict(
        polymorphic_identity='Recharge',
        inherit_condition=(skill_id == Gw2Fact.skill_id and
                           trait_id == Gw2Fact.trait_id and
                           ord == Gw2Fact.ord and
                           is_traited == Gw2Fact.is_traited)
    )


class _Gw2FactTime(Gw2Fact):
    __tablename__ = "gw2_pro_fact_time"

    skill_id = Column(Integer, ForeignKey("gw2_pro_fact.skill_id"), primary_key=True, default=0)
    trait_id = Column(Integer, ForeignKey("gw2_pro_fact.trait_id"), primary_key=True, default=0)
    ord = Column(Integer, ForeignKey("gw2_pro_fact.ord"), primary_key=True)
    is_traited = Column(Boolean, ForeignKey("gw2_pro_fact.is_traited"), primary_key=True)
    duration = Column(Integer, nullable=False)

    __mapper_args__ = dict(
        polymorphic_identity='Time',
        inherit_condition=(skill_id == Gw2Fact.skill_id and
                           trait_id == Gw2Fact.trait_id and
                           ord == Gw2Fact.ord and
                           is_traited == Gw2Fact.is_traited)
    )


class _Gw2FactUnblockable(Gw2Fact):
    __tablename__ = "gw2_pro_fact_unbloc"

    skill_id = Column(Integer, ForeignKey("gw2_pro_fact.skill_id"), primary_key=True, default=0)
    trait_id = Column(Integer, ForeignKey("gw2_pro_fact.trait_id"), primary_key=True, default=0)
    ord = Column(Integer, ForeignKey("gw2_pro_fact.ord"), primary_key=True)
    is_traited = Column(Boolean, ForeignKey("gw2_pro_fact.is_traited"), primary_key=True)
    value = Column(Boolean, nullable=False)

    __mapper_args__ = dict(
        polymorphic_identity='Unblockable',
        inherit_condition=(skill_id == Gw2Fact.skill_id and
                           trait_id == Gw2Fact.trait_id and
                           ord == Gw2Fact.ord and
                           is_traited == Gw2Fact.is_traited)
    )
