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

"""gw2db common module

This module provides elements used by the whole package, particularly JSON to db mapping elements.

Attributes:
    addr_v2: base WebAPI url used to download datas.

    Base: super class for all tables declarations. It didn't use the standard ``DeclarativeMeta`` class
        but an inherited one ``_JsonDeclarativeMeta`` which declare some JSON mapping abstract functions.

"""

# std imports
import copy
import math
import json
import traceback
from abc import abstractmethod
from enum import IntEnum, unique
from datetime import datetime, timezone
from tzlocal import get_localzone

# threading imports
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import closing
from threading import Event, Lock

# web imports
import requests
from requests import HTTPError, Timeout, RequestException
from urllib.parse import urlencode

# ORM imports
from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.inspection import inspect

# base WebAPI url
addr_v2 = 'https://api.guildwars2.com/v2/'


# Super class for tables declaration
class _JsonDeclarativeMeta(DeclarativeMeta):
    """Super class for tables declaration

    This class inherit ``DeclarativeMeta`` to be able to declare tables, and define some
    method for JSON mapping
    """

    @abstractmethod
    def from_parent(self, _pjson):
        """Transform parent JSON datas into values used to replace endpoint params

        :param _pjson: parent JSON datas
        :return: tuple containing tuple / list of tuple params and an extract of parent JSON
        """
        return (None, None,)

    @abstractmethod
    def merge_json(self, _json, parent, params):
        """Append (or not) parent JSON datas from ``from_parent`` into current datas

        :param _json: current JSON datas
        :param parent: parent (exctracted) JSON datas
        :param params: remplacement params for url
        """
        pass

    @abstractmethod
    def to_child(self, ch, key, _json):
        """Filter datas to send to child endpoint

        :param ch: child endpoint
        :param key: access token
        :param _json: current datas
        """
        ch.set_params(key, _json)

    @abstractmethod
    def after_build(self, mapped):
        """Do something after JSON to db mapping

        :param mapped: dictionnary of mapped values - key=table class, value=list of mapped JSON datas
        """
        pass


# Super class for all tables declarations
Base = declarative_base(metaclass=_JsonDeclarativeMeta)


# Types of endpoint
@unique
class EPType(IntEnum):
    """Types of endpoint

    Attributes:
        EPType.std: standard enpoint, return a list of ids and have 'page' / 'page_size' possibles parameters
        EPType.child: child endpoint / subendpoint
        EPType.single: return directly an object when accessed
        EPType.param: endpoint which need parameters to be accessed
        EPType.auth: authenticated endpoint, which need an access token
        EPType.psc: parametrized single child endpoint
        EPType.ac: authenticated child endpoint
        EPType.sa: authenticated single endpoint
        EPType.sac: authenticated single child endpoint
        EPType.psac: parametrized authenticated single child endpoint
    """
    std = 0,
    child = 1,
    single = 2,
    param = 4,
    auth = 8,

    psc = 1 + 2 + 4,  # child + single + param
    ac = 8 + 1,  # auth + child
    sa = 8 + 2,  # auth + single
    sac = 8 + 1 + 2,  # auth + child + single
    psac = 8 + 7  # auth + psc


# Add endpoint definition to a table declaration
def endpoint_def(endpoint, ep_type=EPType.std, locale=False, workers=5, rights=list(), parent='', **kwargs):
    """Add endpoint definition to a table declaration

    :param endpoint: endpoint name, which will be added to ``addr_v2`` before download
    :param ep_type: endpoint Type (EPType)
    :param locale: localizable
    :param workers: number of thread used to download datas
    :param rights: access token rights needed to access this endpoint
    :param parent: parent table name (with an endpoint def too)
    :param kwargs: other table arguments, unrelated to JSON mapping
    :return: dictionnary of table parameters - must be set into ``__table_args__``
    """
    return dict(
        info=dict(
            endpoint=endpoint,
            ep_type=ep_type,
            locale=locale,
            workers=workers,
            rights=rights,
            parent=parent
        ),
        **kwargs
    )


# Declare a JSON mapping to a table relationship
def rel_json(cls_, keys=None, fn=lambda j, pj: j):
    """Declare a JSON mapping to a table relationship

    A JSON mapping added to a relationship is used to create mapping for JSON subobject into a subtable

    :param cls_: subtable to map
    :param keys: JSON dict list of keys to access datas to map - if None or not set, relationship name is used
    :param fn: lambda expression / function used to modify datas before mapping - if not set, the subobject is mapped.
               function parameters are: j=found JSON subobject relative to ``keys``, pj=current mapping JSON object
    :return: dictionnary of ``relationship()`` parameters - must be set into ``info``
    """
    p = dict(map=cls_, fn=fn)
    if keys is not None:
        p['keys'] = keys if type(keys) is list else [keys]
    return p


# Declare a JSON mapping to a table column
def col_json(keys=None, fn=lambda j, pj: j):
    """Declare a JSON mapping to a table column

    A JSON mapping added to a column is used to set a value into a table column

    :param keys: JSON dict list of keys to access value to store - if None or not set, column name is used
    :param fn: lambda expression / function used to modify value before storing - if not set, the value is
               stored as is, except for list which are stored with <c>lambda j, pj: str(j)[1: -1].replace('\'', '')</c>
               function parameters are: j=found JSON subobject relative to ``keys``, pj=current mapping JSON object
    :return: dictionnary of ``Column()`` parameters - must be set into ``info``
    """
    p = dict(fn=fn)
    if keys is not None:
        p['keys'] = keys if type(keys) is list else [keys]
    return p


# Convert a JSON string date into a storable datetime
def gw2_to_orm_date(strdate, pj):
    """Convert a JSON string date into a storable datetime

     This function is used as ``fn`` function in ``col_json``.

    :param strdate: string date to convert
    :param pj: unused parameter
    :return: a storable datetime date
    """
    if '.' in strdate:
        d = datetime.strptime(strdate.replace('Z', '+0000'), '%Y-%m-%dT%H:%M:%S.%f%z')
    else:
        d = datetime.strptime(strdate.replace('Z', '+0000'), '%Y-%m-%dT%H:%M:%S%z')
    return d.replace(tzinfo=timezone.utc).astimezone(get_localzone())


# WebAPI endpoint manager
class Gw2Endpoint:
    """WebAPI endpoint manager

    Need a table declared class with ``endpoint_def`` to work. This class downloads datas from an endpoint,
    maps them into a dictionnary which can be added to the database
    """
    def __init__(self, table, lang, children):
        """Initialize an endpoint manager

        :param table: an inherited class of ``Base`` which has a ``__table_args__ = endpoint_def(...)`` attribute
        :param lang: current db language
        :param children: list of all inherited class of ``Base`` which are declared with ``EPType.child`` in type
        """
        self._table = table
        kwargs = copy.deepcopy(table.__table__.info)

        self._endpoint = kwargs.pop('endpoint')
        self._locale = lang if kwargs.pop('locale') else None
        self._workers = kwargs.pop('workers')
        self._type = kwargs.pop('ep_type')
        self._rights = kwargs.pop('rights')

        self._children = [Gw2Endpoint(x, lang, children) for x in children if x.__table__.info['parent'] == table.__name__]

        self._lock = Lock()
        self._pkid = 0

        self._end = Event()
        self._err = Event()
        self._pqueue = deque()

    @property
    def table_name(self):
        """Give access to inherited class of ``Base`` name

        :return: the name of the class associated to this endpoint
        """
        return self._table.__name__

    @property
    def rights(self):
        """Give access to the access token rights needed to access this endpoint

        :return: the rights declared in ``endpoint_def`` call
        """
        return self._rights

    @property
    def _next_pkid(self):
        """Generate a new primary key id

        SQLite need an integer primary key if there is only one primary_key. Some JSON objects have a string as id and
        have subobjects, so it need this property

        :return:
        """
        with self._lock:
            self._pkid += 1
            return self._pkid

    def _size(self, args=None):
        """For non single endpoints, get the number of objects returned by the endpoint

        :param args: arguments as dictionnary added to the url after the '?'
        :return: the endpoint size
        """
        if (self._type & EPType.single) != 0:
            return 0

        urlp = '?' + urlencode(args) if args is not None and len(args) > 0 else ''
        try:
            ans = requests.get(addr_v2 + self._endpoint + urlp, timeout=5)
            return int(math.ceil(int(ans.headers['x-result-total']) / 200))
        except (HTTPError, Timeout, KeyError):
            self.on_error()
            return -1

    def _make_args(self, key=''):
        """Make the url arguments, regarding to endpoint definition

        :param key: access token value
        :return: a dictionnary of parameters
        """
        ua = dict()

        if self._locale is not None:
            ua['lang'] = self._locale

        if (self._type & EPType.auth) != 0:
            ua['access_token'] = key

        if (self._type & EPType.single) != 0:
            return [ua]

        size = self._size(ua)
        uas = [dict(page=i, page_size=200, **ua) for i in range(0, size)]
        return uas

    def _read(self):
        """Read a part of the endpoint datas, regarding to url arguments stored in the queue

        :return: list of JSON objects
        """
        args, params, parent = (None, None, None)
        while not self._err.is_set():
            try:
                p = self._pqueue.pop()
                if type(p) is str:
                    self._end.set()
                    return None

                (args, params, parent) = p
                break
            except IndexError:
                params = None
                if self._end.is_set():
                    return None

        urlp = '?' + urlencode(args) if args is not None and len(args) > 0 else ''
        endpoint = self._endpoint
        if params is not None:
            if type(params) is list:
                endpoint = self._endpoint % tuple(params)
            else:
                endpoint = self._endpoint % params

        try:
            text = ''
            with closing(requests.get(addr_v2 + endpoint + urlp, stream=True, timeout=10)) as r:
                r.raise_for_status()
                for data in r.iter_content(chunk_size=64 * 1024, decode_unicode=True):
                    text += data
        except RequestException:
            self.on_error()
            return None

        _json = json.loads(text)
        if type(_json) is not list:
            _json = [_json]
        for i in range(0, len(_json)):
            if type(_json[i]) is dict:
                break
            if _json[i] is not None and type(_json[i]) is not dict:
                _json = [{'id': x} for x in _json if x is not None]
                break

        _json = [x for x in _json if x is not None]
        if (self._type & (EPType.auth | EPType.child)) != 0:
            for _j in _json:
                if (self._type & EPType.auth) != 0:
                    _j['api_key'] = args['access_token']
                if (self._type & EPType.child) != 0:
                    self._table.merge_json(_j, parent, params)

        for ch in self._children:
            for _j in _json:
                self._table.to_child(ch, args['access_token'] if 'access_token' in args else '', _j)

        return _json

    def _mapping(self, _json, table, _pjson=None):
        """Map a JSON object / subobject to a storable dictionnary

        This method is recursive. The first call is for the endpoint object, next are for subobject found with
        table relationship

        :param _json: JSON object / subobject to map
        :param table: inherited class of Base to map JSON into
        :param _pjson: parent JSON object - None on first call, parent object of ``_json`` after
        :return: a list of mapped objects as tuple - (table, list of objects)
        """
        def strlist(x):
            return str(x)[1: -1]

        mapped = list()
        _newj = {}

        # check inherited class
        _table = table
        subc = _table.__subclasses__()
        if len(subc) > 0:
            subc.append(_table)
            switch = _table.__mapper_args__['polymorphic_on'].key
            for _t in subc:
                if _json[switch] == _t.__mapper_args__['polymorphic_identity']:
                    _table = _t
                    break

        # mapping columns
        try:
            cols = [x for x in _table.__table__.columns]
            if _table != table:
                cols.extend([x for x in table.__table__.columns])
            for col in cols:
                value = None
                if col.key in _json:
                    value = _json[col.key]
                elif 'keys' in col.info:
                    value = _json
                    for i, sk in enumerate(col.info['keys']):
                        value = value[sk] if sk in value else None
                        if value is None:
                            break

                if value is not None:
                    fn = col.info['fn'] if 'fn' in col.info else lambda j, pj: j
                    _newj[col.key] = fn(value, _pjson)
                    if type(_newj[col.key]) is list:
                        _newj[col.key] = strlist(value)
                else:
                    if col.default is not None and col.primary_key:
                        _newj[col.key] = col.default.arg
                    if col.key == 'pkid':
                        _newj[col.key] = self._next_pkid
                        _json[col.key] = _newj[col.key]
        except:
            traceback.print_exc()
            self.on_error()
            return None

        if len(_newj) == 0:
            return mapped
        mapped.append((_table, _newj))

        # mapping relationships
        try:
            rels = [x for x in inspect(_table).relationships if 'map' in x.info]
            if _table != table:
                rels.extend([x for x in inspect(table).relationships if 'map' in x.info])
            for rel in rels:
                value = None
                if rel.key in _json:
                    value = _json[rel.key]
                elif 'keys' in rel.info:
                    value = _json
                    for i, sk in enumerate(rel.info['keys']):
                        value = value[sk] if sk in value else None
                        if value is None:
                            break

                if value is not None:
                    fn = rel.info['fn']
                    subj = fn(value, _json)
                    if type(subj) is list:
                        for s in subj:
                            mapped.extend(self._mapping(s, rel.info['map'], _json))
                    else:
                        mapped.extend(self._mapping(subj, rel.info['map'], _json))
        except:
            traceback.print_exc()
            self.on_error()
            return None

        return mapped

    def _build(self):
        """Threaded method - read then map a part of the endpoint

        :return: a list of mapped objects as tuple - (table, list of objects)
        """
        mapped = list()
        while not self._end.is_set() and not self._err.is_set():
            _json = self._read()
            if _json is None:
                if not self._end.is_set():
                    self.on_error()
                break

            for _j in _json:
                _map = self._mapping(_j, self._table)
                if _map is None:
                    if not self._end.is_set():
                        self.on_error()
                    break
                for elem in _map:
                    (k, v) = elem
                    mapped.append((k, v))

        return mapped if not self._err.is_set() else None

    def upgrade(self):
        """Read and map all the endpoint datas, then manage subendpoints.

        :return: a dictionnary of mapped object - key=table class, values=list of objects
        """
        # making args
        if self._type == EPType.std:
            uas = self._make_args()
            if len(uas) == 0:
                self.on_error()
                return None
            for ua in uas:
                self._pqueue.appendleft((ua, None, None))
            self._pqueue.appendleft('end')

            w = min(len(self._pqueue), self._workers)
        else:
            w = self._workers

        mapped = dict()
        # running myself
        with ThreadPoolExecutor(max_workers=w) as my_dl:
            my_ths = {my_dl.submit(self._build): i for i in range(0, w)}
            for future in as_completed(my_ths):
                if future.exception() is not None:
                    self.on_error()
                    traceback.print_exc()
                    continue
                if self._err.is_set():
                    continue

                datas = future.result()
                if datas is None:
                    self.on_error()
                    continue

                for (_cls, _map) in datas:
                    if _cls in mapped:
                        mapped[_cls].append(_map)
                    else:
                        mapped[_cls] = [_map]

            # tell children to stop without err
            for ch in self._children:
                ch.set_params()

        # starting children
        with ThreadPoolExecutor(max_workers=len(self._children)) as ch_dl:
            ch_ths = {ch_dl.submit(x.upgrade): x for x in self._children}
            for future in as_completed(ch_ths):
                if future.exception() is not None:
                    self.on_error()
                    traceback.print_exc()
                    continue
                if self._err.is_set():
                    continue

                _mapped = future.result()
                if _mapped is None:
                    self.on_error()
                    continue

                for k, v in _mapped.items():
                    if k in mapped:
                        mapped[k].extend(v)
                    else:
                        mapped[k] = v

        self._table.after_build(mapped)
        return mapped if not self._err.is_set() else None

    def set_params(self, key='', _pjson=None):
        """Add parameters needed to call the endpoint

        :param key: access token
        :param _pjson: parent endpoint object
        """
        if self._type == EPType.std:
            return

        if len(key) == 0 and _pjson is None:
            self._pqueue.appendleft('end')
            return

        uas = self._make_args(key)
        if len(uas) == 0:
            self.on_error()
            return

        if (self._type & EPType.param) != 0:
            (format_, _pj) = self._table.from_parent(_pjson)
            if format_ is None:
                return
            if type(format_) is tuple:
                format_ = [format_]
        else:
            (format_, _pj) = ([None], _pjson)

        self._pqueue.extendleft([(ua, _f_, _pj) for ua in uas for _f_ in format_])

    def on_error(self):
        """Stop the download / mapping. The ``upgrade`` method will finish with error too"""
        self._err.set()
        for ch in self._children:
            ch.on_error()


# Db table - store applications parameters
class Param(Base):
    """Db table - store applications parameters

    Attributes:
        Param.id: a unused primary key - needed by SQLite
        Param.name: the parameter name
        Param.value: the parameter value
    """
    __tablename__ = "app_params"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    value = Column(String, nullable=False)
