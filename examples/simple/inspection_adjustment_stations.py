#!/usr/local/bin/python3

# Example: Inspection and Adjustment Stations on a Production Line
#
#   This is a model of the workflow with a loop. Also there are two infinite
#   queues.
#
#   It is described in different sources [1, 2]. So, this is chapter 8 of [2]
#   and section 5.15 of [1].
#
#  [1] A. Alan B. Pritsker, Simulation with Visual SLAM and AweSim, 2nd ed.
#
#  [2] Труб И.И., Объектно-ориентированное моделирование на C++: Учебный
#      курс. - СПб.: Питер, 2006
#
# Assembled television sets move through a series of testing stations in
# the final stage of their production. At the last of these stations,
# the vertical control setting on the TV sets is tested. If the setting is
# found to be functioning improperly, the offending set is routed to
# an adjustment station where the setting is adjusted. After adjustment,
# the television set is sent back to the last inspection station where
# the setting is again inspected. Television sets passing the final inspection
# phase, whether for the first time of after one or more routings through
# the adjustment station, are routed to a packing area.
#
# The time between arrivals of television sets to the final inspection station
# is uniformly distributed between 3.5 and 7.5 minutes. Two inspectors work
# side-by-side at the final inspection station. The time required to inspect
# a set is uniformly distributed between 6 and 12 minutes. On the average,
# 85 percent of the sets are routed to the adjustment station which is manned
# by a single worker. Adjustment of the vertical control setting requires
# between 20 and 40 minutes, uniformly distributed.
#
# The inspection station and adjustor are to be simulated for 480 minutes
# to estimate the time to process television sets through the final production
# stage and to determine the utilization of the inspectors and the adjustors.

from simulation.aivika.modeler import *

model = MainModel()

transact_type = TransactType(model, 'Transact')

specs = Specs(0, 480, 0.1)

input_arrival_timer = create_arrival_timer(model,
    name = 'input_arrival_timer', descr = 'Measures the Input')
input_arrival_timer.add_result_source()

output_arrival_timer = create_arrival_timer(model,
    name = 'output_arrival_timer', descr = 'Measures the Output')
output_arrival_timer.add_result_source()

input_stream = uniform_random_stream(transact_type, 3.5, 7.5)

inspection_queue = create_unbounded_queue(model, transact_type,
    name = 'inspection_queue', descr = 'Inspection Queue')
inspection_queue.add_result_source()

adjustment_queue = create_unbounded_queue(model, transact_type,
    name = 'adjustment_queue', descr = 'Adjustment Queue')
adjustment_queue.add_result_source()

inspection_station_1 = uniform_random_server(transact_type, 6.0, 12.0,
    name = 'inspection_station_1', descr = 'Inspection Station no. 1')
inspection_station_1.add_result_source()

inspection_station_2 = uniform_random_server(transact_type, 6.0, 12.0,
    name = 'inspection_station_2', descr = 'Inspection Station no. 2')
inspection_station_2.add_result_source()

adjustment_station = uniform_random_server(transact_type, 20.0, 40.0,
    name = 'adjustment_station', descr = 'Adjustment Station')
adjustment_station.add_result_source()

s01 = unbounded_dequeue_stream(inspection_queue)
(s02_1, s02_2) = split_stream(2, s01)
s03_1 = server_stream(inspection_station_1, s02_1)
s03_2 = server_stream(inspection_station_2, s02_2)
s04 = merge_streams([s03_1, s03_2])

test_expr = binary_expr(uniform_random_expr(model, 0.0, 1.0), '<=',
    return_expr(model, 0.85))

(passed_stream, failed_stream) = test_stream(test_expr, s04)

terminate_stream(arrival_timer_stream(output_arrival_timer, passed_stream))
unbounded_enqueue_stream(adjustment_queue, failed_stream)

s05 = unbounded_dequeue_stream(adjustment_queue)
s06 = server_stream(adjustment_station, s05)

unbounded_enqueue_stream(inspection_queue, s06)

s07 = arrival_timer_stream(input_arrival_timer, input_stream)

unbounded_enqueue_stream(inspection_queue, s07)

model.run(specs)
