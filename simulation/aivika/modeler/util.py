# Copyright (c) 2017 David Sorokin <david.sorokin@gmail.com>
#
# Licensed under BSD3. See the LICENSE.txt file in the root of this distribution.

class InvalidDataTypeException(Exception):
    """Raised when the data type is invalid."""

    def __init__(self, message):
        """Initializes a new instance."""
        self.message = message

def encode_data_type(data_type):
    """Encode the data type represented by a list of strings."""
    return ' '.join(map(_encode_data_type_item, data_type))

def _encode_data_type_item(data_type_item):
    """Encode the data type item."""
    if isinstance(data_type_item, str):
        return data_type_item
    elif isinstance(data_type_item, list):
        return '(' + encode_data_type(data_type_item) + ')'
    else:
        raise InvalidDataTypeException('Expected a legal data type: ' + str(data_type_item))
