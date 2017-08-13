#!/usr/local/bin/python3

# NOTE: The model itself is quite meaningless. The purpose is
#       to check some features. Consider it like an unit-test

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
port2c = hold_stream(return_expr(model, 1.5), port2a)
port1.connect_to(port2)
port4 = merge_streams([port2c, port2b])
(port5a, port5b) = clone_stream(2, port4)

port5a.connect_to(port3)

r1 = create_resource(model, 1, 'r1')
r2 = create_resource_with_max_count(model, 2, None, 'r2')
r3 = create_resource_with_max_count(model, 3, None, 'r3', queue_strategy = 'StaticPriorities')

r3.add_result_source()
reset_resource(r3, 10.0)

priority = if_expr(binary_expr(return_expr(model, 10), '<',
    binary_expr(time_expr(model), '*', int2double_expr(resource_count(r1)))),
        return_expr(model, 2),
        return_expr(model, 4))

port6a = release_resource(r3, request_resource_with_priority(r3, priority, release_resource(r1, request_resource(r1, port5b))))
port6b = transform_stream(field2.expr_transform(resource_count(r1)), port6a)
port6c = inc_resource(r2, return_expr(model, 1), port6b)
port6d = dec_resource(r2, return_expr(model, 1), port6c)
port6e = release_resource(r2, request_resource_in_parallel(r2, port6d))
port6f = release_resource(r3, request_resource_with_priority_in_parallel(r3, priority, port6e))
port6 = port6f

(port7a, port7b) = test_stream(return_expr(model, 'False'), port6)

q1 = create_queue(model, data_type, 7, 'q1')
q2 = create_unbounded_queue(model, data_type, 'q2')

reset_queue(q1, 10.0)
reset_unbounded_queue(q2, 10.0)

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
port13f = transform_stream(field1.expr_transform(arriving_time_expr(data_type)), port13e)
port13 = port13f

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

pr1 = create_preemptible_resource_with_max_count(model, 77, None, 'pr1')

reset_preemptible_resource(pr1, 10.0)

port16a = release_preemptible_resource(pr1, request_preemptible_resource_with_priority(pr1, return_expr(model, 11), port15))
port16b = transform_stream(field2.expr_transform(preemptible_resource_count(pr1)), port16a)
port16c = inc_preemptible_resource(pr1, return_expr(model, 1), port16b)
port16d = dec_preemptible_resource(pr1, return_expr(model, 1), port16c)
port16e = release_preemptible_resource(pr1, request_preemptible_resource_with_priority_in_parallel(pr1, return_expr(model, 12), port16d))
port16 = port16e

port17 = hold_stream(return_expr(model, 0.123), port16)

sr = hold_server(data_type, return_expr(model, 0.456), name = 'sr')

reset_server(sr, 10.0)

port18 = server_stream(sr, port17)

timer = create_arrival_timer(model, 'timer')
timer.add_result_source()

reset_arrival_timer(timer, 10.0)

port19 = arrival_timer_stream(timer, port18)
port20 = within_stream(return_expr(model, '()'), port19)

ref = create_ref(model, 7.8, DOUBLE_TYPE, 'ref')

port21a = transform_stream(field1.expr_transform(read_ref(ref)), port20)
port21b = within_stream(write_ref(ref, return_expr(model, 9.1)), port21a)
port21c = trace_stream(port21b)
port21d = trace_stream(port21c, request_message = 'Request')
port21e = trace_stream(port21d, request_message = 'Request', response_message = 'Response')
port21f = prefetch_stream(port21e)
port21g = filter_stream(return_expr(model, True), port21f)
port21h = take_stream_while(return_expr(model, True), port21g)
port21i = drop_stream_while(return_expr(model, False), port21h)
port21j = take_stream(100000, port21i)
port21k = drop_stream(3, port21j)
port21  = port21k

ref_stats1 = create_ref(model, EMPTY_SAMPLING_STATS, DOUBLE_SAMPLING_STATS, 'ref_stats1')
ref_stats2 = create_ref(model, EMPTY_TIMING_STATS, DOUBLE_TIMING_STATS, 'ref_stats2')

expr_stat1 = write_ref(ref_stats1,
    add_sampling_stats(return_expr(model, 1),
        read_ref(ref_stats1)))

expr_stat2 = write_ref(ref_stats2,
    add_timing_stats(return_expr(model, 2),
        read_ref(ref_stats2)))

port22a = within_stream(expr_stat1, port21)
port22b = within_stream(expr_stat2, port22a)
port22  = port22b

terminate_stream(port22)

port23 = singleton_stream(model, 12, DOUBLE_TYPE)

terminate_stream(port23)

port24 = empty_stream(model, INT_TYPE)
port24 = delay_stream(5, port24)
terminate_stream(port24)

port25 = empty_stream(model, data_type)
port25 = transform_stream(field1.expr_transform(start_time_expr(model)), port25)
port25 = transform_stream(field1.expr_transform(stop_time_expr(model)), port25)
port25 = transform_stream(field1.expr_transform(dt_expr(model)), port25)
terminate_stream(port25)

run_expr_in_start_time(return_expr(model, UNIT))
run_expr_in_stop_time(return_expr(model, UNIT))
enqueue_expr(10, return_expr(model, UNIT))

int_cell = create_ref(model, 0, INT_TYPE, name = 'int_cell')
run_expr_in_start_time(inc_ref(int_cell))
run_expr_in_start_time(dec_ref(int_cell))
run_expr_in_start_time(expr_sequence([inc_ref(int_cell)]))
run_expr_in_start_time(expr_sequence([inc_ref(int_cell), dec_ref(int_cell)]))

specs = Specs(0, 100, 0.1)

model.run(specs)
