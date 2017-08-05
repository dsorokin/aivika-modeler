# Copyright (c) 2017 David Sorokin <david.sorokin@gmail.com>
#
# Licensed under BSD3. See the LICENSE.txt file in the root of this distribution.

class ResultSource:
    """Represents the result source."""

    def __init__(self, name):
        """Initializes a new instance by the specified name."""
        self._name = name

    def read_results(self):
        """Return the code that identifies the specified results."""
        return self._name

class ResourceSource(ResultSource):
    """Represents the resource result source."""

    def __init__(self, name):
        """Initializes a new instance by the specified name."""
        ResultSource.__init__(self, name)

class PreemptibleResourceSource(ResultSource):
    """Represents the preemptible resource result source."""

    def __init__(self, name):
        """Initializes a new instance by the specified name."""
        ResultSource.__init__(self, name)

class UnboundedQueueSource(ResultSource):
    """Represents the unbounded queue result source."""

    def __init__(self, name):
        """Initializes a new instance by the specified name."""
        ResultSource.__init__(self, name)

class QueueSource(ResultSource):
    """Represents the bounded queue result source."""

    def __init__(self, name):
        """Initializes a new instance by the specified name."""
        ResultSource.__init__(self, name)

class ServerSource(ResultSource):
    """Represents the server result source."""

    def __init__(self, name):
        """Initializes a new instance by the specified name."""
        ResultSource.__init__(self, name)

class ArrivalTimerSource(ResultSource):
    """Represents the arrival timer result source."""

    def __init__(self, name):
        """Initializes a new instance by the specified name."""
        ResultSource.__init__(self, name)

class RefSource(ResultSource):
    """Represents the reference result source."""

    def __init__(self, name):
        """Initializes a new instance by the specified name."""
        ResultSource.__init__(self, name)
