#!/usr/local/bin/python3

from simulation.aivika.modeler import *

model = MainModel()

data_type = 'Int'

port1 = empty_stream(model, data_type)
port2 = StreamPort(model, data_type, 'port2')
port3 = StreamPort(model, data_type, 'port3')

(port2a, port2b) = split_stream(2, port2)
port2c = delay_stream(1.5, port2a)
port1.connect_to(port2)
port4 = merge_streams([port2c, port2b])
(port5a, port5b) = clone_stream(2, port4)

port5a.connect_to(port3)

r1 = create_resource(model, 1, 'r1')
r2 = create_resource_with_max_count(model, 2, 10, 'r2')
r3 = create_resource(model, 3, 'r3', queue_strategy = 'StaticPriorities')

r3.add_result_source()

priority = if_expr(binary_expr(return_expr(model, 10), '<',
    binary_expr(time_expr(model), '*', return_expr(model, 5))),
        return_expr(model, 2),
        return_expr(model, 4))

port6 = request_resource_with_priority(r3, priority, release_resource(r1, request_resource(r1, port5b)))

(port7a, port7b) = test_stream(return_expr(model, 'False'), port6)

q1 = create_queue(model, data_type, 7, 'q1')

enqueue_stream(q1, port3)
port8 = dequeue_stream(q1)

terminate_stream(port7a)
terminate_stream(port7b)
terminate_stream(port8)

specs = Specs(0, 10, 0.1)

model.run(standalone = True, specs = specs)
