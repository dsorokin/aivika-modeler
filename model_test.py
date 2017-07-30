#!/usr/local/bin/python3

# NOTE: The model itself is quite meaningless. The purpose is
#       to check all possible cases. Consider it like an unit-test

from simulation.aivika.modeler import *

model = MainModel()

data_type = TransactType(model, 'MyTransact')

field1 = Attr(data_type, 'field1', 3)
field2 = OptionalAttr(data_type, 'field2', INT_TYPE)

port1 = merge_streams([empty_stream(model, data_type),
    uniform_random_stream(data_type, 3, 7),
    uniform_int_random_stream(data_type, 3, 7),
    triangular_random_stream(data_type, 3, 4, 7),
    normal_random_stream(data_type, 5, 3),
    lognormal_random_stream(data_type, 5, 3),
    exponential_random_stream(data_type, 5),
    erlang_random_stream(data_type, 5, 4),
    poisson_random_stream(data_type, 5),
    binomial_random_stream(data_type, 0.2, 3),
    gamma_random_stream(data_type, 2, 3),
    beta_random_stream(data_type, 2, 3),
    weibull_random_stream(data_type, 2, 3),
    discrete_random_stream(data_type, [(0.1, 2), (0.4, 3), (0.5, 6)])])

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
    binary_expr(time_expr(model), '*', int2double_expr(resource_count(r1)))),
        return_expr(model, 2),
        return_expr(model, 4))

port6 = release_resource(r3, request_resource_with_priority(r3, priority, release_resource(r1, request_resource(r1, port5b))))

(port7a, port7b) = test_stream(return_expr(model, 'False'), port6)

q1 = create_queue(model, data_type, 7, 'q1')
q2 = create_unbounded_queue(model, data_type, 'q2')

(port8a, port8b) = clone_stream(2, port3)

enqueue_stream(q1, port8a)
enqueue_stream_or_remove_item(q1, port7a)
unbounded_enqueue_stream(q2, port8b)

port9a = dequeue_stream(q1)
port9b = unbounded_dequeue_stream(q2)

terminate_stream(port7b)
terminate_stream(port9a)

queue_expr = binary_expr(binary_expr(queue_size(q1), '<', queue_capacity(q1)),
    'and', binary_expr(unbounded_queue_size(q2), '>', return_expr(model, 0)))

(port10a, port10b) = test_stream(queue_expr, port9b)

terminate_stream(port10b)

cmp_attr_expr = binary_expr(field1.get_expr(), '>', return_expr(model, 3))

(port11a, port11b) = test_stream(cmp_attr_expr, port10a)

terminate_stream(port11a)

cmp_opt_attr = binary_expr(field2.get_expr('777'), '<', return_expr(model, 11))
cmp_opt_attr = binary_expr(field2.has_expr(), 'and', cmp_opt_attr)

(port12a, port12b) = test_stream(cmp_opt_attr, port11b)

terminate_stream(port12a)

port13a = transform_stream(identity_transform(model), port12b)
port13b = transform_stream(compose_transforms(identity_transform(model), identity_transform(model)), port13a)
port13c = transform_stream(field1.assign_transform(6.5), port13b)
port13d = transform_stream(field2.assign_transform(10), port13c)
port13e = transform_stream(compose_transforms(identity_transform(model), field2.removal_transform()), port13d)
port13 = port13e

s1 = uniform_random_server(data_type, 3, 7)
s2 = uniform_int_random_server(data_type, 3, 7)

port14a = server_stream(s1, port13)
port14b = server_stream(s2, port14a)
port14 = port14b

terminate_stream(port14)

specs = Specs(0, 100, 0.1)

model.run(standalone = True, specs = specs)
