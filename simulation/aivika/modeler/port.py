# Copyright (c) 2017 David Sorokin <david.sorokin@gmail.com>
#
# Licensed under BSD3. See the LICENSE.txt file in the root of this distribution.

from simulation.aivika.modeler.data_type import *

class InvalidPortException(Exception):
    """Raised when the port is invalid."""

    def __init__(self, message):
        """Initializes a new instance."""
        self.message = message

class Port:
    """The simulation port."""

    _next_id = 1

    def __init__(self, model, data_type, name = None, descr = None, comp = None):
        """Initializes a new port."""
        self._model = model
        self._data_type = data_type
        if name is None:
            self._name = '_port_' + str(Port._next_id)
            Port._next_id += 1
        else:
            self._name = name
        self._mangled_name = model.get_var_prefix() + self._name
        if descr is None:
            self._descr = ''
        else:
            self._descr = descr
        self._comp = comp
        if comp is None:
            model.add_lazy_var(self._mangled_name)
        else:
            model.add_var(self._mangled_name, comp)

    def get_model(self):
        """Return the model that the port belongs to."""
        return self._model

    def get_data_type(self):
        """Return the port data type."""
        return self._data_type

    def get_name(self):
        """Return the port name."""
        return self._name

    def get_mangled_name(self):
        """Return the real possibly mangled name of the port."""
        return self._mangled_name

    def is_bound_to_input(self):
        """Test whether the port is bound to its input."""
        return True

    def is_bound_to_output(self):
        """Test whether the port is bound to its output."""
        return True

    def read(self):
        """Read the variable value."""
        return self._mangled_name

    def write(self, comp):
        """Set the variable value if it was not defined before."""
        if self._comp is None:
            self._comp = comp
            self._model.add_var(self._mangled_name, comp)
            self._model.add_port(self)
        else:
            raise InvalidPortException('Port ' + self._name + ' is already defined')

    def _connect_to(self, in_port):
        """Connect this port to another input port."""
        if self._data_type != in_port._data_type:
            raise InvalidPortException('Expected ' + in_port._name + ' to have data type ' + encode_data_type(self._data_type))
        else:
            in_port.write('return ' + self.read())

    def _add_result_source(self):
        """Add this port to the result sources."""
        name = '"' + self._encode_str(self._mangled_name) + '"'
        descr = '"' + self._encode_str(self._descr) + '"'
        code = 'resultSource ' + name + ' ' + descr + ' ' + self._mangled_name
        self._model.add_result_source(code)

    def _encode_str(self, str):
        """Encode the string."""
        str = str.replace('\r\n', ' ')
        str = str.replace('\n', ' ')
        str = str.replace('\r', ' ')
        str = str.replace('\\', '\\\\')
        str = str.replace('"', '\\"')
        return str

class PortOnce(Port):
    """The port that can be used as input and output only once."""

    def __init__(self, model, data_type, name = None, descr = None, comp = None):
        """Initializes a new port."""
        Port.__init__(self, model, data_type, name, descr, comp)
        self._input_bound = False
        self._output_bound = False

    def bind_to_input(self):
        """Bind the port to its input."""
        if self._input_bound:
            raise InvalidPortException('Port ' + self._name + ' is already bound to its input')
        else:
            self._input_bound = True

    def bind_to_output(self):
        """Bind the port to its output."""
        if self._output_bound:
            raise InvalidPortException('Port ' + self._name + ' is already bound to its output')
        else:
            self._output_bound = True

    def is_bound_to_input(self):
        """Test whether the port is bound to its input."""
        return self._input_bound

    def is_bound_to_output(self):
        """Test whether the port is bound to its output."""
        return self._output_bound

    def connect_to(self, in_port):
        """Connect this port to another input port."""
        self.bind_to_output()
        in_port.bind_to_input()
        Port._connect_to(self, in_port)

class SourcePort(Port):
    """The port that can be a result source."""

    def __init__(self, model, data_type, name = None, descr = None, comp = None):
        """Initializes a new port."""
        Port.__init__(self, model, data_type, name, descr, comp)

    def add_result_source(self):
        """Add this port to the result sources."""
        Port._add_result_source(self)

def expect_same_model(ports):
    """Expect the ports to be belong to the same model."""
    if len(ports) > 0:
        p0 = ports[0]
        model = p0.get_model()
        for p in ports:
            if model != p.get_model():
                raise InvalidPortException('Expected ports ' + p0.get_name() + ' and ' + p.get_name() + ' to belong to the same model.')

def expect_same_data_type(ports):
    """Expect the ports to have the same data type."""
    if len(ports) > 0:
        p0 = ports[0]
        tp0 = encode_data_type(p0.get_data_type())
        for p in ports:
            tp = encode_data_type(p.get_data_type())
            if tp0 != tp:
                raise InvalidPortException('Expected ports ' + p0.get_name() + ' and ' + p.get_name() + ' to be of the same data type: ' + tp0 + ' versus ' + tp)

class StreamPort(PortOnce):
    """The stream port."""

    def __init__(self, model, item_data_type, name = None, descr = None, comp = None):
        """Initializes a new port."""
        self._item_data_type = item_data_type
        base_comp = model.get_base_comp()
        data_type = []
        data_type.append('Stream')
        if not (base_comp is None):
            data_type.append(base_comp)
        data_type.append(item_data_type)
        PortOnce.__init__(self, model, data_type, name, descr, comp)

    def get_item_data_type(self):
        """Get the item data type"""
        return self._item_data_type

def expect_stream(stream_port):
    """Expect the port to be a stream."""
    s = stream_port
    data_type = s.get_data_type()
    if (not isinstance(s, StreamPort)) or len(data_type) == 0 or data_type[0] != 'Stream':
        raise InvalidPortException('Expected ' + s.get_name() + ' to be a stream')

class ResourcePort(SourcePort):
    """The resource port."""

    def __init__(self, model, queue_strategy, name = None, descr = None, comp = None):
        """Initializes a new port."""
        base_comp = model.get_base_comp()
        if base_comp is None:
            model.add_module_import('import qualified Simulation.Aivika.Resource as R')
        else:
            model.add_module_import('import qualified Simulation.Aivika.Trans.Resource as R')
        data_type = []
        data_type.append('Resource')
        if not (base_comp is None):
            data_type.append(base_comp)
        data_type.append(queue_strategy)
        SourcePort.__init__(self, model, data_type, name, descr, comp)

def expect_resource(resource_port):
    """Expect the port to be a resource."""
    r = resource_port
    data_type = r.get_data_type()
    if len(data_type) == 0 or data_type[0] != 'Resource':
        raise InvalidPortException('Expected ' + r.get_name() + ' to be a resource')

class UnboundedQueuePort(SourcePort):
    """The unbounded queue port."""

    def __init__(self, model, item_data_type, storing_queue_strategy, output_queue_strategy, name = None, descr = None, comp = None):
        """Initializes a new port."""
        self._item_data_type = item_data_type
        base_comp = model.get_base_comp()
        if base_comp is None:
            model.add_module_import('import qualified Simulation.Aivika.Queue.Infinite as IQ')
        else:
            model.add_module_import('import qualified Simulation.Aivika.Trans.Queue.Infinite as IQ')
        data_type = []
        data_type.append('IQ.Queue')
        if not (base_comp is None):
            data_type.append(base_comp)
        data_type.append(storing_queue_strategy)
        data_type.append(output_queue_strategy)
        data_type.append(item_data_type)
        SourcePort.__init__(self, model, data_type, name, descr, comp)

    def get_item_data_type(self):
        """Get the item data type"""
        return self._item_data_type

def expect_unbounded_queue(unbounded_queue_port):
    """Expect the port to be an unbounded queue."""
    q = unbounded_queue_port
    data_type = q.get_data_type()
    if (not isinstance(q, UnboundedQueuePort)) or len(data_type) == 0 or data_type[0] != 'IQ.Queue':
        raise InvalidPortException('Expected ' + q.get_name() + ' to be an unbounded queue')

class QueuePort(SourcePort):
    """The bounded queue port."""

    def __init__(self, model, item_data_type, capacity, input_queue_strategy, storing_queue_strategy, output_queue_strategy, name = None, descr = None, comp = None):
        """Initializes a new port."""
        self._item_data_type = item_data_type
        base_comp = model.get_base_comp()
        if base_comp is None:
            model.add_module_import('import qualified Simulation.Aivika.Queue as Q')
        else:
            model.add_module_import('import qualified Simulation.Aivika.Trans.Queue as Q')
        data_type = []
        data_type.append('Q.Queue')
        if not (base_comp is None):
            data_type.append(base_comp)
        data_type.append(input_queue_strategy)
        data_type.append(storing_queue_strategy)
        data_type.append(output_queue_strategy)
        data_type.append(item_data_type)
        SourcePort.__init__(self, model, data_type, name, descr, comp)

    def get_item_data_type(self):
        """Get the item data type"""
        return self._item_data_type

def expect_queue(queue_port):
    """Expect the port to be a bounded queue."""
    q = queue_port
    data_type = q.get_data_type()
    if (not isinstance(q, QueuePort)) or len(data_type) == 0 or data_type[0] != 'Q.Queue':
        raise InvalidPortException('Expected ' + q.get_name() + ' to be a bounded queue')
