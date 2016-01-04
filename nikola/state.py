# -*- coding: utf-8 -*-

# Copyright © 2012-2016 Roberto Alsina and others.

# Permission is hereby granted, free of charge, to any
# person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Persistent state implementation."""

import json
import os

from . import utils


class Persistor():
    """Persist stuff in a place.

    This is an intentionally dumb implementation. It is *not* meant to be
    fast, or useful for arbitrarily large data. Use lightly.

    Intentionally it has no namespaces, sections, etc. Use as a
    responsible adult.
    """

    def __init__(self, path):
        """Where do you want it persisted."""
        self._path = path
        utils.makedirs(os.path.dirname(path))
        self.data = {}
        if os.path.isfile(path):
            with open(path) as inf:
                self.data = json.load(inf)

    def get(self, key):
        """Get data stored in key."""
        return self.data.get(key)

    def set(self, key, value):
        """Store value in key."""
        self.data[key] = value
        self._save()

    def delete(self, key):
        """Delete key and the value it contains."""
        if key in self.data:
            self.data.pop(key)
        self._save()

    def _save(self):
        with open(self._path, 'w') as outf:
            json.dump(self.data, outf, sort_keys=True, indent=2)
