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

port6a = release_resource(r3, request_resource_with_priority(r3, priority, release_resource(r1, request_resource(r1, port5b))))
port6b = transform_stream(field2.expr_transform(resource_count(r1)), port6a)
port6 = port6b

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

sa = uniform_random_server(data_type, 3, 7)
sb = uniform_int_random_server(data_type, 3, 7)
sc = triangular_random_server(data_type, 3, 4, 7, preemptible = True)
sd = normal_random_server(data_type, 0.5, 0.3)
se = lognormal_random_server(data_type, 0.5, 0.3)
sf = exponential_random_server(data_type, 0.5)
sg = erlang_random_server(data_type, 0.5, 3)
sh = poisson_random_server(data_type, 0.5)
si = binomial_random_server(data_type, 0.2, 3)
sj = gamma_random_server(data_type, 0.2, 0.3)
sk = beta_random_server(data_type, 0.2, 0.3)
sl = weibull_random_server(data_type, 0.2, 0.3)
sm = discrete_random_server(data_type, [(0.1, 2), (0.4, 3), (0.5, 6)])

port14a = server_stream(sa, port13)
port14b = server_stream(sb, port14a)
port14c = server_stream(sc, port14b)
port14d = server_stream(sd, port14c)
port14e = server_stream(se, port14d)
port14f = server_stream(sf, port14e)
port14g = server_stream(sg, port14f)
port14h = server_stream(sh, port14g)
port14i = server_stream(si, port14h)
port14j = server_stream(sj, port14i)
port14k = server_stream(sk, port14j)
port14l = server_stream(sl, port14k)
port14m = server_stream(sm, port14l)
port14 = port14m

ea = uniform_random_expr(model, 3.0, 7.0)
eb = uniform_int_random_expr(model, 3, 7)
ec = triangular_random_expr(model, 3, 4, 7)
ed = normal_random_expr(model, 0.5, 0.1)
ee = lognormal_random_expr(model, 0.5, 0.1)
ef = exponential_random_expr(model, 0.5)
eg = erlang_random_expr(model, 0.5, 3)
eh = poisson_random_expr(model, 0.5)
ei = binomial_random_expr(model, 0.2, 3)
ej = gamma_random_expr(model, 0.2, 0.3)
ek = beta_random_expr(model, 0.2, 0.3)
el = weibull_random_expr(model, 0.2, 0.3)
em = discrete_random_expr(model, [(0.1, 2), (0.4, 3), (0.5, 6)])

port15a = transform_stream(field1.expr_transform(ea), port14)
port15b = transform_stream(field2.expr_transform(eb), port15a)
port15c = transform_stream(field1.expr_transform(ec), port15b)
port15d = transform_stream(field1.expr_transform(ed), port15c)
port15e = transform_stream(field1.expr_transform(ee), port15d)
port15f = transform_stream(field1.expr_transform(ef), port15e)
port15g = transform_stream(field1.expr_transform(eg), port15f)
port15h = transform_stream(field2.expr_transform(eh), port15g)
port15i = transform_stream(field2.expr_transform(ei), port15h)
port15j = transform_stream(field1.expr_transform(ej), port15i)
port15k = transform_stream(field1.expr_transform(ek), port15j)
port15l = transform_stream(field1.expr_transform(el), port15k)
port15m = transform_stream(field1.expr_transform(em), port15l)
port15 = port15m

pr1 = create_preemptible_resource(model, 71, 'pr1')

port16a = release_preemptible_resource(pr1, request_preemptible_resource_with_priority(pr1, return_expr(model, 11), port15))
port16b = transform_stream(field2.expr_transform(preemptible_resource_count(pr1)), port16a)
port16 = port16b

port17 = hold_stream(return_expr(model, 0.123), port16)

sr = hold_server(data_type, return_expr(model, 0.456))

port18 = server_stream(sr, port17)

timer = create_arrival_timer(model, 'timer')
timer.add_result_source()

port19 = arrival_timer_stream(timer, port18)
port20 = within_stream(return_expr(model, '()'), port19)

ref = create_ref(model, 7.8, DOUBLE_TYPE, 'ref')

port21a = transform_stream(field1.expr_transform(read_ref(ref)), port20)
port21b = within_stream(write_ref(ref, return_expr(model, 9.1)), port21a)
port21 = port21b

terminate_stream(port21)

specs = Specs(0, 100, 0.1)

model.run(standalone = True, specs = specs)