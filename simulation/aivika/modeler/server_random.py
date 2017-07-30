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

def uniform_int_random_server(transact_type, min_delay, max_delay, preemptible = False):
    """Return a new server that hold the process with integer random delays distributed uniformly."""
    expect_transact_type(transact_type)
    tp = transact_type.get_data_type()
    model = transact_type.get_model()
    code = 'newPreemptibleRandomUniformIntServer '
    code += str(preemptible)
    code += ' '
    code += str(min_delay)
    code += ' '
    code += str(max_delay)
    y = ServerPort(model, UNIT_TYPE, tp, tp)
    y.write(code)
    return y

def triangular_random_server(transact_type, min_delay, mean_delay, max_delay, preemptible = False):
    """Return a new server that hold the process with random delays having the triangular distribution."""
    expect_transact_type(transact_type)
    tp = transact_type.get_data_type()
    model = transact_type.get_model()
    code = 'newPreemptibleRandomTriangularServer '
    code += str(preemptible)
    code += ' '
    code += str(min_delay)
    code += ' '
    code += str(mean_delay)
    code += ' '
    code += str(max_delay)
    y = ServerPort(model, UNIT_TYPE, tp, tp)
    y.write(code)
    return y

def normal_random_server(transact_type, mean_delay, delay_deviation, preemptible = False):
    """Return a new server that hold the process with random delays having the normal distribution."""
    expect_transact_type(transact_type)
    tp = transact_type.get_data_type()
    model = transact_type.get_model()
    code = 'newPreemptibleRandomNormalServer '
    code += str(preemptible)
    code += ' '
    code += str(mean_delay)
    code += ' '
    code += str(delay_deviation)
    y = ServerPort(model, UNIT_TYPE, tp, tp)
    y.write(code)
    return y

def lognormal_random_server(transact_type, normal_mean_delay, normal_delay_deviation, preemptible = False):
    """Return a new server that hold the process with random delays having the lognormal distribution.

       The numerical parameters are related to the normal distribution that
       this distribution is derived from.
    """
    expect_transact_type(transact_type)
    tp = transact_type.get_data_type()
    model = transact_type.get_model()
    code = 'newPreemptibleRandomLogNormalServer '
    code += str(preemptible)
    code += ' '
    code += str(normal_mean_delay)
    code += ' '
    code += str(normal_delay_deviation)
    y = ServerPort(model, UNIT_TYPE, tp, tp)
    y.write(code)
    return y

def exponential_random_server(transact_type, mean_delay, preemptible = False):
    """Return a new server that hold the process with random delays having the exponential distribution."""
    expect_transact_type(transact_type)
    tp = transact_type.get_data_type()
    model = transact_type.get_model()
    code = 'newPreemptibleRandomExponentialServer '
    code += str(preemptible)
    code += ' '
    code += str(mean_delay)
    y = ServerPort(model, UNIT_TYPE, tp, tp)
    y.write(code)
    return y

def erlang_random_server(transact_type, scale, shape, preemptible = False):
    """Return a new server that hold the process with random delays having the Erlang distribution with the specified scale (a reciprocal of the rate) and shape parameters."""
    expect_transact_type(transact_type)
    tp = transact_type.get_data_type()
    model = transact_type.get_model()
    code = 'newPreemptibleRandomErlangServer '
    code += str(preemptible)
    code += ' '
    code += str(scale)
    code += ' '
    code += str(shape)
    y = ServerPort(model, UNIT_TYPE, tp, tp)
    y.write(code)
    return y

def poisson_random_server(transact_type, mean_delay, preemptible = False):
    """Return a new server that hold the process with random delays having the Poisson distribution with the specified mean."""
    expect_transact_type(transact_type)
    tp = transact_type.get_data_type()
    model = transact_type.get_model()
    code = 'newPreemptibleRandomPoissonServer '
    code += str(preemptible)
    code += ' '
    code += str(mean_delay)
    y = ServerPort(model, UNIT_TYPE, tp, tp)
    y.write(code)
    return y

def binomial_random_server(transact_type, probability, trials, preemptible = False):
    """Return a new server that hold the process with random delays having the binomial distribution with the specified probability and trials."""
    expect_transact_type(transact_type)
    tp = transact_type.get_data_type()
    model = transact_type.get_model()
    code = 'newPreemptibleRandomBinomialServer '
    code += str(preemptible)
    code += ' '
    code += str(probability)
    code += ' '
    code += str(trials)
    y = ServerPort(model, UNIT_TYPE, tp, tp)
    y.write(code)
    return y
