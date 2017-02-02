# -*- coding: utf-8 -*-

# This file is part of gw2db.
#
# gw2db is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pyGw2Tools is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# gw2db.  If not, see <http://www.gnu.org/licenses/>.


"""

"""

from unittest import TestLoader, TextTestRunner, TestSuite

from tests.test_gw2Db import TestGw2Db
from tests.test_gw2Endpoint import TestGw2Endpoint

if __name__ == "__main__":

    loader = TestLoader()
    suite = TestSuite((
        loader.loadTestsFromTestCase(TestGw2Endpoint),
        loader.loadTestsFromTestCase(TestGw2Db)
    ))

    runner = TextTestRunner(verbosity = 2)
    runner.run(suite)
