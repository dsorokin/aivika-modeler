# Copyright (c) 2017 David Sorokin <david.sorokin@gmail.com>
#
# Licensed under BSD3. See the LICENSE.txt file in the root of this distribution.

class InvalidPortException(Exception):
    """Raised when the port is invalid."""

    def __init__(self, message):
        """Initializes a new instance."""
        self.message = message

class Port:
    """It represents the port."""

    _next_id = 1

    def __init__(self, model, data_type, name = None, descr = None, comp = None):
        """Initializes a new port."""
        self._model = model
        self._data_type = data_type
        if name is None:
            self._name = '__port_' + str(Port._next_id)
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

    def read(self):
        """Read the variable value."""
        return self._mangled_name

    def write(self, comp):
        """Set the variable value if it was not defined before."""
        if self._comp is None:
            self._comp = comp
            self._model.add_var(self._mangled_name, comp)
        else:
            raise InvalidPortException('Port ' + self._name + ' is already defined')

    def _connect_to(self, in_port):
        """Connect this port to another input port."""
        if self._data_type != in_port._data_type:
            raise InvalidPortException('Expected ' + in_port._name + ' to have data type ' + self._data_type)
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
    """It represents the port that can be used as input and output only once."""

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

    def connect_to(self, in_port):
        """Connect this port to another input port."""
        self.bind_to_output()
        in_port.bind_to_input()
        Port._connect_to(self, in_port)

class SourcePort(Port):
    """It represents the port that can be a result source."""

    def __init__(self, model, data_type, name = None, descr = None, comp = None):
        """Initializes a new port."""
        Port.__init__(self, model, data_type, name, descr, comp)

    def add_result_source(self):
        """Add this port to the result sources."""
        Port._add_result_source(self)
