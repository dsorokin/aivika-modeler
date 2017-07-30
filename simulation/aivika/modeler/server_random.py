# Copyright (c) 2017 David Sorokin <david.sorokin@gmail.com>
#
# Licensed under BSD3. See the LICENSE.txt file in the root of this distribution.

from simulation.aivika.modeler.model import *
from simulation.aivika.modeler.port import *
from simulation.aivika.modeler.stream import *
from simulation.aivika.modeler.data_type import *

def uniform_random_server(transact_type, min_delay, max_delay, preemptible = False):
    """Return a new server that hold the process with random delays distributed uniformly."""
    expect_transact_type(transact_type)
    tp = transact_type.get_data_type()
    model = transact_type.get_model()
    code = 'newPreemptibleRandomUniformServer '
    code += str(preemptible)
    code += ' '
    code += str(min_delay)
    code += ' '
    code += str(max_delay)
    y = ServerPort(model, UNIT_TYPE, tp, tp)
    y.write(code)
    return y
