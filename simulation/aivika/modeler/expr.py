# Copyright (c) 2017 David Sorokin <david.sorokin@gmail.com>
#
# Licensed under BSD3. See the LICENSE.txt file in the root of this distribution.

class InvalidExprException(Exception):
    """Raised when the expression is invalid."""

    def __init__(self, message):
        """Initializes a new instance."""
        self.message = message

class Expr:
    """The expression that may depend on the current modeling time or transact attributes."""

    def __init__(self, model, comp):
        """Initializes a new instance."""
        self._model = model
        self._comp = comp

    def get_model(self):
        """Return the corresponding simulation model."""
        return self._model

    def read(self, transact_comp):
        """Return the corresponding computation."""
        return '(' + self._comp + ' ' + transact_comp + ')'

def expect_expr(expr):
    """Expect the argument to be an expression."""
    if isinstance(expr, Expr):
        pass
    else:
        raise InvalidExprException('Expected an expression: ' + expr)

def return_expr(model, value):
    """Get an expression that returns the specified constant value."""
    code = 'const (return ' + str(value) + ')'
    return Expr(model, code)

def attr_expr(model, attr_name):
    """Get an expression that returns the specified attribute value."""
    code = '(\\a -> return $ ' + attr_name + ' a)'
    return Expr(model, code)

def time_expr(model):
    """Get an expression that returns the current modeling time."""
    code = 'const (liftDynamics time)'
    return Expr(model, code)

def binary_expr(expr_1, op, expr_2):
    """Apply the specified binary operator to the expressions."""
    e1 = expr_1
    e2 = expr_2
    if e1.get_model() != e2.get_model():
        raise InvalidExprException('Expected all expressions to belong to the same model')
    model = e1.get_model()
    model.add_module_import('import Control.Monad')
    if op == '!=':
        op = '/='
    elif op == '%':
        op = 'mod'
    elif op == 'and':
        op = '&&'
    elif op == 'or':
        op = '||'
    elif op in ['==', '<', '>', '<=', '>=', '+', '-', '*', '/']:
        pass
    else:
        raise InvalidExprException('Unrecognized binary operator: ' + op + ' (must be one of: ==, !=, <, >, <=, >=, +, -, *, /, %, and, or)')
    code = '(\\a -> liftM2 (' + op + ') ' + e1.read('a') + ' ' + e2.read('a') + ')'
    return Expr(model, code)

def unary_expr(op, expr):
    """Apply the specified unary operator to the expression."""
    model.add_module_import('import Data.Functor')
    if op == '-':
        op = 'negate'
    elif op == '+':
        op = 'id'
    elif op in ['abs', 'not']:
        pass
    else:
        raise InvalidExprException('Unrecognized unary operator: ' + op + ' (must be one of: +, -, abs, not)')
    model = expr.get_model()
    code = '(\\a -> fmap (' + op + ') ' + expr.read('a') + ')'
    return Expr(model, code)

def if_expr(cond_expr, true_expr, false_expr):
    """The conditional expression."""
    c = cond_expr
    t = true_expr
    f = false_expr
    if (c.get_model() != t.get_model()) or (c.get_model() != f.get_model()):
        raise InvalidExprException('Expected all expressions to belong to the same model')
    model = c.get_model()
    code = '(\\a -> do { f <- ' + c.read('a') + '; '
    code += 'if f then ' + t.read('a') + ' else ' + f.read('a')
    code += ' })'
    return Expr(model, code)
