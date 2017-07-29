# Copyright (c) 2017 David Sorokin <david.sorokin@gmail.com>
#
# Licensed under BSD3. See the LICENSE.txt file in the root of this distribution.

from simulation.aivika.modeler.model import *
from simulation.aivika.modeler.port import *
from simulation.aivika.modeler.stream import *
from simulation.aivika.modeler.data_type import *

def uniform_random_stream(transact_type, min_value, max_value):
    """Return a new stream of transacts with random delays distributed uniformly."""
    expect_transact_type(transact_type)
    model = transact_type.get_model()
    code = 'return $ mapStream (\\a -> ' + transact_type.coerce_arrival('a') + ') $ '
    code += 'randomUniformStream ' + str(min_value) + ' ' + str(max_value)
    y = StreamPort(model, transact_type.get_data_type())
    y.bind_to_input()
    y.write(code)
    return y
