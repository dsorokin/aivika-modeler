# Copyright (c) 2017 David Sorokin <david.sorokin@gmail.com>
#
# Licensed under BSD3. See the LICENSE.txt file in the root of this distribution.

from simulation.aivika.modeler.util import *

def empty_results():
    """Return empty results."""
    return 'mempty'

def all_results():
    """Return all results."""
    return 'id'

class ResultSource:
    """Represents the result source."""

    def __init__(self):
        """Initializes a new instance by the specified name."""
        pass

class SamplingStatsSource(ResultSource):
    """The result source for observation statistics based on samples."""

    def __init__(self, source):
        """Initializes a new instance by the specified result source."""
        ResultSource.__init__(self)
        self._source = source
        self.count = self._get_source_property('SamplingStatsCountId')
        self.min_value = self._get_source_property('SamplingStatsMinId')
        self.max_value = self._get_source_property('SamplingStatsMaxId')
        self.mean_value = self._get_source_property('SamplingStatsMeanId')
        self.mean2_value = self._get_source_property('SamplingStatsMean2Id')
        self.variance = self._get_source_property('SamplingStatsVarianceId')
        self.deviation = self._get_source_property('SamplingStatsDeviationId')

    def read_results(self):
        """Return the code that identifies the specified results."""
        return source

    def _get_source_property(self, result_id):
        """Return the specified property by the result identifier."""
        code = self._source.read_results()
        code += ' >>> expandResults >>> resultById '
        code += result_id
        return code

class PortSource(ResultSource):
    """Represents the result source originated from the port."""

    def __init__(self, port):
        """Initializes a new instance by the specified port."""
        ResultSource.__init__(self)
        self._port = port

    def read_results(self):
        """Return the code that identifies the specified results."""
        return 'resultByName ' + encode_str(self._port.get_source_name())

class ResourceSource(PortSource):
    """Represents the resource result source."""

    def __init__(self, port):
        """Initializes a new instance by the specified port."""
        PortSource.__init__(self, port)

class PreemptibleResourceSource(PortSource):
    """Represents the preemptible resource result source."""

    def __init__(self, port):
        """Initializes a new instance by the specified port."""
        PortSource.__init__(self, port)

class UnboundedQueueSource(PortSource):
    """Represents the unbounded queue result source."""

    def __init__(self, port):
        """Initializes a new instance by the specified port."""
        PortSource.__init__(self, port)

class QueueSource(PortSource):
    """Represents the bounded queue result source."""

    def __init__(self, port):
        """Initializes a new instance by the specified port."""
        PortSource.__init__(self, port)

class ServerSource(PortSource):
    """Represents the server result source."""

    def __init__(self, port):
        """Initializes a new instance by the specified port."""
        PortSource.__init__(self, port)

class ArrivalTimerSource(PortSource):
    """Represents the arrival timer result source."""

    def __init__(self, port):
        """Initializes a new instance by the specified port."""
        PortSource.__init__(self, port)

class RefSource(PortSource):
    """Represents the reference result source."""

    def __init__(self, port):
        """Initializes a new instance by the specified port."""
        PortSource.__init__(self, port)
