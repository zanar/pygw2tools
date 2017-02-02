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


class _Gw2RecipeIngredient(Base):
    """Store items ingredients for a recipe"""
    __tablename__ = "gw2_item_recipe_ingr"

    # Columns
    recipe_id = Column(Integer, ForeignKey("gw2_item_recipe.id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("gw2_item_item.id"), primary_key=True)
    count = Column(Integer, nullable=False)

    # Relations
    item = relationship("Gw2Item", uselist=False)


class _Gw2RecipeGUIngredient(Base):
    """Store guild upgrade ingredients for a recipe"""
    __tablename__ = "gw2_item_recipe_guild_up_ingr"

    # Columns
    recipe_id = Column(Integer, ForeignKey("gw2_item_recipe.id"), primary_key=True)
    upgrade_id = Column(Integer, ForeignKey("gw2_item_guild_upgrade.id"), primary_key=True)
    count = Column(Integer, nullable=False)

    # Relations
    guild_upgrade = relationship("Gw2GuildUpgrade", uselist=False)


class Gw2Recipe(Base):
    """Map the recipes endpoint

    This class gives access to v2/recipes enpoint.
    For more informations about this endpoint, see:
        - https://wiki.guildwars2.com/wiki/API:2/recipes
        - https://github.com/arenanet/api-cdi/blob/master/v2/recipes.js

    This endpoint shows information about recipes
    """
    __tablename__ = "gw2_item_recipe"
    __table_args__ = endpoint_def('recipes', workers=10)

    # Columns
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    output_item_id = Column(Integer, ForeignKey("gw2_item_item.id"), nullable=False)
    output_item_count = Column(Integer, nullable=False)
    output_upgrade_id = Column(Integer, ForeignKey("gw2_item_guild_upgrade.id"))
    time_to_craft_ms = Column(Integer, nullable=False)
    disciplines = Column(String)
    min_rating = Column(Integer, nullable=False)
    flags = Column(String)
    chat_link = Column(String, nullable=False)

    # Relations
    output_items = relationship("Gw2Item", uselist=False)
    output_upgrade = relationship("Gw2GuildUpgrade", uselist=False)

    ingredients = relationship("_Gw2RecipeIngredient",
                               uselist=True,
                               info=rel_json(_Gw2RecipeIngredient, fn=lambda j, pj: [dict(recipe_id=pj['id'], **x) for x in j]))

    guild_ingredients = relationship("_Gw2RecipeGUIngredient",
                                     uselist=True,
                                     info=rel_json(_Gw2RecipeGUIngredient, fn=lambda j, pj: [dict(recipe_id=pj['id'], **x) for x in j]))

    unlocker = relationship("Gw2ConsumableItem",
                            primaryjoin="Gw2ConsumableItem.recipe_id == Gw2Recipe.id",
                            uselist=False)
