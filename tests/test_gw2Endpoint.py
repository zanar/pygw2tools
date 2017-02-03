from unittest import TestCase

import inspect

import sys

from gw2db import *
from gw2db.auths.accounts import _Gw2AccountAchievement, _Gw2AccountBankUpgrade, _Gw2AccountBank, _Gw2AccountDye, \
    _Gw2AccountFinisher, _Gw2AccountInventory, _Gw2AccountMastery, _Gw2AccountMini, _Gw2AccountOutfit, \
    _Gw2AccountRecipe, _Gw2AccountSkin, _Gw2AccountTitle, _Gw2AccountVault, _Gw2AccountWallet

from gw2db.common import Gw2Endpoint, Base, EPType


class TestGw2Endpoint(TestCase):

    def setUp(self):
        # make the base to force ORM mapping
        try:
            Gw2Db()
        except Exception as e:
            self.fail("Error while mapping ORM: " + str(e))

        def filter_(cls_):
            if not inspect.isclass(cls_):
                return False
            if not issubclass(cls_, Base):
                return False
            if '__table__' not in cls_.__dict__:
                return False
            if 'info' not in cls_.__table__.__dict__:
                return False
            return len( cls_.__table__.info) > 0

        # get tables as endpoint mappers
        eps = inspect.getmembers(sys.modules[__name__], filter_)

        # generate parent / children list
        self.p_eps = [x[1] for x in eps if 'ep_type' in x[1].__table__.info and (x[1].__table__.info['ep_type'] & EPType.child) == 0]
        self.c_eps = [x[1] for x in eps if 'ep_type' in x[1].__table__.info and x[1] not in self.p_eps]

        # to test auths endpoint, put your access token here
        self.test_key = ''

    def test___init__properties(self):
        for lst in [self.p_eps, self.c_eps]:
            for tep in lst:
                try:
                    ep = Gw2Endpoint(tep, 'en', [])
                except Exception as e:
                    self.fail(tep.__name__ + str(e))

                self.assertEquals(ep.table_name, tep.__name__)
                self.assertEquals(ep.rights, tep.__table_args__['info']['rights'])

        parents = list(set([x.__table__.info['parent'] for x in self.c_eps]))
        for tep in self.p_eps:
            try:
                ep = Gw2Endpoint(tep, 'en', self.c_eps)
                if tep.__name__ in parents:
                    self.assertGreater(len(ep._children), 0, ep.table_name)
                else:
                    self.assertEquals(len(ep._children), 0, ep.table_name)
            except Exception as e:
                self.fail(tep.__name__ + str(e))

    def test__next_pkid(self):
        ep = Gw2Endpoint(Gw2Currency, 'en', [])
        for i in range(1, 11):
            self.assertEquals(ep._next_pkid, i)

    def test_set_params(self):
        if len(self.test_key) == 0:
            return

        eps = list()
        for lst in [self.p_eps, self.c_eps]:
            for tep in lst:
                ep = Gw2Endpoint(tep, 'en', [])
                ep.set_params(self.test_key)
                ep.set_params()
                eps.append(ep)
        for ep in eps:
            if (ep._type & EPType.auth) != 0 and (ep._type & EPType.param) == 0:
                _len = 2
            elif (ep._type & EPType.std) != 0:
                _len = 0
            else:
                _len = 1

            self.assertEquals(len(ep._pqueue), _len, ep.table_name)

    def test__size(self):
        for lst in [self.p_eps, self.c_eps]:
            for tep in lst:
                ep = Gw2Endpoint(tep, 'en', [])
                if (ep._type & EPType.auth) == 0:
                    # can't test auths endpoint without access token...
                    self.assertGreater(ep._size(), -1, ep.table_name)
                elif len(self.test_key) > 0:
                    self.assertGreater(ep._size({'access_token': self.test_key}), -1, ep.table_name)
                else:
                    # without access token, return 0 if single else -1
                    self.assertEquals(ep._size(), 0 if (ep._type & EPType.single) != 0 else -1, ep.table_name)

    def test__make_args(self):
        for lst in [self.p_eps, self.c_eps]:
            for tep in lst:
                ep = Gw2Endpoint(tep, 'en', [])
                if (ep._type & EPType.auth) == 0:
                    # can't test auths endpoint without access token...
                    self.assertGreater(len(ep._make_args()), 0, ep.table_name)
                elif len(self.test_key) > 0:
                    self.assertGreater(len(ep._make_args(self.test_key)), 0, ep.table_name)
                else:
                    # without access token, return empty list
                    self.assertEquals(len(ep._make_args()), 0, ep.table_name)

    def test__read(self):
        for tep in self.p_eps:
            ep = Gw2Endpoint(tep, 'en', self.c_eps)
            if (ep._type & EPType.auth) == 0:
                # can't test auths endpoint without access token...
                args = ep._make_args()
            elif len(self.test_key) > 0:
                args = ep._make_args(self.test_key)
            else:
                ep._pqueue.appendleft((None, None, None))
                datas = ep._read()
                self.assertIsNone(datas, ep.table_name)
                continue
                
            ep._pqueue.appendleft((args[0], None, None))
            datas = ep._read()
            self.assertIsNotNone(datas, ep.table_name)
            self.assertGreater(len(datas), 0, ep.table_name)
            # check children if any - args made automatically
            for ch in ep._children:
                datas = ch._read()
                self.assertIsNotNone(datas, ch.table_name)
                self.assertGreater(len(datas), 0, ch.table_name)

    def test_on_error(self):
        ep = Gw2Endpoint(self.p_eps[0], 'en', [])
        ep.on_error()
        self.assertIsNone(ep._read(), ep.table_name)
        self.assertIsNone(ep._build(), ep.table_name)
        self.assertIsNone(ep.upgrade(), ep.table_name)

    def test_upgrade(self):
        for tep in self.p_eps:
            ep = Gw2Endpoint(tep, 'en', self.c_eps)

            if (ep._type & EPType.auth) != 0:
                if len(self.test_key) > 0:
                    ep.set_params(self.test_key)

            if (ep._type & EPType.auth) != 0 and len(self.test_key) == 0:
                ep.set_params()
                datas = ep.upgrade()
                self.assertIsNotNone(datas, ep.table_name)
                self.assertEquals(len(datas), 0)
                continue

            ep.set_params()
            datas = ep.upgrade()
            self.assertIsNotNone(datas, ep.table_name)
            self.assertGreater(len(datas), 0, ep.table_name)
