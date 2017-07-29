# Copyright (c) 2017 David Sorokin <david.sorokin@gmail.com>
#
# Licensed under BSD3. See the LICENSE.txt file in the root of this distribution.

from simulation.aivika.modeler.model import *
from simulation.aivika.modeler.port import *
from simulation.aivika.modeler.stream import *
from simulation.aivika.modeler.data_type import *

def uniform_random_stream(transact_type, min_delay, max_delay):
    """Return a new stream of transacts with random delays distributed uniformly."""
    expect_transact_type(transact_type)
    model = transact_type.get_model()
    code = 'return $ mapStream (\\a -> ' + transact_type.coerce_arrival('a') + ') $ '
    code += 'randomUniformStream ' + str(min_delay) + ' ' + str(max_delay)
    y = StreamPort(model, transact_type.get_data_type())
    y.bind_to_input()
    y.write(code)
    return y

def uniform_random_int_stream(transact_type, min_delay, max_delay):
    """Return a new stream of transacts with integer random delays distributed uniformly."""
    expect_transact_type(transact_type)
    model = transact_type.get_model()
    code = 'return $ mapStream (\\a -> ' + transact_type.coerce_arrival('a') + ') $ '
    code += 'randomUniformIntStream ' + str(min_delay) + ' ' + str(max_delay)
    y = StreamPort(model, transact_type.get_data_type())
    y.bind_to_input()
    y.write(code)
    return y

def triangular_random_stream(transact_type, min_delay, median_delay, max_delay):
    """Return a new stream of transacts with random delays having the triangular distribution."""
    expect_transact_type(transact_type)
    model = transact_type.get_model()
    code = 'return $ mapStream (\\a -> ' + transact_type.coerce_arrival('a') + ') $ '
    code += 'randomTriangularStream ' + str(min_delay) + ' ' +  str(median_delay) + ' ' + str(max_delay)
    y = StreamPort(model, transact_type.get_data_type())
    y.bind_to_input()
    y.write(code)
    return y

def normal_random_stream(transact_type, mean_delay, delay_deviation):
    """Return a new stream of transacts with random delays having the normal distribution."""
    expect_transact_type(transact_type)
    model = transact_type.get_model()
    code = 'return $ mapStream (\\a -> ' + transact_type.coerce_arrival('a') + ') $ '
    code += 'randomNormalStream ' + str(mean_delay) + ' ' + str(delay_deviation)
    y = StreamPort(model, transact_type.get_data_type())
    y.bind_to_input()
    y.write(code)
    return y

def lognormal_random_stream(transact_type, normal_mean_delay, normal_delay_deviation):
    """Return a new stream of transacts with random delays having the lognormal distribution.

       The numerical parameters are related to the normal distribution that
       this distribution is derived from.
    """
    expect_transact_type(transact_type)
    model = transact_type.get_model()
    code = 'return $ mapStream (\\a -> ' + transact_type.coerce_arrival('a') + ') $ '
    code += 'randomLogNormalStream ' + str(normal_mean_delay) + ' ' + str(normal_delay_deviation)
    y = StreamPort(model, transact_type.get_data_type())
    y.bind_to_input()
    y.write(code)
    return y
