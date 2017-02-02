from unittest import TestCase

import inspect

import sys
import os

from gw2db import *
from gw2db.auths.accounts import _Gw2AccountAchievement, _Gw2AccountBankUpgrade, _Gw2AccountBank, \
    _Gw2AccountDye, _Gw2AccountFinisher, _Gw2AccountInventory, _Gw2AccountMastery, _Gw2AccountMini, \
    _Gw2AccountOutfit, _Gw2AccountRecipe, _Gw2AccountSkin, _Gw2AccountTitle, _Gw2AccountVault, \
    _Gw2AccountWallet

from gw2db.common import Base, Param


class TestGw2Endpoint(TestCase):

    def setUp(self):
        if os.path.isfile('gw2.db'):
            os.remove('gw2.db')
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
        self.eps = inspect.getmembers(sys.modules[__name__], filter_)
        self.eps = [x[0] for x in self.eps]

        # to test auths endpoint, put your access token here
        self.test_key = ''

    def test___init__properties(self):
        try:
            db1 = Gw2Db()
            db2 = Gw2Db()
        except Exception as e:
            self.fail(str(e))
        
        self.assertIsNotNone(db1)
        self.assertEquals(id(db1), id(db2), "Singleton")
        self.assertEquals(os.path.isfile('gw2.db'), True)
        
        # session
        self.assertIsNotNone(db1.session)
        
        # lang
        l = db1.lang
        self.assertIn(l, ['en', 'es', 'fr', 'de'])
        db1.session.query(Param).filter(Param.name == 'lang').first().value = 'fr' if l != 'fr' else 'en'
        db1.session.commit()
        self.assertNotEquals(db2.lang, l)
        
        # endpoints
        self.assertEquals(len(db1.show_endpoints()), len(self.eps))
        for ep in db1.show_endpoints():
            self.assertIn(ep, self.eps)
        
        try:
            with Gw2Db() as db3:
                self.assertIsNotNone(db3.session)
        except Exception as e:
            self.fail(e)

    def test__check_verions(self):
        db = Gw2Db()
        v = db._check_verions()
        self.assertGreater(v, 0)
        db.session.add(Param(name='build', value=str(v)))
        db.session.commit()
        self.assertEquals(db._check_verions(), 0)

    def check_upgrade(self):
        with Gw2Db() as db:
            if len(db.session.query(Param).filter(Param.name.startswith('KEY_')).all()) == 0:
                if len(self.test_key) > 0:
                    db.session.add(Param(name='KEY_Test', value=self.test_key))
                    db.session.commit()
            
            self.assertGreater(db.upgrade(), 0)         # db is empty, upgrade
            self.assertEquals(db.upgrade(), 0)          # db just upgraded, nothing to do
            self.assertGreater(db.upgrade(True), 0)     # forced upgrade
