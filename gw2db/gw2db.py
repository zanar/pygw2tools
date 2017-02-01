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

"""Package entry module.

This package provides the "master" class of this package: ``Gw2Db``.

"""

# std imports
import json
import locale
import os
import traceback
from enum import IntEnum, unique

# threading imports
from concurrent.futures import ThreadPoolExecutor, as_completed

# web imports
import requests
from requests import RequestException

# ORM imports
from sqlalchemy import event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Mapper, configure_mappers
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlite3 import Connection as SQLite3Connection

# package imports
from gw2db.common import Base, addr_v2, Gw2Endpoint, Param, EPType
from gw2db.tools import Singleton, CbEvent

from gw2db.auths import *
from gw2db.items import *
from gw2db.miscs import *
from gw2db.profs import *
from gw2db.story import *


# Event function called when db is connected
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    """Event function called when db is connected

    Set some parameters to the connection and the db to speed up exchanges.
    This function should never be called manually.

    :param dbapi_connection: the establised connection
    :param connection_record: unused parameter
    """
    if isinstance(dbapi_connection, SQLite3Connection):
        print('pragmas')
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode = MEMORY")
        cursor.execute("PRAGMA temp_store = MEMORY")
        cursor.execute("PRAGMA cache_size = -1000")
        cursor.execute("PRAGMA case_sensitive_like = 0")
        cursor.execute("PRAGMA encoding = \"UTF-8\"")
        cursor.close()


# Event fuction called when a table is mapped into db
@event.listens_for(Mapper, "mapper_configured")
def _on_table_mapped(mapper, class_):
    """Event fuction called when all declared tables are mapped into db

    Generate the list of tables which are linked to an endpoint.
    This function should never be called manually.

    :param mapper: unused parameter
    :param class_: the mapped class
    :return:
    """
    if len(class_.__table__.info) > 0 and class_ not in Gw2Db.__endpoints__:
        Gw2Db.__endpoints__.append(class_)


# Database upgrade status
@unique
class DbUpgradeStatus(IntEnum):
    """Database upgrade status

    Attributes:
        DbUpgradeStatus.started: the upgrade just started
        DbUpgradeStatus.downloading: the current datas are backed, starting retrieving new datas
         DbUpgradeStatus.success: the process ended with success, new datas are available
         DbUpgradeStatus.error: an error occured during process, the backed datas are restored
    """
    started = 1
    downloading = 2
    success = 3
    error = 4


# Endpoint upgrade status
@unique
class EndpointUpgradeStatus(IntEnum):
    """Endpoint upgrade status

    Attributes:
        EndpointUpgradeStatus.started: the endpoint upgrade started
        EndpointUpgradeStatus.downloading: the endpoint manager is downloading / mapping datas
        EndpointUpgradeStatus.commiting: all datas are mapped, starting to add them in base
        EndpointUpgradeStatus.success: the endpoint is upgraded successfully
        EndpointUpgradeStatus.error: an error occured, backed db must be restored
    """
    started = 1
    downloading = 2
    commiting = 3
    success = 4
    error = 5


# Package master class
class Gw2Db:
    """Package master class

    This class manage the database: access, upgrades... It's a singleton class, multipe instanciations return the
    same instance.

    Attributes:
        self.running_status: a callback event, showing the upgrade status
                             parameters are: <status (DbUpgradeStatus)>, <nb of endpoints (int)>

        self.endpoint_status: a callback event, showing an endpoint upgrade status
                              parameters are: <status (EndpointUpgradeStatus)>, <tablename (str)>

    Example:
        with Gw2Db() as db:
            my_datas db.session.query(...).filter(...).all()
            # do something with my_datas

    Warning:
        - All the gw2_* tables should be considered as "read-only".
        - The ``session`` object does NOT have autocommit. You MUST call ``session.commit()`` after any changes to save
          them. See <http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session> for more
          details about the session object.
    """
    __metaclass__ = Singleton
    
    __endpoints__ = list()
    
    def __init__(self):
        """Initialize the manager"""
        self.running_status = CbEvent()
        self.endpoint_status = CbEvent()
        
        self._db = 'gw2.db'
        self._back = self._db + '.back'
        
        self._engine = None
        self._session = None
        
        self._make_db()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.rollback()
        self._get_session()

    def __del__(self):
        self._close_db()

    @property
    def session(self):
        """Give access to the db session"""
        return self._get_session()

    @property
    def lang(self):
        """Get the db language or find it from system regarding the WebAPI available languages"""
        self._get_session()

        try:
            _lang = self._session.query(Param).filter(Param.name == 'lang').first().value
            return _lang
        except (SQLAlchemyError, AttributeError):
            _lang = locale.getdefaultlocale()[0].split('_')[0]
            if _lang not in ['fr', 'de', 'en', 'es']:
                _lang = 'en'
            self._session.add(Param(name='lang', value=_lang))
            self._session.commit()
            return _lang

    def _make_db(self):
        """Initialize the db engine and create a session"""
        self._engine = create_engine('sqlite:///' + self._db,
                                     connect_args={'check_same_thread': False},
                                     poolclass=StaticPool)
        Base.metadata.bind = self._engine
        Base.metadata.create_all()
        self._session = sessionmaker(bind=self._engine)(autoflush=False)
        configure_mappers()
        
    def _close_db(self):
        """Shut down the db engine and the opened session"""
        if self._session is not None:
            self._session.close_all()
            self._session = None
            
        if self._engine is not None:
            # self._engine.dispose()
            self._engine = None

    def _check_verions(self):
        """Compare the local datas version and the WebAPI exposed version

        :return: -1 on error, 0 if versions are equals, remote version if an upgrade is needed
        """
        try:
            ans = requests.get(addr_v2 + 'build', timeout=5)
            rv = json.loads(ans.text)['id']
        except RequestException:
            return -1

        lv = self._session.query(Param).filter(Param.name == 'build').first()
        if lv is not None:
            lv = int(lv.value)
        else:
            return rv
            
        return rv if rv > lv else 0

    def _fill_datas(self, lang, params):
        """Download, map and store all declared endpoints datas

        :param lang: the language to use as url argument
        :param params: current parameters stored in db, as dictionnary (k=name, v=value)
        :return: True on success, False on error
        """
        # TODO: start img dl
        
        keys = [v for k, v in params.items() if k.startswith('KEY_')]
        self.running_status(DbUpgradeStatus.downloading, len(Gw2Db.__endpoints__))
        
        import time
        st = time.time()

        chs = [x for x in Gw2Db.__endpoints__ if (x.__table__.info['ep_type'] & EPType.child) != 0]
        eps = [Gw2Endpoint(x, lang, chs) for x in Gw2Db.__endpoints__ if (x.__table__.info['ep_type'] & EPType.child) == 0]
        with ThreadPoolExecutor(max_workers=len(eps)) as mapper:
            ths = {}
            for ep in eps:
                ths[mapper.submit(ep.upgrade)] = ep
                self.endpoint_status(EndpointUpgradeStatus.downloading, ep.table_name)
                for key in keys:
                    ep.set_params(key=key)
                ep.set_params()

            def _on_error(_cls_):
                self.endpoint_status(EndpointUpgradeStatus.error, _cls_)
                for _ep_ in eps:
                    _ep_.on_error()
                return False

            ok = True
            for future in as_completed(ths):
                if future.exception() is not None:
                    traceback.print_exc()
                    ok = _on_error(ths[future].table_name)
                    continue
                if not ok:
                    continue

                ep = ths[future]
                datas = future.result()
                if datas is not None:
                    self.endpoint_status(EndpointUpgradeStatus.commiting, ep.table_name)
                    try:
                        for k, v in datas.items():
                            self._session.bulk_insert_mappings(k, v, return_defaults=True)
                            self._session.commit()
                    except SQLAlchemyError:
                        traceback.print_exc()
                        ok = _on_error(ep.table_name)
                        continue
                    self.endpoint_status(EndpointUpgradeStatus.success, ep.table_name)
                else:
                    ok = _on_error(ths[future].table_name)

        print('all dl: ', (time.time() - st))
        
        # TODO: end img dl
                            
        if not ok:
            self.running_status(DbUpgradeStatus.error, -1)
            return False
        return True

    def _get_session(self):
        """Give access to the opened session, or open a new one if needed

        :return: a session object
        """
        if self._engine is None:
            if self._session is None:
                self._make_db()
        elif self._session is None:
            self._session = sessionmaker(bind=self._engine)()

        return self._session

    def show_endpoints(self):
        """Give access to the defined endpoints

        :return: the list of found endpoints
        """
        eps = {cls.__name__: cls.__table__.info['endpoint'] for cls in Gw2Db.__endpoints__}
        return eps
            
    def upgrade(self, force=False):
        """Upgrade database if needed or requested

        This method check if an upgrade is needed and in this case, backs up the current datas, retreive new datas, store them
        then delete backed. If an error occurs, new datas are deleted and backed are restored.

        :param force: if True, force the upgrade even if it's not needed
        :return: -1 on error, 0 when upgrade is not needed, new version on success
        """
        self.running_status(DbUpgradeStatus.started, len(Gw2Db.__endpoints__))
        if force:
            self._get_session()
            p = self._session.query(Param).filter(Param.name == 'build').first()
            if p is not None:
                p.value = 0
                self._session.commit()

        nv = self._check_verions()
        if nv <= 0:
            return nv

        # backing params and db file
        lang = self.lang
        params = {x.name: x.value for x in self._session.query(Param).filter(Param.name != 'build').all()}

        self._close_db()
        if os.path.isfile(self._db):
            os.rename(self._db, self._back)
        
        # creating new db
        self._make_db()

        try:
            # reloading datas
            if self._fill_datas(lang, params) is False:
                raise NameError('An error occured while getting new datas')

            # saved, adding backed params and current build
            if len(params) > 0:
                self._session.add_all([Param(name=k, value=v) for k, v in params.items()])
            self._session.add(Param(name='build', value=str(nv)))
            self._session.commit()

            # all fine, deleting backup
            if os.path.isfile(self._back):
                os.remove(self._back)

            # let's go!
            ret = nv
            self.running_status(DbUpgradeStatus.success, len(Gw2Db.__endpoints__))
        except Exception as e:
            print(e)
            traceback.print_exc()

            # surely while downloading new datas or mapping them => go back
            self._close_db()

            # deleting new incomplete db and restore backed
            if os.path.isfile(self._db):
                os.remove(self._db)
            os.rename('./' + self._back, './' + self._db)

            # reuse backed db
            self._make_db()
            self.running_status(DbUpgradeStatus.error, -1)

            ret = -1

        return ret
