pyGw2Tools
===

This project is a set of off-game tools for [GuildWars 2](https://heartofthorns.guildwars2.com/), based on the [WebAPI](https://github.com/arenanet/api-cdi) provided by ArenaNet ([doc here](https://wiki.guildwars2.com/wiki/API:2)).

> **Warning:**
> This project development just starts, lots of feature are not implemented yet.

-----------------------


Licence
---
[![GPLv3](https://www.gnu.org/graphics/gplv3-127x51.png)](https://www.gnu.org/licenses/gpl.html)

------------------------


Features
---

| Feature | Status | Note |
| :----------- | :------: | :----------- |
| WebAPI access - local storage | dev | see ``gw2db`` |
| Plugin system for tools | *planned* | add your own tools! |
| Main GUI | *planned* | probably with Qt |
| Tool: character build maker | *planned* | create a build for a new / existing character |
| Tool: build compare | *planned* | compare two character builds |
| Tool: crafting recipe | *planned* | full missing ressources list to craft an object / multiples objects, with cost to buy them |
| Tool: world map | *maybe* | see the GW2 world map with all points of interests |
| your feature here soon? | [talk about it](https://github.com/zanar/pygw2tools/issues) | |


----------------

Requirements
---

This module is developped and tested with python 3.4 on Linux. Tell me your experience with this module to improve it!

> **Note:**
> Compatibility with python 2.x is not planned. It could work, but it would be fortuitous and I doubt about that.

Here is the list of 3rd party modules used within this project (for now):

| Module | Description |
| --- | --- |
| [Requests](docs.python-requests.org) | easy access to WebAPI endpoints |
| [SQLAlchemy](http://www.sqlalchemy.org/) | ORM access for SQLite data storage |
| [Tzlocal](https://pypi.python.org/pypi/tzlocal) | datetime localisation |
