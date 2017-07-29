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
        expect_attr(attr)
        self._attrs[attr.get_name()] = attr

    def get_code(self):
        """Return the type definition code."""
        code = 'data ' + self.get_name() + ' = '
        if len(self._attrs) == 0:
            code += self.get_name()
        else:
            code += '\n  ' + self.get_name() + ' {'
            first = True
            for name in self._attrs:
                attr = self._attrs[name]
                if first:
                    first = False
                    code += '\n      '
                else:
                    code += '\n    , '
                code += attr.get_code()
                code += ' :: ' + _encode_data_type_item(attr.get_data_type())
            code += '\n    }'
        code += '\n'
        return code

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
        code = '(\\a -> return $ ' + self.get_code() + ' a)'
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
        code = '(\\a -> return $ maybe ' + str(default_value) + ' id $ ' + self.get_code() + ' a)'
        return Expr(self._model, code)

    def has_expr(self):
        """Return an expression that evaluates to flag indicating whether the attribute is defined."""
        code = '(\\a -> return $ isJust $ ' + self.get_code(name) + ' a)'
        return Expr(self._model, code)

    def get_data_type(self):
        """Return the data type."""
        return ['Maybe', self._data_type]

def expect_transact_type(transact_type):
    """Expect the argument to define the transact type."""
    if isinstance(transact_type, TransactType):
        pass
    else:
        raise InvalidDataTypeException('Expected a transact data type: ' + str(transact_type))

def expect_attr(attr):
    """Expect the argument to define the attribute."""
    if isinstance(attr, Attr):
        pass
    elif isinstance(attr, OptionalAttr):
        pass
    else:
        raise InvalidDataTypeException('Expected an attribute: ' + str(attr))

def encode_data_type(data_type):
    """Encode the data type represented by a list of strings."""
    return ' '.join(map(_encode_data_type_item, data_type))

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
