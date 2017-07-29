# Copyright (c) 2017 David Sorokin <david.sorokin@gmail.com>
#
# Licensed under BSD3. See the LICENSE.txt file in the root of this distribution.

from simulation.aivika.modeler.model import *
from simulation.aivika.modeler.port import *
from simulation.aivika.modeler.queue_strategy import *

def create_resource(model, count, name, descr = None, queue_strategy = 'FCFS'):
    """Return a resource by the specified model, count, name, optional description and queue strategy.

       The possible queue strategies are: FCFS (aka FIFO), LCFS (aka LIFO),
       SIRO (service in random order) and StaticPriorities. The default is FCFS.

       The resource with StaticPriorities can be acquired only by passing in
       the corresponding priority value, where the less value is a higher priority.
    """
    return create_resource_with_max_count(model, count, count, name, descr = descr, queue_strategy = queue_strategy)

def create_resource_with_max_count(model, count, max_count, name, descr = None, queue_strategy = 'FCFS'):
    """Return a resource by the specified model, count, maximum count, name, optional description and queue strategy.

       The maximum count can be None, which means that the resource bound is indefinite.

       The possible queue strategies are: FCFS (aka FIFO), LCFS (aka LIFO),
       SIRO (service in random order) and StaticPriorities. The default is FCFS.

       The resource with StaticPriorities can be acquired only by passing in
       the corresponding priority value, where the less value is a higher priority.
    """
    expect_queue_strategy(queue_strategy)
    y = ResourcePort(model, queue_strategy, name = name, descr = descr)
    y.priority_queue_strategy = is_priority_queue_strategy(queue_strategy)
    y.queue_strategy = queue_strategy
    count = str(count)
    if max_count is None:
        max_count = 'Nothing'
    else:
        max_count = '(Just ' + str(max_count) + ')'
    code = 'R.newResourceWithMaxCount ' + queue_strategy + ' ' + count + ' ' + max_count
    code = 'runEventInStartTime $ ' + code
    y.write(code)
    return y

def request_resource(resource_port, stream_port):
    """Request for the resource when processing the specified stream within the resulting stream."""
    r = resource_port
    s = stream_port
    expect_resource(r)
    expect_stream(s)
    expect_same_model([r, s])
    if r.priority_queue_strategy:
        raise InvalidPortException('Expected port ' + r.get_name() + ' to have a non-priority queue strategy: ' + r.queue_strategy)
    model = r.get_model()
    base_comp = model.get_base_comp()
    if base_comp is None:
        model.add_module_import('import qualified Simulation.Aivika.Resource as R')
    else:
        model.add_module_import('import qualified Simulation.Aivika.Trans.Resource as R')
    item_data_type = s.get_item_data_type()
    code = 'return $ mapStreamM (\\a -> do { R.requestResource '
    code += r.read()
    code += '; return a }) '
    code += s.read()
    y = StreamPort(model, item_data_type)
    y.write(code)
    y.bind_to_input()
    s.bind_to_output()
    return y

def request_resource_with_priority(resource_port, priority_expr, stream_port):
    """Request for the resource with priority when processing the specified stream within the resulting stream.

       The less priority is higher. The priority must be specified as the Expr instance.

       Also the resource must have the StaticPriorities queue strategy.
    """
    r = resource_port
    s = stream_port
    expect_resource(r)
    expect_stream(s)
    expect_same_model([r, s])
    if not r.priority_queue_strategy:
        raise InvalidPortException('Expected port ' + r.get_name() + ' to have a priority queue strategy: ' + r.queue_strategy)
    model = r.get_model()
    base_comp = model.get_base_comp()
    if base_comp is None:
        model.add_module_import('import qualified Simulation.Aivika.Resource as R')
    else:
        model.add_module_import('import qualified Simulation.Aivika.Trans.Resource as R')
    item_data_type = s.get_item_data_type()
    code = 'return $ mapStreamM (\\a -> do { p <- liftEvent $ '
    code += priority_expr.read('a')
    code += '; R.requestResourceWithPriority '
    code += r.read()
    code += ' p; return a }) '
    code += s.read()
    y = StreamPort(model, item_data_type)
    y.write(code)
    y.bind_to_input()
    s.bind_to_output()
    return y

def release_resource(resource_port, stream_port):
    """Release the resource when processing the specified stream within the resulting stream."""
    r = resource_port
    s = stream_port
    expect_resource(r)
    expect_stream(s)
    expect_same_model([r, s])
    model = r.get_model()
    base_comp = model.get_base_comp()
    if base_comp is None:
        model.add_module_import('import qualified Simulation.Aivika.Resource as R')
    else:
        model.add_module_import('import qualified Simulation.Aivika.Trans.Resource as R')
    item_data_type = s.get_item_data_type()
    code = 'return $ mapStreamM (\\a -> do { R.releaseResource '
    code += r.read()
    code += '; return a }) '
    code += s.read()
    y = StreamPort(model, item_data_type)
    y.write(code)
    y.bind_to_input()
    s.bind_to_output()
    return y

def resource_count(resource_port):
    """Return an expression that evaluates to the resource contents."""
    r = resource_port
    expect_resource(r)
    model = r.get_model()
    code = '(\\a -> liftEvent $ R.resourceCount ' + r.read() + ')'
    return Expr(model, code)
