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

"""Tools elements for this package

Provides some generic tools for this package

"""


class singleton(object):
    """Singleton decorator."""

    def __init__(self, cls):
        self.__dict__['cls'] = cls

    instances = {}

    def __call__(self):
        if self.cls not in self.instances:
            self.instances[self.cls] = self.cls()
        return self.instances[self.cls]

    def __getattr__(self, attr):
        return getattr(self.__dict__['cls'], attr)

    def __setattr__(self, attr, value):
        return setattr(self.__dict__['cls'], attr, value)


class CbEvent:
    """Callback event handler

    Example:
        # add a callback
        cb_event += my_cb_func

        # remove a callback
        cb_event -= my_cb_func

        # fire an event
        cb_event(..)
    """

    def __init__(self):
        """Initialize a new event handler"""
        self._handlers = set()

    def handle(self, handler):
        """Add a new callback to the handler

        :param handler: the callback function
        :return self
        """
        self._handlers.add(handler)
        return self

    def unhandle(self, handler):
        """Remove a callback from the handler"""
        try:
            self._handlers.remove(handler)
        except:
            raise ValueError("Handler is not handling this event, so cannot unhandle it.")
        return self

    def fire(self, *args, **kargs):
        """Generate a new event"""
        for handler in self._handlers:
            handler(*args, **kargs)

    def get_handler_count(self):
        """Give access to the count of callback handled"""
        return len(self._handlers)

    __iadd__ = handle
    __isub__ = unhandle
    __call__ = fire
    __len__ = get_handler_count
