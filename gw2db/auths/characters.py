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

"""characters endpoint mapping

This module gives access to v2/characters enpoint.
For more informations about this endpoint, see:
    <https://wiki.guildwars2.com/wiki/API:2/characters>
    <https://github.com/arenanet/api-cdi/blob/master/v2/characters/characters.js>
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship

from gw2db.common import Base, endpoint_def, rel_json, col_json, gw2_to_orm_date, EPType


class _Gw2CharacterBackStory(Base):
    """Store the character's backstory answers"""
    __tablename__ = "gw2_auth_character_backstory"

    char_id = Column(String, ForeignKey("gw2_auth_character.name"), primary_key=True)
    ans_id = Column(String, ForeignKey("gw2_sto_backstory_answer.id"), primary_key=True)


class _Gw2CharacterCraft(Base):
    """Store informations about character's crafting disciplines"""
    __tablename__ = "gw2_auth_character_craft"

    char_id = Column(String, ForeignKey("gw2_auth_character.name"), primary_key=True)
    discipline = Column(String, nullable=False, primary_key=True)
    rating = Column(Integer, nullable=False)
    active = Column(Boolean, nullable=False)


class _Gw2CharacterEquipmentInfusion(Base):
    __tablename__ = "gw2_auth_character_equipment_item_infusion_rel"

    pkid = Column(Integer, primary_key=True)
    eqp_id = Column(Integer, ForeignKey("gw2_auth_character_equipment.pkid"), nullable=False)
    infusion_id = Column(Integer, ForeignKey("gw2_item_item_upgrade.id"), nullable=False)


class _Gw2CharacterEquipmentUpgrade(Base):
    __tablename__ = "gw2_auth_character_equipment_item_upgrade_rel"

    pkid = Column(Integer, primary_key=True)
    eqp_id = Column(Integer, ForeignKey("gw2_auth_character_equipment.pkid"), nullable=False)
    upgrade_id = Column(Integer, ForeignKey("gw2_item_item_upgrade.id"), nullable=False)


class _Gw2CharacterEquipmentStat(Base):
    __tablename__ = "gw2_auth_character_equipment_stat"

    eqp_id = Column(Integer, ForeignKey("gw2_auth_character_equipment.pkid"), primary_key=True)
    id = Column(Integer, ForeignKey("gw2_item_item_stat.id"), nullable=False)
    power = Column(Integer, nullable=False, default=0, info=col_json(keys='Power'))
    precision = Column(Integer, nullable=False, default=0, info=col_json(keys='Precision'))
    toughness = Column(Integer, nullable=False, default=0, info=col_json(keys='Toughness'))
    vitality = Column(Integer, nullable=False, default=0, info=col_json(keys='Vitality'))
    condition_damage = Column(Integer, nullable=False, default=0, info=col_json(keys='ConditionDamage'))
    condition_duration = Column(Integer, nullable=False, default=0, info=col_json(keys='ConditionDuration'))
    healing = Column(Integer, nullable=False, default=0, info=col_json(keys='Healing'))
    boon_duration = Column(Integer, nullable=False, default=0, info=col_json(keys='BoonDuration'))


class _Gw2CharacterEquipment(Base):
    """Store the character's current equipment"""
    __tablename__ = "gw2_auth_character_equipment"

    pkid = Column(Integer, primary_key=True)
    char_id = Column(Integer, ForeignKey("gw2_auth_character.name"), nullable=False)
    slot = Column(String, nullable=False)
    id = Column(Integer, ForeignKey("gw2_item_item.id"), nullable=False)
    skin_id = Column(Integer, ForeignKey("gw2_item_skin.id"), nullable=True, info=col_json(keys='skin'))
    binding = Column(String, nullable=True)
    bound_to = Column(String, nullable=True)
    charges = Column(Integer, nullable=True)
    
    item = relationship("Gw2Item", foreign_keys=[id], uselist=False)
    skin = relationship("Gw2Skin", uselist=False)

    infusions = relationship("Gw2UpgradeItem",
                             secondary="gw2_auth_character_equipment_item_infusion_rel",
                             uselist=True,
                             info=rel_json(_Gw2CharacterEquipmentInfusion,
                                           fn=lambda j, pj: [dict(eqp_id=pj['pkid'], infusion_id=x) for x in j]))

    upgrades = relationship("Gw2UpgradeItem",
                            secondary="gw2_auth_character_equipment_item_upgrade_rel",
                            uselist=True,
                            info=rel_json(_Gw2CharacterEquipmentUpgrade,
                                          fn=lambda j, pj: [dict(eqp_id=pj['id'], upgrade_id=x) for x in j]))

    stats = relationship("_Gw2CharacterEquipmentStat",
                         uselist=False,
                         info=rel_json(_Gw2CharacterEquipmentStat,
                                       fn=lambda j, pj: dict(eqp_id=pj['id'], id=j['id'],
                                                             **(j['attributes'] if 'attributes' in j else {'aze': 'rty'}))))


class _Gw2CharacterInventoryInfusion(Base):
    __tablename__ = "gw2_auth_character_inventory_item_infusion_rel"

    pkid = Column(Integer, primary_key=True)
    inv_id = Column(String, ForeignKey("gw2_auth_character_inventory.pkid"), nullable=False)
    infusion_id = Column(Integer, ForeignKey("gw2_item_item_upgrade.id"), nullable=False)


class _Gw2CharacterInventoryUpgrade(Base):
    __tablename__ = "gw2_auth_character_inventory_item_upgrade_rel"

    pkid = Column(Integer, primary_key=True)
    inv_id = Column(String, ForeignKey("gw2_auth_character_inventory.pkid"), nullable=False)
    upgrade_id = Column(Integer, ForeignKey("gw2_item_item_upgrade.id"), nullable=False)


class _Gw2CharacterInventoryStat(Base):
    __tablename__ = "gw2_auth_character_inventory_stat"

    inv_id = Column(String, ForeignKey("gw2_auth_character_inventory.pkid"), primary_key=True)
    id = Column(Integer, ForeignKey("gw2_item_item_stat.id"), nullable=False)
    power = Column(Integer, nullable=False, default=0, info=col_json(keys='Power'))
    precision = Column(Integer, nullable=False, default=0, info=col_json(keys='Precision'))
    toughness = Column(Integer, nullable=False, default=0, info=col_json(keys='Toughness'))
    vitality = Column(Integer, nullable=False, default=0, info=col_json(keys='Vitality'))
    condition_damage = Column(Integer, nullable=False, default=0, info=col_json(keys='ConditionDamage'))
    condition_duration = Column(Integer, nullable=False, default=0, info=col_json(keys='ConditionDuration'))
    healing = Column(Integer, nullable=False, default=0, info=col_json(keys='Healing'))
    boon_duration = Column(Integer, nullable=False, default=0, info=col_json(keys='BoonDuration'))


class _Gw2CharacterInventory(Base):
    """Store the character's current inventory"""
    __tablename__ = "gw2_auth_character_inventory"

    pkid = Column(Integer, primary_key=True)
    char_id = Column(Integer, ForeignKey("gw2_auth_character.name"), primary_key=True)
    id = Column(Integer, ForeignKey("gw2_item_item.id"), nullable=False)
    skin_id = Column(Integer, ForeignKey("gw2_item_skin.id"), nullable=True, info=col_json(keys='skin'))
    binding = Column(String, nullable=True)
    bound_to = Column(String, nullable=True)
    charges = Column(Integer, nullable=True)
    
    item = relationship("Gw2Item", foreign_keys=[id], uselist=False)
    skin = relationship("Gw2Skin", uselist=False)
    
    infusions = relationship("Gw2UpgradeItem",
                             secondary="gw2_auth_character_inventory_item_infusion_rel",
                             uselist=True,
                             info=rel_json(_Gw2CharacterInventoryInfusion,
                                           fn=lambda j, pj: [dict(inv_id=pj['pkid'], infusion_id=x) for x in j]))

    upgrades = relationship("Gw2UpgradeItem",
                            secondary="gw2_auth_character_inventory_item_upgrade_rel",
                            uselist=True,
                            info=rel_json(_Gw2CharacterInventoryUpgrade,
                                          fn=lambda j, pj: [dict(inv_id=pj['pkid'], upgrade_id=x) for x in j]))
                                          
    stats = relationship("_Gw2CharacterInventoryStat",
                         uselist=False,
                         info=rel_json(_Gw2CharacterInventoryStat,
                                       fn=lambda j, pj: dict(inv_id=pj['pkid'],
                                                             id=j['id'],
                                                             **(j['attributes'] if 'attributes' in j else {'aze': 'rty'}))))


class _Gw2CharacterSkill(Base):
    """Store the character's currently selected skills"""
    __tablename__ = "gw2_auth_character_skill"

    char_id = Column(Integer, ForeignKey("gw2_auth_character.name"), primary_key=True)
    type = Column(String, primary_key=True)
    heal_id = Column(Integer, ForeignKey("gw2_pro_skill.id"), nullable=True, info=col_json(keys='heal'))
    util0_id = Column(Integer, ForeignKey("gw2_pro_skill.id"), nullable=True,
                      info=col_json(keys='utilities', fn=lambda j, pj: j[0] if len(j) > 0 else None))
    util1_id = Column(Integer, ForeignKey("gw2_pro_skill.id"), nullable=True,
                      info=col_json(keys='utilities', fn=lambda j, pj: j[1] if len(j) > 1 else None))
    util2_id = Column(Integer, ForeignKey("gw2_pro_skill.id"), nullable=True,
                      info=col_json(keys='utilities', fn=lambda j, pj: j[2] if len(j) > 2 else None))
    elite_id = Column(Integer, ForeignKey("gw2_pro_skill.id"), nullable=True,
                      info=col_json(keys='elite'))

    heal = relationship("Gw2Skill", foreign_keys=[heal_id], uselist=False)
    util0 = relationship("Gw2Skill", foreign_keys=[util0_id], uselist=False)
    util1 = relationship("Gw2Skill", foreign_keys=[util1_id], uselist=False)
    util2 = relationship("Gw2Skill", foreign_keys=[util2_id], uselist=False)
    elite = relationship("Gw2Skill", foreign_keys=[elite_id], uselist=False)


class _Gw2CharacterSpecialization(Base):
    """Store the character's currently selected specializations"""
    __tablename__ = "gw2_auth_character_spec"

    id = Column(Integer, ForeignKey("gw2_pro_specialization.id"), primary_key=True)
    type = Column(String, primary_key=True)
    char_id = Column(String, ForeignKey("gw2_auth_character.name"), primary_key=True)
    trait0_id = Column(Integer, ForeignKey("gw2_pro_trait.id"), nullable=True,
                       info=col_json(keys='traits', fn=lambda j, pj: j[0] if len(j) > 0 else None))
    trait1_id = Column(Integer, ForeignKey("gw2_pro_trait.id"), nullable=True,
                       info=col_json(keys='traits', fn=lambda j, pj: j[1] if len(j) > 1 else None))
    trait2_id = Column(Integer, ForeignKey("gw2_pro_trait.id"), nullable=True,
                       info=col_json(keys='traits', fn=lambda j, pj: j[2] if len(j) > 2 else None))

    specialization = relationship("Gw2Specialization", uselist=False)

    trait0 = relationship("Gw2Trait", foreign_keys=[trait0_id], uselist=False)
    trait1 = relationship("Gw2Trait", foreign_keys=[trait1_id], uselist=False)
    trait2 = relationship("Gw2Trait", foreign_keys=[trait2_id], uselist=False)


class _Gw2CharacterTrain(Base):
    """Store the character's current training"""
    __tablename__ = "gw2_auth_character_train"

    id = Column(Integer, ForeignKey("gw2_pro_training.id"), primary_key=True)
    char_id = Column(String, ForeignKey("gw2_auth_character.name"), primary_key=True)
    spent = Column(Integer, nullable=False)
    done = Column(Boolean, nullable=False)


class Gw2Character(Base):
    """Map the characters endpoint

    This endpoint shows the informations of a character
    """
    __tablename__ = "gw2_auth_character"
    __table_args__ = endpoint_def('characters', ep_type=EPType.ac, workers=3, rights=['characters'], parent='Gw2Token')

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    api_key = Column(String, ForeignKey("gw2_auth_token.api_key"), nullable=False)
    race = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    prof_id = Column(String, ForeignKey("gw2_pro_profession.id"), nullable=False, info=col_json(keys='profession'))
    level = Column(Integer, nullable=False)
    # guild_id = Column(Integer, ForeignKey("gw2_auth_guild.id"), nullable=True)
    age = Column(Integer, nullable=False)
    created = Column(DateTime, nullable=False, info=col_json(keys='created', fn=gw2_to_orm_date))
    deaths = Column(Integer, nullable=False)
    title_id = Column(Integer, ForeignKey("gw2_misc_title.id"), nullable=True, info=col_json(keys='title'))

    backstory = relationship("Gw2BackstoryAnswer",
                             secondary="gw2_auth_character_backstory",
                             uselist=True,
                             info=rel_json(_Gw2CharacterBackStory,
                                           fn=lambda j, pj: [dict(char_id=pj['name'], ans_id=x) for x in j]))
    crafting = relationship("_Gw2CharacterCraft",
                            uselist=True,
                            info=rel_json(_Gw2CharacterCraft,
                                          fn=lambda j, pj: [dict(char_id=pj['name'], **x) for x in j]))
    equipment = relationship("_Gw2CharacterEquipment", uselist=True,
                             info=rel_json(_Gw2CharacterEquipment,
                                           fn=lambda j, pj: [dict(char_id=pj['name'], **x) for x in j if x is not None]))
    # guild = relationship("Gw2Guild", uselist=False)
    inventory = relationship(
        "_Gw2CharacterInventory", uselist=True,
        info=rel_json(
            _Gw2CharacterInventory,
            keys='bags',
            fn=lambda j, pj: [dict(char_id=pj['name'], **inv) for bag in j if bag is not None for inv in bag['inventory'] if inv is not None]
        )
    )
    profession = relationship("Gw2Profession", uselist=False)
    skills = relationship("_Gw2CharacterSkill",
                          uselist=True,
                          info=rel_json(_Gw2CharacterSkill,
                                        fn=lambda j, pj: [dict(char_id=pj['name'], type=k, **v) for k, v in j.items()]))
    specializations = relationship(
        "_Gw2CharacterSpecialization", uselist=True,
        info=rel_json(
            _Gw2CharacterSpecialization,
            fn=lambda j, pj: [dict(char_id=pj['name'], type=k, **_v) for k, v in j.items() for _v in v if _v is not None]
        )
    )
    title = relationship("Gw2Title", uselist=False)
    training = relationship("_Gw2CharacterTrain", uselist=True,
                            info=rel_json(_Gw2CharacterTrain,
                                          fn=lambda j, pj: [dict(char_id=pj['name'], **x) for x in j]))
