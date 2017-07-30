# Copyright (c) 2017 David Sorokin <david.sorokin@gmail.com>
#
# Licensed under BSD3. See the LICENSE.txt file in the root of this distribution.

from simulation.aivika.modeler.model import *
from simulation.aivika.modeler.expr import *
from simulation.aivika.modeler.pdf import *

def uniform_random_expr(model, min_value, max_value):
    """Return an expression that returns the random value distributed uniformly."""
    code = '(const $ liftParameter $ '
    code += 'randomUniform '
    code += str(min_value)
    code += ' '
    code += str(max_value)
    code += ')'
    return Expr(model, code)

def uniform_int_random_expr(model, min_value, max_value):
    """Return an expression that returns the integer random value distributed uniformly."""
    code = '(const $ liftParameter $ '
    code += 'randomUniformInt '
    code += str(min_value)
    code += ' '
    code += str(max_value)
    code += ')'
    return Expr(model, code)

def triangular_random_expr(model, min_value, median_value, max_value):
    """Return an expression that returns the random value having the triangular distribution."""
    code = '(const $ liftParameter $ '
    code += 'randomTriangular '
    code += str(min_value)
    code += ' '
    code += str(median_value)
    code += ' '
    code += str(max_value)
    code += ')'
    return Expr(model, code)

def normal_random_expr(model, mean_value, deviation):
    """Return an expression that returns the random value having the normal distribution."""
    code = '(const $ liftParameter $ '
    code += 'randomNormal '
    code += str(mean_value)
    code += ' '
    code += str(deviation)
    code += ')'
    return Expr(model, code)
