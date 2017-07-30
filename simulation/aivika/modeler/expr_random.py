# Copyright (c) 2017 David Sorokin <david.sorokin@gmail.com>
#
# Licensed under BSD3. See the LICENSE.txt file in the root of this distribution.

from simulation.aivika.modeler.model import *
from simulation.aivika.modeler.expr import *
from simulation.aivika.modeler.pdf import *

def uniform_random_expr(model, min_delay, max_delay):
    """Return an expression that returns the random value distributed uniformly."""
    code = '(const $ liftParameter $ '
    code += 'randomUniform '
    code += str(min_delay)
    code += ' '
    code += str(max_delay)
    code += ')'
    return Expr(model, code)

def uniform_int_random_expr(model, min_delay, max_delay):
    """Return an expression that returns the integer random value distributed uniformly."""
    code = '(const $ liftParameter $ '
    code += 'randomUniformInt '
    code += str(min_delay)
    code += ' '
    code += str(max_delay)
    code += ')'
    return Expr(model, code)
