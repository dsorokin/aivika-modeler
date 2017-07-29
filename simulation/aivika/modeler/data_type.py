# Copyright (c) 2017 David Sorokin <david.sorokin@gmail.com>
#
# Licensed under BSD3. See the LICENSE.txt file in the root of this distribution.

from simulation.aivika.modeler.expr import *

STRING_TYPE = 'String'

DOUBLE_TYPE = 'Double'

INT_TYPE = 'Int'

class InvalidDataTypeException(Exception):
    """Raised when the data type is invalid."""

    def __init__(self, message):
        """Initializes a new instance."""
        self.message = message

class TransactType:
    """The transact data type."""

    def __init__(self, model, name):
        """Initializes a new instance."""
        self._model = model
        self._name = name
        self._attrs = dict()
        model.add_module_import('import Data.Maybe')
        model.add_transact_type(self)

    def get_model(self):
        """Return the simulation model."""
        return self._model

    def get_name(self):
        """Return the type name."""
        return self._name

    def add_attr(self, attr):
        """Add the specified attribute."""
        expect_either_attr(attr)
        self._attrs[attr.get_name()] = attr

    def write(self, file):
        """Write the type definition code in the specified file."""
        file.write('type ')
        file.write(self.get_name())
        file.write(' = Arrival ')
        file.write(self._get_impl_name())
        file.write('\n\n')
        self._write_impl(file)

    def _get_impl_name(self):
        """Return the implementation type name."""
        return self.get_name() + '_Impl'

    def _write_impl(self, file):
        """Write the implementation type definition code."""
        name = self._get_impl_name()
        file.write('data ' + name + ' = ')
        if len(self._attrs) == 0:
            file.write(name)
        else:
            file.write('\n  ')
            file.write(name)
            file.write(' {')
            first = True
            for name in self._attrs:
                attr = self._attrs[name]
                if first:
                    first = False
                    file.write('\n      ')
                else:
                    file.write('\n    , ')
                file.write(attr.get_code())
                file.write(' :: ')
                file.write(encode_data_type(attr.get_data_type()))
            file.write('\n    }')
        file.write('\n')

class Attr:
    """The transact attribute."""

    def __init__(self, transact_type, name, data_type = DOUBLE_TYPE):
        """Initializes a new attribute by the specified name and data type."""
        self._model = transact_type.get_model()
        self._name = name
        self._data_type = data_type
        self._transact_type = transact_type
        self._transact_type.add_attr(self)

    def get_model(self):
        """Return the simulation model."""
        return self._model

    def get_name(self):
        """Return the attribute name."""
        return self._name

    def get_code(self):
        """Return the attribute code."""
        code = '_' + self._transact_type.get_name() + '_' + self._name
        return code

    def get_expr(self):
        """Return an expression that evaluates to the attribute value."""
        code = '(\\a -> return $ ' + self.get_code() + ' $ arrivalValue a)'
        return Expr(self._model, code)

    def get_data_type(self):
        """Return the data type."""
        return self._data_type

class OptionalAttr(Attr):
    """The optional transact attribute."""

    def __init__(self, transact_type, name, data_type = DOUBLE_TYPE):
        """Initializes a new attribute by the specified name and data type."""
        self._model = transact_type.get_model()
        self._name = name
        self._data_type = data_type
        self._transact_type = transact_type
        self._transact_type.add_attr(self)

    def get_model(self):
        """Return the simulation model."""
        return self._model

    def get_name(self):
        """Return the attribute name."""
        return self._name

    def get_code(self):
        """Return the attribute code."""
        code = '_' + self._transact_type.get_name() + '_' + self._name
        return code

    def get_expr(self, default_value):
        """Return an expression that evaluates to the attribute value."""
        code = '(\\a -> return $ maybe ' + str(default_value) + ' id $ ' + self.get_code() + ' $ arrivalValue a)'
        return Expr(self._model, code)

    def has_expr(self):
        """Return an expression that evaluates to flag indicating whether the attribute is defined."""
        code = '(\\a -> return $ isJust $ ' + self.get_code() + ' $ arrivalValue a)'
        return Expr(self._model, code)

    def get_data_type(self):
        """Return the data type."""
        return ['Maybe', self._data_type]

def expect_transact_type(transact_type):
    """Expect the argument to define a transact type."""
    if isinstance(transact_type, TransactType):
        pass
    else:
        raise InvalidDataTypeException('Expected a transact data type: ' + str(transact_type))

def expect_either_attr(attr):
    """Expect the argument to define either an attribute or optional attribute."""
    if isinstance(attr, Attr):
        pass
    elif isinstance(attr, OptionalAttr):
        pass
    else:
        raise InvalidDataTypeException('Expected either an attribute or optional attribute: ' + str(attr))

def expect_optional_attr(attr):
    """Expect the argument to define an optional attribute."""
    if isinstance(attr, OptionalAttr):
        pass
    else:
        raise InvalidDataTypeException('Expected an optional attribute: ' + str(attr))

def encode_data_type(data_type):
    """Encode the data type represented by a list of strings."""
    if isinstance(data_type, str):
        return data_type
    elif isinstance(data_type, list):
        return ' '.join(map(_encode_data_type_item, data_type))
    elif isinstance(data_type_item, TransactType):
        return data_type_item.get_name()
    else:
        raise InvalidDataTypeException('Expected a legal data type: ' + str(data_type_item))

def _encode_data_type_item(data_type_item):
    """Encode the data type item."""
    if isinstance(data_type_item, str):
        return data_type_item
    elif isinstance(data_type_item, list):
        return '(' + encode_data_type(data_type_item) + ')'
    elif isinstance(data_type_item, TransactType):
        return data_type_item.get_name()
    else:
        raise InvalidDataTypeException('Expected a legal data type: ' + str(data_type_item))
