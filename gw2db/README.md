pyGw2Tools - gw2db
===

This module downloads (a lots of) [**v2** WepAPI](https://api.guildwars2.com/v2) endpoints and store them into a SQLite database. It also gives access to this database through ORM.

> **Note:**
> This module is extractable from this project to be added to your own. It don't require others project modules.

> **Warning:**
> This project is still in development, some endpoints are not implemented yet.

> **Warning:**
> Some errors could be shown in datas. It could come from the WebAPI, still in development (too).

-----------------------


Licence
---
[![GPLv3](https://www.gnu.org/graphics/gplv3-127x51.png)](https://www.gnu.org/licenses/gpl.html)

------------------------


Features
---

### db manager
| Feature | Status | Note |
| :----------- | :------: | :----------- |
| unique manager instance | test | |
| create and connect db | test | |
| connect existing db | test | |
| close db | test | |
| get db current localization / generate localization for new | test | based on WebAPI, available languages are English, Frensh, Spanish and German
| check local vs WebAPI datas version | test | |
| load new datas | test | see ``endpoint manager`` |
| insert new datas | dev/test |  |
| run upgrade with backup | dev/test | |
| change db localization | *planned* | |
| graphical upgrade status | *planned* | probably through Qt |
| manage db corruption | *planned* | |

### endpoint manager
| Feature | Status | Note |
| :----------- | :------: | :----------- |
| create manager with mapper params | dev/test | |
| download datas | dev/test | |
| map datas | dev/test | see ``JSON / ORM mapping`` |
| manage sub-enpoints | dev/test | |
| download objects images | *planned* | each 'icon', 'background', ... for a faster / easier access |

### JSON / ORM mapping
| Feature | Status | Note |
| :----------- | :------: | :------ |
| **account related:**<br/> v2/account<br/> v2/account/achievements<br/> v2/account/bank<br/> v2/account/dyes<br/> v2/account/finishers<br/> v2/account/inventory<br/> v2/account/masteries<br/> v2/account/materials<br/> v2/account/minis<br/> v2/account/outfits<br/> v2/account/recipes<br/> v2/account/skins<br/> v2/account/titles<br/> v2/account/wallet<br/> v2/characters<br/> v2/guild/:id<br/> v2/tokeninfo | dev/test | these endpoints need authentication. see [ArenaNet Access Token](https://account.arena.net/applications). To use all project tools, create an access token with all rights |
| v2/characters/:id/heropoints<br/> v2/commerce/transactions<br/> v2/guild/:id/log<br/> v2/guild/:id/members<br/> v2/guild/:id/ranks<br/> v2/guild/:id/stash<br/> v2/guild/:id/teams<br/> v2/guild/:id/treasury<br/> v2/guild/:id/upgrades | *planned* | |
| v2/pvp/games<br/> v2/pvp/standings<br/> v2/pvp/stats | *maybe...* | |
| **items related:**<br/> v2/colors<br/> v2/guild/upgrades<br/> v2/items<br/> v2/itemstats<br/> v2/materials<br/> v2/minis<br/> v2/recipes<br/> v2/skins | dev/test | |
| v2/pvp/amulets<br/> | *maybe...* | |
| **professions related:**<br/> v2/legends<br/> v2/masteries<br/> v2/pets<br/> v2/professions<br/> v2/skills<br/> v2/specializations<br/> v2/traits | dev/test | |
| **story related:**<br/> v2/stories<br/> v2/stories/seasons<br/> v2/backstory/answer<br/> v2/backstory/question | dev/test | |
| **maps related:**<br/> v2/continents<br/> v2/maps | *planned* | only public access maps / all maps? |
| **commerce related:**<br/> v2/commerce/exchange <br/> v2/commerce/listings<br/> v2/commerce/prices | *planned* | won't be stored in db, only in session. Datas can change too fast... |
| **miscellaneous:**<br/> v2/achievements<br/> v2/achievements/categories<br/> v2/achievements/groups<br/> v2/currencies<br/> v2/emblem<br/> v2/finishers<br/> v2/outfits<br/> v2/titles<br/> v2/worlds | dev/test | |
| v2/achievements/daily<br/> v2/achievements/daily/tomorrow<br/> v2/guild/permissions | *planned* | |
| **PvP / WvW related:**<br/> v2/pvp<br/> v2/pvp/ranks<br/> v2/pvp/seasons<br/> v2/pvp/seasons/:id/leaderboards<br/> v2/pvp/seasons/:id/leaderboards/:board/:region<br/> v2/wvw/abilities<br/> v2/wvw/matches<br/> v2/wvw/matches/overview<br/> v2/wvw/matches/scores<br/> v2/wvw/matches/stats<br/> v2/wvw/objectives<br/> v2/wvw/ranks | *maybe* | |


----------------

Requirements
---

This module is developped and tested with python 3.4 on Linux. Tell us your experience with this module to improve it!

> **Note:**
> Compatibility with python 2.x is not planned. It could work, but it would be fortuitous and I doubt about that.

Here is the list of 3rd party modules used within this project (for now):

| Module | Description |
| --- | --- |
| [Requests](docs.python-requests.org) | easy access to WebAPI endpoints |
| [SQLAlchemy](http://www.sqlalchemy.org/) | ORM access for SQLite data storage |
| [Tzlocal](https://pypi.python.org/pypi/tzlocal) | datetime localisation |
