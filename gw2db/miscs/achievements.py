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

from gw2db.common import Base, endpoint_def, rel_json, col_json


class _Gw2AchievementBit(Base):
    __tablename__ = "gw2_misc_achievement_bit"

    # Columns
    pkid = Column(Integer, primary_key=True)
    ach_id = Column(Integer, ForeignKey("gw2_misc_achievement.id"), nullable=False)
    type = Column(String, nullable=False)

    __mapper_args__ = {'polymorphic_on': type}


class _Gw2ABText(_Gw2AchievementBit):
    __tablename__ = "gw2_misc_achievement_bit_text"
    __mapper_args__ = {'polymorphic_identity': 'Text'}

    # Columns
    pkid = Column(Integer, ForeignKey("gw2_misc_achievement_bit.pkid"), primary_key=True)
    text = Column(String, nullable=False)


class _Gw2ABItem(_Gw2AchievementBit):
    __tablename__ = "gw2_misc_achievement_bit_item"
    __mapper_args__ = {'polymorphic_identity': 'Item'}

    # Columns
    pkid = Column(Integer, ForeignKey("gw2_misc_achievement_bit.pkid"), primary_key=True)
    item_id = Column(Integer, ForeignKey("gw2_item_item.id"), nullable=False, info=col_json(keys='id'))

    # Relations
    item = relationship("Gw2Item", uselist=False)


class _Gw2ABMinipet(_Gw2AchievementBit):
    __tablename__ = "gw2_misc_achievement_bit_minipet"
    __mapper_args__ = {'polymorphic_identity': 'Minipet'}

    # Columns
    pkid = Column(Integer, ForeignKey("gw2_misc_achievement_bit.pkid"), primary_key=True)
    minipet_id = Column(Integer, ForeignKey("gw2_item_minipet.id"), nullable=False, info=col_json(keys='id'))

    # Relations
    minipet = relationship("Gw2MiniPet", uselist=False)


class _Gw2ABSkin(_Gw2AchievementBit):
    __tablename__ = "gw2_misc_achievement_bit_skin"
    __mapper_args__ = {'polymorphic_identity': 'Skin'}

    # Columns
    pkid = Column(Integer, ForeignKey("gw2_misc_achievement_bit.pkid"), primary_key=True)
    skin_id = Column(Integer, ForeignKey("gw2_item_skin.id"), nullable=False, info=col_json(keys='id'))

    # Relations
    skin = relationship("Gw2Skin", uselist=False)


class _Gw2AchievementReward(Base):
    __tablename__ = "gw2_misc_achievement_reward"

    # Columns
    pkid = Column(Integer, primary_key=True)
    ach_id = Column(Integer, ForeignKey("gw2_misc_achievement.id"), nullable=False)
    type = Column(String, nullable=False)

    __mapper_args__ = {'polymorphic_on': type}


class _Gw2ARCash(_Gw2AchievementReward):
    __tablename__ = "gw2_misc_achievement_reward_cash"
    __mapper_args__ = {'polymorphic_identity': 'Coins'}

    # Columns
    pkid = Column(Integer, ForeignKey("gw2_misc_achievement_reward.pkid"), primary_key=True)
    count = Column(Integer, nullable=False)


class _Gw2ARItem(_Gw2AchievementReward):
    __tablename__ = "gw2_misc_achievement_reward_item"
    __mapper_args__ = {'polymorphic_identity': 'Item'}

    # Columns
    pkid = Column(Integer, ForeignKey("gw2_misc_achievement_reward.pkid"), primary_key=True)
    item_id = Column(Integer, ForeignKey("gw2_item_item.id"), nullable=False, info=col_json(keys='id'))
    count = Column(Integer, nullable=False)

    # Relations
    item = relationship("Gw2Item", uselist=False)


class _Gw2ARMastery(_Gw2AchievementReward):
    __tablename__ = "gw2_misc_achievement_reward_mastery"
    __mapper_args__ = {'polymorphic_identity': 'Mastery'}

    # Columns
    pkid = Column(Integer, ForeignKey("gw2_misc_achievement_reward.pkid"), primary_key=True)
    mastery_id = Column(Integer, ForeignKey("gw2_pro_mastery.id"), nullable=False, info=col_json(keys='id'))
    region = Column(String, nullable=False)

    # Relations
    mastery = relationship("Gw2Mastery", uselist=False)


class _Gw2ARTitle(_Gw2AchievementReward):
    __tablename__ = "gw2_misc_achievement_reward_title"
    __mapper_args__ = {'polymorphic_identity': 'Title'}

    # Columns
    pkid = Column(Integer, ForeignKey("gw2_misc_achievement_reward.pkid"), primary_key=True)
    title_id = Column(Integer, ForeignKey("gw2_misc_title.id"), nullable=False, info=col_json(keys='id'))

    # Relations
    title = relationship("Gw2Title", uselist=False)


class _Gw2AchievementTier(Base):
    __tablename__ = "gw2_misc_achievement_tier"

    # Columns
    pkid = Column(Integer, primary_key=True)
    ach_id = Column(Integer, ForeignKey("gw2_misc_achievement.id"), nullable=False)
    count = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)


class _Gw2AchievementRequires(Base):
    __tablename__ = "gw2_misc_achievement_req_rel"

    # Columns
    ach_id = Column(Integer, ForeignKey("gw2_misc_achievement.id"), primary_key=True)
    req_id = Column(Integer, ForeignKey("gw2_misc_achievement.id"), primary_key=True)


class Gw2Achievement(Base):
    """Map the achievements endpoint

    This class gives access to v2/achievements enpoint.
    For more informations about this endpoint, see:
        - https://wiki.guildwars2.com/wiki/API:2/achievements
        - https://github.com/arenanet/api-cdi/blob/master/v2/achievements/index.js

    This endpoint shows information about achievements
    """
    __tablename__ = "gw2_misc_achievement"
    __table_args__ = endpoint_def('achievements', locale=True)

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    icon = Column(String, default=None)
    requirement = Column(String, nullable=False)
    locked_text = Column(String, nullable=False)
    type = Column(String, nullable=False)
    flags = Column(String, nullable=True)
    point_cap = Column(Integer, nullable=True)

    # Relations
    tiers = relationship("_Gw2AchievementTier", uselist=True,
                         info=rel_json(_Gw2AchievementTier, fn=lambda j, pj: [dict(ach_id=pj['id'], **x) for x in j]))

    rewards = relationship("_Gw2AchievementReward", uselist=True,
                           info=rel_json(_Gw2AchievementReward, fn=lambda j, pj: [dict(ach_id=pj['id'], **x) for x in j]))

    bits = relationship("_Gw2AchievementBit", uselist=True,
                        info=rel_json(_Gw2AchievementBit, fn=lambda j, pj: [dict(ach_id=pj['id'], **x) for x in j]))

    prerequisites = relationship("Gw2Achievement",
                                 secondary="gw2_misc_achievement_req_rel",
                                 primaryjoin="_Gw2AchievementRequires.ach_id == Gw2Achievement.id",
                                 secondaryjoin="_Gw2AchievementRequires.req_id == Gw2Achievement.id",
                                 uselist=True,
                                 info=rel_json(_Gw2AchievementRequires,
                                               fn=lambda j, pj: [{'ach_id': pj['id'], 'req_id': x} for x in j]))


class _Gw2AchievementCategorization(Base):
    __tablename__ = "gw2_misc_achievement_category_rel"

    # Columns
    category_id = Column(Integer, ForeignKey("gw2_misc_achievement_category.id"), primary_key=True)
    achievement_id = Column(Integer, ForeignKey("gw2_misc_achievement.id"), primary_key=True)


class Gw2AchievementCategory(Base):
    """Map the achievements/categories endpoint

    This class gives access to v2/achievements/categories endpoint.
    For more informations about this endpoint, see:
        - https://wiki.guildwars2.com/wiki/API:2/achievements/categories
        - https://github.com/arenanet/api-cdi/blob/master/v2/achievements/categories.js

    This endpoint shows information about achievements categories
    """
    __tablename__ = "gw2_misc_achievement_category"
    __table_args__ = endpoint_def('achievements/categories', locale=True, workers=1)

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    order = Column(Integer, nullable=False)
    icon = Column(String, nullable=False)

    # Relations
    achievements = relationship("Gw2Achievement",
                                secondary="gw2_misc_achievement_category_rel",
                                uselist=True,
                                info=rel_json(_Gw2AchievementCategorization,
                                              fn=lambda j, pj: [dict(category_id=pj['id'], achievement_id=x) for x in list(set(j))]))


class _Gw2AchievementGrouping(Base):
    __tablename__ = "gw2_misc_achievement_group_rel"

    # Columns
    group_id = Column(String, ForeignKey("gw2_misc_achievement_group.id"), primary_key=True)
    category_id = Column(Integer, ForeignKey("gw2_misc_achievement_category.id"), primary_key=True)


class Gw2AchievementGroup(Base):
    """Map the achievements/groups endpoint

    This class gives access to v2/achievements/groups endpoint.
    For more informations about this endpoint, see:
        - https://wiki.guildwars2.com/wiki/API:2/achievements/groups
        - https://github.com/arenanet/api-cdi/blob/master/v2/achievements/groups.js

    This endpoint shows information about achievements groups
    """
    __tablename__ = "gw2_misc_achievement_group"
    __table_args__ = endpoint_def('achievements/groups', locale=True, workers=1)

    # Columns
    pkid = Column(Integer, primary_key=True)
    id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    order = Column(Integer, nullable=False)

    # Relations
    categories = relationship("Gw2AchievementCategory",
                              secondary="gw2_misc_achievement_group_rel",
                              uselist=True,
                              info=rel_json(_Gw2AchievementGrouping,
                                            fn=lambda j, pj: [dict(group_id=pj['id'], category_id=x) for x in j]))

