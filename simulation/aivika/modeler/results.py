# Copyright (c) 2017 David Sorokin <david.sorokin@gmail.com>
#
# Licensed under BSD3. See the LICENSE.txt file in the root of this distribution.

class ResultSource:
    """Represents the result source."""

    def __init__(self, name):
        """Initializes a new result source by its name."""
        self._name = name

    def read_results(self):
        """Return the code that identifies the specified results."""
        return self._name
        
