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
from sqlalchemy import DateTime
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship

from gw2db.common import Base, endpoint_def, rel_json, col_json, EPType, gw2_to_orm_date


class Gw2Account(Base):
    """Map the account endpoint

    This class gives access to v2/account enpoint and its subendpoints.
    For more informations about these endpoints, see:
        - https://wiki.guildwars2.com/wiki/API:2/account and account/*
        - https://github.com/arenanet/api-cdi/tree/master/v2/account

    This endpoint shows the general informations of an account
    """
    __tablename__ = "gw2_auth_account"
    __table_args__ = endpoint_def('account', ep_type=EPType.sac, workers=1, rights=['account'], parent='Gw2Token')

    id = Column(String, primary_key=True)
    name = Column(String, primary_key=True)
    api_key = Column(String, ForeignKey("gw2_auth_token.api_key"), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    world_id = Column(Integer, ForeignKey("gw2_misc_world.id"), nullable=False, info=col_json('world'))
    created = Column(DateTime, nullable=False, info=col_json(keys='created', fn=gw2_to_orm_date))
    access = Column(String, nullable=False)
    commander = Column(Boolean, nullable=False)
    fractal_level = Column(Integer, nullable=True)
    daily_ap = Column(Integer, nullable=True)
    monthly_ap = Column(Integer, nullable=True)
    wvw_rank = Column(Integer, nullable=True)

    achievements = relationship("_Gw2AccountAchievement", uselist=True)
    bank = relationship("_Gw2AccountBank", uselist=True)
    dyes = relationship("Gw2Dye", secondary="gw2_auth_account_dye", uselist=True)
    finisher = relationship("_Gw2AccountFinisher", uselist=True)
    guilds = relationship("Gw2Guild", uselist=True)
    inventory = relationship("_Gw2AccountInventory", uselist=True)
    masteries = relationship("_Gw2AccountMastery", uselist=True)
    mini_pets = relationship("Gw2MiniPet", secondary="gw2_auth_account_mini", uselist=True)
    outfits = relationship("Gw2Outfit", secondary="gw2_auth_account_outfit", uselist=True)
    recipes = relationship("Gw2Recipe", secondary="gw2_auth_account_recipe", uselist=True)
    skins = relationship("Gw2Skin", secondary="gw2_auth_account_skin", uselist=True)
    titles = relationship("Gw2Title", secondary="gw2_auth_account_title", uselist=True)
    vault = relationship("_Gw2AccountVault", uselist=True)

    @staticmethod
    def merge_json(_json, parent, params):
        _json['_token_'] = parent

    @staticmethod
    def to_child(ch, key, _json):
        if len(set(ch.rights).intersection(_json['_token_']['permissions'])) == len(ch.rights):
            ch.set_params(key, _json)


class _Gw2AccountAchievement(Base):
    """Map the account/achievements endpoint

    This endpoint shows the informations about achievements of an account
    """
    __tablename__ = "gw2_auth_account_achievement"
    __table_args__ = endpoint_def('account/achievements', ep_type=EPType.sac, workers=1, rights=['account', 'progression'], parent='Gw2Token')

    id = Column(Integer, ForeignKey("gw2_misc_achievement.id"), primary_key=True)
    api_key = Column(String, ForeignKey("gw2_auth_account.api_key"), primary_key=True)
    current = Column(Integer, nullable=True)
    max = Column(Integer, nullable=True)
    done = Column(Boolean, nullable=False)
    repeated = Column(Integer, nullable=True)


class _Gw2AccountBankUpgrade(Base):
    __tablename__ = "gw2_auth_account_bank_upgrade"

    id = Column(Integer, ForeignKey("gw2_auth_account_bank.pkid"), primary_key=True)
    upgrade_id = Column(Integer, ForeignKey("gw2_item_item_upgrade.id"), primary_key=True)


class _Gw2AccountBankInfusion(Base):
    __tablename__ = "gw2_auth_account_bank_infusion"

    id = Column(Integer, ForeignKey("gw2_auth_account_bank.pkid"), primary_key=True)
    infusion_id = Column(Integer, ForeignKey("gw2_item_item_upgrade.id"), primary_key=True)


class _Gw2AccountBank(Base):
    """Map the account/bank endpoint

    This endpoint shows the stored items in the account bank
    """
    __tablename__ = "gw2_auth_account_bank"
    __table_args__ = endpoint_def('account/bank', ep_type=EPType.sac, workers=1, rights=['account', 'inventories'], parent='Gw2Token')

    pkid = Column(Integer, primary_key=True)
    id = Column(Integer, ForeignKey("gw2_item_item.id"), nullable=False)
    api_key = Column(String, ForeignKey("gw2_auth_account.api_key"), nullable=False)
    count = Column(Integer, nullable=False)
    skin_id = Column(Integer, ForeignKey("gw2_item_skin.id"), nullable=True, info=col_json(fn='skin'))
    binding = Column(String)
    bound_to = Column(String)
    charges = Column(Integer)

    item = relationship("Gw2Item", uselist=False)
    skin = relationship("Gw2Skin", uselist=False)

    upgrades = relationship("Gw2UpgradeItem",
                            secondary="gw2_auth_account_bank_upgrade",
                            uselist=True,
                            info=rel_json(_Gw2AccountBankUpgrade,
                                          fn=lambda j, pj: [dict(id=pj['pkid'], upgrade_id=x) for x in j]))

    infusions = relationship("Gw2UpgradeItem",
                             secondary="gw2_auth_account_bank_infusion",
                             uselist=True,
                             info=rel_json(_Gw2AccountBankUpgrade,
                                           fn=lambda j, pj: [dict(id=pj['pkid'], infusion_id=x) for x in j]))


class _Gw2AccountDye(Base):
    """Map the account/dyes endpoint

    This endpoint shows the informations about unlocked dyes of an account
    """
    __tablename__ = "gw2_auth_account_dye"
    __table_args__ = endpoint_def('account/dyes', ep_type=EPType.sac, workers=1, rights=['account', 'unlocks'], parent='Gw2Token')

    id = Column(Integer, ForeignKey("gw2_item_dye.id"), primary_key=True)
    api_key = Column(String, ForeignKey("gw2_auth_account.api_key"), primary_key=True)


class _Gw2AccountFinisher(Base):
    """Map the account/finishers endpoint

    This endpoint shows the informations about unlocked finishers of an account
    """
    __tablename__ = "gw2_auth_account_finisher"
    __table_args__ = endpoint_def('account/finishers', ep_type=EPType.sac, workers=1, rights=['account', 'unlocks'], parent='Gw2Token')

    id = Column(Integer, ForeignKey("gw2_misc_finisher.id"), primary_key=True)
    api_key = Column(String, ForeignKey("gw2_auth_account.api_key"), primary_key=True)
    permanent = Column(Boolean, nullable=False)
    quantity = Column(Integer, nullable=True)

    finisher = relationship("Gw2Finisher", uselist=False)


class _Gw2AccountInventory(Base):
    """Map the account/inventory endpoint

    This endpoint shows the stored items in the account shared inventory
    """
    __tablename__ = "gw2_auth_account_inventory"
    __table_args__ = endpoint_def('account/inventory', ep_type=EPType.sac, workers=1, rights=['account', 'inventories'], parent='Gw2Token')

    id = Column(Integer, ForeignKey("gw2_item_item.id"), primary_key=True)
    api_key = Column(String, ForeignKey("gw2_auth_account.api_key"), primary_key=True)
    count = Column(Integer, nullable=False)
    binding = Column(String)

    item = relationship("Gw2Item", uselist=False)


class _Gw2AccountMastery(Base):
    """Map the account/masteries endpoint

    This endpoint shows the informations about unlocked mastery points of an account
    """
    __tablename__ = "gw2_auth_account_mastery"
    __table_args__ = endpoint_def('account/masteries', ep_type=EPType.sac, workers=1, rights=['account', 'progression'], parent='Gw2Token')

    id = Column(Integer, ForeignKey("gw2_pro_mastery.id"), primary_key=True)
    api_key = Column(String, ForeignKey("gw2_auth_account.api_key"), primary_key=True)
    level = Column(Integer, nullable=False)

    mastery = relationship("Gw2Mastery", uselist=False)


class _Gw2AccountMini(Base):
    """Map the account/minis endpoint

    This endpoint shows the informations about unlocked minipets of an account
    """
    __tablename__ = "gw2_auth_account_mini"
    __table_args__ = endpoint_def('account/minis', ep_type=EPType.sac, workers=1, rights=['account', 'unlocks'], parent='Gw2Token')

    id = Column(Integer, ForeignKey("gw2_item_minipet.id"), primary_key=True)
    api_key = Column(String, ForeignKey("gw2_auth_account.api_key"), primary_key=True)


class _Gw2AccountOutfit(Base):
    """Map the account/outfits endpoint

    This endpoint shows the informations about unlocked outfits of an account
    """
    __tablename__ = "gw2_auth_account_outfit"
    __table_args__ = endpoint_def('account/outfits', ep_type=EPType.sac, workers=1, rights=['account', 'unlocks'], parent='Gw2Token')

    id = Column(Integer, ForeignKey("gw2_misc_outfit.id"), primary_key=True)
    api_key = Column(String, ForeignKey("gw2_auth_account.api_key"), primary_key=True)


class _Gw2AccountRecipe(Base):
    """Map the account/recipes endpoint

    This endpoint shows the informations about unlocked recipes of an account
    """
    __tablename__ = "gw2_auth_account_recipe"
    __table_args__ = endpoint_def('account/recipes', ep_type=EPType.sac, workers=1, rights=['account', 'unlocks'], parent='Gw2Token')

    id = Column(Integer, ForeignKey("gw2_item_recipe.id"), primary_key=True)
    api_key = Column(String, ForeignKey("gw2_auth_account.api_key"), primary_key=True)


class _Gw2AccountSkin(Base):
    """Map the account/skins endpoint

    This endpoint shows the informations about unlocked skins of an account
    """
    __tablename__ = "gw2_auth_account_skin"
    __table_args__ = endpoint_def('account/skins', ep_type=EPType.sac, workers=1, rights=['account', 'unlocks'], parent='Gw2Token')

    id = Column(Integer, ForeignKey("gw2_item_skin.id"), primary_key=True)
    api_key = Column(String, ForeignKey("gw2_auth_account.api_key"), primary_key=True)


class _Gw2AccountTitle(Base):
    """Map the account/titles endpoint

    This endpoint shows the informations about unlocked titles of an account
    """
    __tablename__ = "gw2_auth_account_title"
    __table_args__ = endpoint_def('account/titles', ep_type=EPType.sac, workers=1, rights=['account', 'unlocks'], parent='Gw2Token')

    id = Column(Integer, ForeignKey("gw2_misc_title.id"), primary_key=True)
    api_key = Column(String, ForeignKey("gw2_auth_account.api_key"), primary_key=True)


class _Gw2AccountVault(Base):
    """Map the account/materials endpoint

    This endpoint shows the stored items in the account vault
    """
    __tablename__ = "gw2_auth_account_vault"
    __table_args__ = endpoint_def('account/materials', ep_type=EPType.sac, workers=1, rights=['account', 'inventories'], parent='Gw2Token')

    id = Column(Integer, ForeignKey("gw2_item_item.id"), primary_key=True)
    api_key = Column(String, ForeignKey("gw2_auth_account.api_key"), primary_key=True)
    category = Column(Integer, ForeignKey("gw2_item_material.id"), nullable=False)
    count = Column(Integer, nullable=False)

    item = relationship("Gw2Item", uselist=False)
    material = relationship("Gw2Material", uselist=False)


class _Gw2AccountWallet(Base):
    """Map the account/materials endpoint

    This endpoint shows the amount of each currency owned by an account
    """
    __tablename__ = "gw2_auth_account_wallet"
    __table_args__ = endpoint_def('account/wallet', ep_type=EPType.sac, workers=1, rights=['account', 'wallet'], parent='Gw2Token')

    id = Column(Integer, ForeignKey("gw2_misc_currencies.id"), primary_key=True)
    api_key = Column(String, ForeignKey("gw2_auth_account.api_key"), primary_key=True)
    value = Column(Integer, nullable=False)

    currency = relationship("Gw2Currency", uselist=False)
