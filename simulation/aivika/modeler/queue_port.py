# Copyright (c) 2017 David Sorokin <david.sorokin@gmail.com>
#
# Licensed under BSD3. See the LICENSE.txt file in the root of this distribution.

from simulation.aivika.modeler.model import *
from simulation.aivika.modeler.port import *
from simulation.aivika.modeler.queue_strategy import *
from simulation.aivika.modeler.util import *

def create_unbounded_queue(model, item_data_type, name, descr = None, storing_queue_strategy = 'FCFS', output_queue_strategy = 'FCFS'):
    """Return a new unbounded queue by the specified model, item data type, name and optional description.

       You can also specify the strategies that will be applied when storing and extracting the items
       from the queue.
    """
    expect_queue_strategy(storing_queue_strategy)
    expect_queue_strategy(output_queue_strategy)
    base_comp = model.get_base_comp()
    y = UnboundedQueuePort(model, item_data_type, storing_queue_strategy, output_queue_strategy, name = name, descr = descr)
    comp_type = []
    comp_type.append('Simulation')
    if not (base_comp is None):
        comp_type.append(base_comp)
    comp_type.append(y.get_data_type())
    code = 'IQ.newQueue ' + storing_queue_strategy + ' ' + output_queue_strategy
    code = '(runEventInStartTime $ ' + code + ') :: ' + encode_data_type (comp_type)
    y._item_data_type = item_data_type
    y.write(code)
    return y

def unbounded_enqueue_stream(unbounded_queue_port, stream_port):
    """Add the items from the specified stream to the given unbounded queue."""
    q = unbounded_queue_port
    s = stream_port
    expect_unbounded_queue(q)
    expect_stream(s)
    model = q.get_model()
    if model != s.get_model():
        raise InvalidPortException('Expected ports ' + q.get_name() + ' and ' + s.get_name() + ' to belong to the same model.')
    code = 'consumeStream (\\a -> liftEvent $ IQ.enqueue ' + q.read() + ' a) ' + s.read()
    code = 'runProcessInStartTime ' + code
    model.add_action(code)

def unbounded_dequeue_stream(unbounded_queue_port):
    """Return a stream of items extracted from the unbounded queue."""
    q = unbounded_queue_port
    expect_unbounded_queue(q)
    model = q.get_model()
    item_data_type = q.get_item_data_type()
    code = 'return $ repeatProcess (IQ.dequeue ' + q.read() + ')'
    y = StreamPort(model, item_data_type)
    y.write(code)
    y.bind_to_input()
    return y
