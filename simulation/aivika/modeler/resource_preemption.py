# Copyright (c) 2017 David Sorokin <david.sorokin@gmail.com>
#
# Licensed under BSD3. See the LICENSE.txt file in the root of this distribution.

from simulation.aivika.modeler.model import *
from simulation.aivika.modeler.port import *
from simulation.aivika.modeler.expr import *

def create_preemptible_resource(model, count, name, descr = None):
    """Return a preemptible resource by the specified model, count, name and optional description."""
    return create_preemptible_resource_with_max_count(model, count, count, name, descr = descr)

def create_preemptible_resource_with_max_count(model, count, max_count, name, descr = None):
    """Return a preemptible resource by the specified model, count, maximum count, name, and optional description.

       The maximum count can be None, which means that the resource bound is indefinite.
    """
    y = PreemptibleResourcePort(model, name = name, descr = descr)
    count = str(count)
    if max_count is None:
        max_count = 'Nothing'
    else:
        max_count = '(Just ' + str(max_count) + ')'
    code = 'PR.newResourceWithMaxCount ' + count + ' ' + max_count
    code = 'runEventInStartTime $ ' + code
    y.write(code)
    return y

def request_preemptible_resource_with_priority(preemptible_resource_port, priority_expr, stream_port):
    """Request for or preempt the resource in case of need with the given priority when processing the specified stream within the resulting stream.

       The less priority is higher. The priority must be specified as the Expr instance.
    """
    r = preemptible_resource_port
    s = stream_port
    expect_preemptible_resource(r)
    expect_stream(s)
    expect_same_model([r, s])
    model = r.get_model()
    item_data_type = s.get_item_data_type()
    code = 'return $ mapStreamM (\\a -> do { p <- liftEvent $ '
    code += priority_expr.read('a')
    code += '; PR.requestResourceWithPriority '
    code += r.read()
    code += ' p; return a }) '
    code += s.read()
    y = StreamPort(model, item_data_type)
    y.write(code)
    y.bind_to_input()
    s.bind_to_output()
    return y

def release_preemptible_resource(preemptible_resource_port, stream_port):
    """Release the preemptible resource when processing the specified stream within the resulting stream."""
    r = preemptible_resource_port
    s = stream_port
    expect_preemptible_resource(r)
    expect_stream(s)
    expect_same_model([r, s])
    model = r.get_model()
    item_data_type = s.get_item_data_type()
    code = 'return $ mapStreamM (\\a -> do { PR.releaseResource '
    code += r.read()
    code += '; return a }) '
    code += s.read()
    y = StreamPort(model, item_data_type)
    y.write(code)
    y.bind_to_input()
    s.bind_to_output()
    return y

def preemptible_resource_count(preemptible_resource_port):
    """Return an expression that evaluates to the resource contents."""
    r = preemptible_resource_port
    expect_preemptible_resource(r)
    model = r.get_model()
    code = '(\\a -> liftEvent $ PR.resourceCount ' + r.read() + ')'
    return Expr(model, code)
