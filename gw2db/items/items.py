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

"""skins enpoint mapping

This module gives access to v2/skins enpoint.
For more informations about this endpoint, see:
    <https://wiki.guildwars2.com/wiki/API:2/items>
    <https://github.com/arenanet/api-cdi/blob/master/v2/items.js>
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship

from gw2db.common import Base, endpoint_def, rel_json, col_json


class _Gw2ItemItemStat(Base):
    __tablename__ = "gw2_item_item_item_stat_rel"

    # Columns
    item_id = Column(Integer, ForeignKey("gw2_item_item.id"), primary_key=True)
    stat_id = Column(Integer, ForeignKey("gw2_item_item_stat.id"), primary_key=True)


class _Gw2InfixUpgrade(Base):
    __tablename__ = "gw2_item_item_infix_upgrade"

    # Columns
    pkid = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("gw2_item_item.id"), nullable=False)

    buff_skill_id = Column(Integer, info=col_json(keys=['buff', 'skill_id']), nullable=True)
    buff_description = Column(Integer, info=col_json(keys=['buff', 'description']), nullable=True)

    boon_duration = Column(Integer, nullable=False, default=0, info=col_json(keys='BoonDuration'))
    condition_damage = Column(Integer, nullable=False, default=0, info=col_json(keys='ConditionDamage'))
    condition_duration = Column(Integer, nullable=False, default=0, info=col_json(keys='ConditionDuration'))
    crit_damage = Column(Integer, nullable=False, default=0, info=col_json(keys='CritDamage'))
    healing = Column(Integer, nullable=False, default=0, info=col_json(keys='Healing'))
    power = Column(Integer, nullable=False, default=0, info=col_json(keys='Power'))
    precision = Column(Integer, nullable=False, default=0, info=col_json(keys='Precision'))
    thoughness = Column(Integer, nullable=False, default=0, info=col_json(keys='Thoughness'))
    vitality = Column(Integer, nullable=False, default=0, info=col_json(keys='Vitality'))


class _Gw2InfusionSlot(Base):
    __tablename__ = "gw2_item_item_infusion"

    # Columns
    pkid = Column(Integer, primary_key=True)
    item = Column(Integer, ForeignKey("gw2_item_item.id"), nullable=False)
    flags = Column(String, nullable=False)
    infusion_id = Column(Integer, ForeignKey("gw2_item_item.id"), nullable=True, info=col_json(keys='item_id'))

    # Relations
    infusion = relationship("Gw2Item", foreign_keys=[infusion_id], uselist=False)


class Gw2Item(Base):
    """Map the items endpoint

    This endpoint shows information about items
    """
    __tablename__ = "gw2_item_item"
    __table_args__ = endpoint_def('items', locale=True, workers=20)

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    chat_link = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    description = Column(String)
    type = Column(String, nullable=False)
    rarity = Column(String, nullable=False)
    level = Column(Integer, nullable=False)
    vendor_value = Column(Integer, nullable=False)
    default_skin = Column(Integer, ForeignKey("gw2_item_skin.id"), nullable=True)
    flags = Column(Integer, nullable=True)
    game_types = Column(String, nullable=True)
    restrictions = Column(String, nullable=True)

    # Relations
    skin = relationship("Gw2Skin", uselist=False)

    recipe = relationship("Gw2Recipe",
                          primaryjoin="Gw2Recipe.output_item_id == Gw2Item.id",
                          uselist=False)

    material = relationship("Gw2Material",
                            secondary="gw2_item_material_item_rel",
                            uselist=False)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'Trophy'
    }


class Gw2ArmorItem(Gw2Item):
    """Map the item armors details endpoint

    This endpoint shows information about armors
    """
    __tablename__ = "gw2_item_item_armor"

    # Columns
    id = Column(Integer, ForeignKey("gw2_item_item.id"), primary_key=True)
    armor_type = Column(String, nullable=False, info=col_json(keys=['details', 'type']))
    weight_class = Column(String, nullable=False, info=col_json(keys=['details', 'weight_class']))
    defense = Column(Integer, nullable=False, info=col_json(keys=['details', 'defense']))
    suffix_item_id = Column(Integer, ForeignKey("gw2_item_item.id"), nullable=True,
                            info=col_json(keys=['details', 'suffix_item_id']))
    secondary_suffix_item_id = Column(Integer, ForeignKey("gw2_item_item.id"),
                                      nullable=True, info=col_json(keys=['details', 'secondary_suffix_item_id']))

    # Relations
    suffix_item = relationship("Gw2Item",
                               foreign_keys=[suffix_item_id], remote_side=[Gw2Item.id],
                               uselist=False)
    secondary_suffix_item = relationship("Gw2Item",
                                         foreign_keys=[secondary_suffix_item_id], remote_side=[Gw2Item.id],
                                         uselist=False)

    infusion_slots = relationship("_Gw2InfusionSlot",
                                  primaryjoin="_Gw2InfusionSlot.item == Gw2Item.id",
                                  uselist=True,
                                  info=rel_json(_Gw2InfusionSlot,
                                                keys=['details', 'infusion_slots'],
                                                fn=lambda j, pj: [dict(item=pj['id'], **x) for x in j]))

    infix_upgrade = relationship("_Gw2InfixUpgrade", uselist=False,
                                 info=rel_json(_Gw2InfixUpgrade,
                                               keys=['details', 'infix_upgrade'],
                                               fn=lambda j, pj: [dict(item_id=pj['id'],
                                                                      buff=j['buff'] if 'buff' in j else {},
                                                                      **{x['attribute']: x['modifier'] for x in j['attributes']})]))

    stat_choices = relationship("Gw2Itemstat",
                                secondary="gw2_item_item_item_stat_rel",
                                primaryjoin="Gw2ArmorItem.id == _Gw2ItemItemStat.item_id",
                                uselist=True,
                                info=rel_json(_Gw2ItemItemStat,
                                              keys=['details', 'stat_choices'],
                                              fn=lambda j, pj: [dict(item_id=pj['id'], stat_id=x) for x in j]))

    __mapper_args__ = dict(
        polymorphic_identity='Armor',
        inherit_condition=(id == Gw2Item.id)
    )


class Gw2BackItem(Gw2Item):
    """Map the item backs details subobject

    This endpoint shows information about backs
    """
    __tablename__ = "gw2_item_item_back"

    # Columns
    id = Column(Integer, ForeignKey("gw2_item_item.id"), primary_key=True)
    suffix_item_id = Column(Integer, ForeignKey("gw2_item_item.id"), nullable=True,
                            info=col_json(keys=['details', 'suffix_item_id']))
    secondary_suffix_item_id = Column(Integer, ForeignKey("gw2_item_item.id"), nullable=True,
                                      info=col_json(keys=['details', 'secondary_suffix_item_id']))

    # Relations
    suffix_item = relationship("Gw2Item",
                               foreign_keys=[suffix_item_id], remote_side=[Gw2Item.id],
                               uselist=False)
    secondary_suffix_item = relationship("Gw2Item",
                                         foreign_keys=[secondary_suffix_item_id], remote_side=[Gw2Item.id],
                                         uselist=False)

    infusion_slots = relationship("_Gw2InfusionSlot",
                                  primaryjoin="_Gw2InfusionSlot.item == Gw2Item.id",
                                  uselist=True,
                                  info=rel_json(_Gw2InfusionSlot,
                                                keys=['details', 'infusion_slots'],
                                                fn=lambda j, pj: [dict(item=pj['id'], **x) for x in j]))

    infix_upgrade = relationship("_Gw2InfixUpgrade", uselist=False,
                                 info=rel_json(_Gw2InfixUpgrade,
                                               keys=['details', 'infix_upgrade'],
                                               fn=lambda j, pj: [dict(item_id=pj['id'],
                                                                      buff=j['buff'] if 'buff' in j else {},
                                                                      **{x['attribute']: x['modifier'] for x in j['attributes']})]))

    stat_choices = relationship("Gw2Itemstat",
                                secondary="gw2_item_item_item_stat_rel",
                                primaryjoin="Gw2BackItem.id == _Gw2ItemItemStat.item_id",
                                uselist=True,
                                info=rel_json(_Gw2ItemItemStat,
                                              keys=['details', 'stat_choices'],
                                              fn=lambda j, pj: [dict(item_id=pj['id'], stat_id=x) for x in j]))

    __mapper_args__ = dict(
        polymorphic_identity='Back',
        inherit_condition=(id == Gw2Item.id)
    )


class Gw2BagItem(Gw2Item):
    """Map the item bags details endpoint

    This endpoint shows information about bags
    """
    __tablename__ = "gw2_item_item_bag"

    # Columns
    id = Column(Integer, ForeignKey("gw2_item_item.id"), primary_key=True)
    size = Column(Integer, nullable=False, info=col_json(keys=['details', 'size']))
    no_sell_or_sort = Column(Boolean, nullable=False, info=col_json(keys=['details', 'no_sell_or_sort']))

    __mapper_args__ = {'polymorphic_identity': 'Bag'}


class _Gw2ConsumableItemSkin(Base):
    __tablename__ = "gw2_item_item_consumable_skin"

    # Columns
    conso_id = Column(Integer, ForeignKey("gw2_item_item_consumable.id"), primary_key=True)
    skin_id = Column(Integer, ForeignKey("gw2_item_skin.id"), primary_key=True)


class Gw2ConsumableItem(Gw2Item):
    """Map the item consumables details endpoint

    This endpoint shows information about consumables
    """
    __tablename__ = "gw2_item_item_consumable"

    # Columns
    id = Column(Integer, ForeignKey("gw2_item_item.id"), primary_key=True)
    conso_type = Column(String, nullable=False, info=col_json(keys=['details', 'type']))
    conso_name = Column(String, nullable=True, info=col_json(keys=['details', 'name']))
    conso_description = Column(String, nullable=True, info=col_json(keys=['details', 'description']))
    duration_ms = Column(Integer, nullable=True, info=col_json(keys=['details', 'duration_ms']))
    unlock_type = Column(String, nullable=True, info=col_json(keys=['details', 'unlock_type']))
    color_id = Column(Integer, ForeignKey("gw2_item_dye.id"), nullable=True, info=col_json(keys=['details', 'color_id']))
    recipe_id = Column(Integer, ForeignKey("gw2_item_recipe.id"), nullable=True, info=col_json(keys=['details', 'type']))
    apply_count = Column(Integer, nullable=True, info=col_json(keys=['details', 'apply_count']))
    conso_icon = Column(Integer, nullable=True, info=col_json(keys=['details', 'icon']))

    # Relations
    dye = relationship("Gw2Dye", uselist=False)

    skins = relationship("Gw2Skin",
                         secondary="gw2_item_item_consumable_skin",
                         uselist=True,
                         info=rel_json(_Gw2ConsumableItemSkin,
                                       keys=['details', 'skins'],
                                       fn=lambda j, pj: [dict(conso_id=pj['id'], skin_id=x) for x in j]))

    __mapper_args__ = {'polymorphic_identity': 'Consumable'}


class Gw2ContainerItem(Gw2Item):
    """Map the item containers details endpoint

    This endpoint shows information about containers
    """
    __tablename__ = "gw2_item_item_container"

    # Columns
    id = Column(Integer, ForeignKey("gw2_item_item.id"), primary_key=True)
    cont_type = Column(String, nullable=False, info=col_json(keys=['details', 'type']))

    __mapper_args__ = {'polymorphic_identity': 'Container'}


class Gw2CraftingMaterialItem(Gw2Item):
    """Map the item crafting materials details subobject

    This endpoint shows information about crafting materials
    """
    __tablename__ = "gw2_item_item_cm"

    # Columns
    id = Column(Integer, ForeignKey("gw2_item_item.id"), primary_key=True)

    __mapper_args__ = {'polymorphic_identity': 'CraftingMaterial'}


class Gw2GatheringItem(Gw2Item):
    """Map the item gatherings details subobject

    This endpoint shows information about gatherings
    """
    __tablename__ = "gw2_item_item_gathering"

    # Columns
    id = Column(Integer, ForeignKey("gw2_item_item.id"), primary_key=True)
    gath_type = Column(String, nullable=False, info=col_json(keys=['details', 'type']))

    __mapper_args__ = {'polymorphic_identity': 'Gathering'}


class Gw2GizmoItem(Gw2Item):
    """Map the item gizmos details subobject

    This endpoint shows information about gizmos
    """
    __tablename__ = "gw2_item_item_gizmo"

    # Columns
    id = Column(Integer, ForeignKey("gw2_item_item.id"), primary_key=True)
    gizmo_type = Column(String, nullable=False, info=col_json(keys=['details', 'type']))

    __mapper_args__ = {'polymorphic_identity': 'Gizmo'}


class Gw2MiniatureItem(Gw2Item):
    """Map the item minipets details subobject

    This endpoint shows information about minipets
    """
    __tablename__ = "gw2_item_item_miniature"
    __endpoint__ = ''

    # Columns
    id = Column(Integer, ForeignKey("gw2_item_item.id"), primary_key=True)
    minipet_id = Column(Integer, ForeignKey("gw2_item_minipet.id"), nullable=False, info=col_json(keys=['details', 'minipet_id']))

    # Relations
    minipet = relationship("Gw2MiniPet", foreign_keys=[minipet_id], uselist=False)

    __mapper_args__ = {'polymorphic_identity': 'MiniPet'}


class Gw2SalvageItem(Gw2Item):
    """Map the item salvages details subobject

    This endpoint shows information about salvages
    """
    __tablename__ = "gw2_item_item_salvage"

    # Columns
    id = Column(Integer, ForeignKey("gw2_item_item.id"), primary_key=True)
    charges = Column(Integer, nullable=False, info=col_json(keys=['details', 'charges']))

    __mapper_args__ = {'polymorphic_identity': 'Tool'}


class Gw2TraitItem(Gw2Item):
    """Map the item traits details subobject

    This endpoint shows information about traits
    """
    __tablename__ = "gw2_item_item_trait"

    # Columns
    id = Column(Integer, ForeignKey("gw2_item_item.id"), primary_key=True)

    __mapper_args__ = {'polymorphic_identity': 'Trait'}


class Gw2TrinketItem(Gw2Item):
    """Map the item trinkets details subobject

    This endpoint shows information about trinkets
    """
    __tablename__ = "gw2_item_item_trinket"
    __endpoint__ = ''

    # Columns
    id = Column(Integer, ForeignKey("gw2_item_item.id"), primary_key=True)
    trinket_type = Column(String, nullable=False, info=col_json(keys=['details', 'type']))
    suffix_item_id = Column(Integer, ForeignKey("gw2_item_item.id"), nullable=True,
                            info=col_json(keys=['details', 'suffix_item_id']))
    secondary_suffix_item_id = Column(Integer, ForeignKey("gw2_item_item.id"), nullable=True,
                                      info=col_json(keys=['details', 'secondary_suffix_item_id']))

    # Relations
    suffix_item = relationship("Gw2Item",
                               foreign_keys=[suffix_item_id],
                               remote_side=[Gw2Item.id],
                               uselist=False)

    secondary_suffix_item = relationship("Gw2Item",
                                         foreign_keys=[secondary_suffix_item_id],
                                         remote_side=[Gw2Item.id],
                                         uselist=False)

    infusion_slots = relationship("_Gw2InfusionSlot",
                                  primaryjoin="_Gw2InfusionSlot.item == Gw2Item.id",
                                  uselist=True,
                                  info=rel_json(_Gw2InfusionSlot,
                                                keys=['details', 'infusion_slots'],
                                                fn=lambda j, pj: [dict(item=pj['id'], **x) for x in j]))

    infix_upgrade = relationship("_Gw2InfixUpgrade", uselist=False,
                                 info=rel_json(_Gw2InfixUpgrade,
                                               keys=['details', 'infix_upgrade'],
                                               fn=lambda j, pj: [dict(item_id=pj['id'],
                                                                      buff=j['buff'] if 'buff' in j else {},
                                                                      **{x['attribute']: x['modifier'] for x in j['attributes']})]))

    stat_choices = relationship("Gw2Itemstat",
                                secondary="gw2_item_item_item_stat_rel",
                                uselist=True,
                                info=rel_json(_Gw2ItemItemStat,
                                              keys=['details', 'stat_choices'],
                                              fn=lambda j, pj: [dict(item_id=pj['id'], stat_id=x) for x in j]))

    __mapper_args__ = dict(
        polymorphic_identity='Trinket',
        inherit_condition=(id == Gw2Item.id)
    )


class Gw2UpgradeItem(Gw2Item):
    """Map the item upgrades details subobject

    This endpoint shows information about upgrades
    """
    __tablename__ = "gw2_item_item_upgrade"

    # Columns
    id = Column(Integer, ForeignKey("gw2_item_item.id"), primary_key=True)
    upgrade_type = Column(String, nullable=False, info=col_json(keys=['details', 'type']))
    upgrade_flags = Column(String, nullable=True, info=col_json(keys=['details', 'flags']))
    suffix = Column(String, nullable=True, info=col_json(keys=['details', 'suffix']))
    bonuses = Column(String, nullable=True, info=col_json(keys=['details', 'bonuses']))
    infusion_upgrade_flags = Column(String, nullable=True, info=col_json(keys=['details', 'infusion_upgrade_flags']))

    # Relations
    infix_upgrade = relationship("_Gw2InfixUpgrade", uselist=False,
                                 info=rel_json(_Gw2InfixUpgrade,
                                               keys=['details', 'infix_upgrade'],
                                               fn=lambda j, pj: [dict(item_id=pj['id'],
                                                                      buff=j['buff'] if 'buff' in j else {},
                                                                      **{x['attribute']: x['modifier'] for x in j['attributes']})]))

    __mapper_args__ = dict(
        polymorphic_identity='UpgradeComponent',
        inherit_condition=(id == Gw2Item.id)
    )


class Gw2WeaponItem(Gw2Item):
    """Map the item weapons details subobject

    This endpoint shows information about weapons
    """
    __tablename__ = "gw2_item_item_weapon"

    # Columns
    id = Column(Integer, ForeignKey("gw2_item_item.id"), primary_key=True)
    weapon_type = Column(String, nullable=False, info=col_json(keys=['details', 'type']))
    damage_type = Column(String, nullable=False, info=col_json(keys=['details', 'damage_type']))
    min_power = Column(Integer, nullable=False, info=col_json(keys=['details', 'min_power']))
    max_power = Column(Integer, nullable=False, info=col_json(keys=['details', 'max_power']))
    defense = Column(Integer, nullable=False, info=col_json(keys=['details', 'defense']))
    suffix_item_id = Column(Integer, ForeignKey("gw2_item_item.id"), nullable=True,
                            info=col_json(keys=['details', 'suffix_item_id']))
    secondary_suffix_item_id = Column(Integer, ForeignKey("gw2_item_item.id"), nullable=True,
                                      info=col_json(keys=['details', 'secondary_suffix_item_id']))

    # Relations
    suffix_item = relationship("Gw2Item",
                               foreign_keys=[suffix_item_id],
                               remote_side=[Gw2Item.id],
                               uselist=False)

    secondary_suffix_item = relationship("Gw2Item",
                                         foreign_keys=[secondary_suffix_item_id],
                                         remote_side=[Gw2Item.id],
                                         uselist=False)

    infusion_slots = relationship("_Gw2InfusionSlot",
                                  primaryjoin="_Gw2InfusionSlot.item == Gw2Item.id",
                                  uselist=True,
                                  info=rel_json(_Gw2InfusionSlot,
                                                keys=['details', 'infusion_slots'],
                                                fn=lambda j, pj: [dict(item=pj['id'], **x) for x in j]))

    infix_upgrade = relationship("_Gw2InfixUpgrade", uselist=False,
                                 info=rel_json(_Gw2InfixUpgrade,
                                               keys=['details', 'infix_upgrade'],
                                               fn=lambda j, pj: [dict(item_id=pj['id'],
                                                                      buff=j['buff'] if 'buff' in j else {},
                                                                      **{x['attribute']: x['modifier'] for x in j['attributes']})]))

    stat_choices = relationship("Gw2Itemstat",
                                secondary="gw2_item_item_item_stat_rel",
                                uselist=True,
                                info=rel_json(_Gw2ItemItemStat,
                                              keys=['details', 'stat_choices'],
                                              fn=lambda j, pj: [dict(item_id=pj['id'], stat_id=x) for x in j]))

    __mapper_args__ = dict(
        polymorphic_identity='Weapon',
        inherit_condition=(id == Gw2Item.id)
    )
