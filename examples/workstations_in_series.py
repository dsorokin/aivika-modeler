#!/usr/local/bin/python3

# Example: Work Stations in Series
#
#   This is a model of two work stations connected in a series and separated by
#   finite queues. It is described in different sources [1, 2]. So, this is
#   chapter 7 of [2] and section 5.14 of [1].
#
#   [1] A. Alan B. Pritsker, Simulation with Visual SLAM and AweSim, 2nd ed.
#
#   [2] Труб И.И., Объектно-ориентированное моделирование на C++: Учебный
#       курс. - СПб.: Питер, 2006
#
# The maintenance facility of a large manufacturer performs two operations.
# These operations must be performed in series; operation 2 always follows
# operation 1. The units that are maintained are bulky, and space is available
# for only eight units including the units being worked on. A proposed design
# leaves space for two units between the work stations, and space for four units
# before work station 1. [..] Current company policy is to subcontract
# the maintenance of a unit if it cannot gain access to the in-house facility.

# Historical data indicates that the time interval between requests for
# maintenance is exponentially distributed with a mean of 0.4 time units.
# Service times are also exponentially distributed with the first station
# requiring on the average 0.25 time units and the second station, 0.5 time
# units. Units are transported automatically from work station 1 to work
# station 2 in a negligible amount of time. If the queue of work station 2 is
# full, that is, if there are two units awaiting for work station 2, the first
# station is blocked and a unit cannot leave the station. A blocked work
# station cannot server other units.

from simulation.aivika.modeler import *

model = MainModel()

# the transacts can have assignable and updatable fields, but it is not used here
data_type = TransactType(model, 'Transact')

# it will help us to measure the processing time of transacts
timer = create_arrival_timer(model, name = 'timer', descr = 'Measures the processing time')
timer_source = timer.add_result_source()

# this is a generator of transacts
input_stream = exponential_random_stream(data_type, 0.4)

# a queue before the first workstation
queue1 = create_queue(model, data_type, 4, name = 'queue1', descr = 'Queue no. 1')
queue1_source = queue1.add_result_source()

# another queue before the second workstation
queue2 = create_queue(model, data_type, 2, name = 'queue2', descr = 'Queue no. 2')
queue2_source = queue2.add_result_source()

# the first workstation activity is modeled by the server
workstation1 = exponential_random_server(data_type, 0.25, name = 'workstation1', descr = 'Workstation no. 1')
workstation1_source = workstation1.add_result_source()

# this is the second workstation
workstation2 = exponential_random_server(data_type, 0.5, name = 'workstation2', descr = 'Workstation no. 2')
workstation2_source = workstation2.add_result_source()

# try to enqueue the arrivals; otherwise, count them as lost
enqueue_stream_or_remove_item(queue1, input_stream)

# a chain of streams originated from the first queue
stream2 = dequeue_stream(queue1)
stream3 = server_stream(workstation1, stream2)
enqueue_stream(queue2, stream3)

# another chain of streams, which must be terminated already
stream4 = dequeue_stream(queue2)
stream5 = server_stream(workstation2, stream4)
stream5 = arrival_timer_stream(timer, stream5)
terminate_stream(stream5)

# reset the statistics after 30 time units
reset_time = 30
reset_queue(queue1, 0)
reset_queue(queue2, 0)
reset_server(workstation1, 0)
reset_server(workstation2, 0)
reset_arrival_timer(timer, 0)

# it defines the simulation specs
specs = Specs(0 - reset_time, 300, 0.1)

processing_factors = [workstation1_source.processing_factor,
    workstation2_source.processing_factor]

# define what to display in the report
views = [ExperimentSpecsView(),
         InfoView(),
         FinalStatsView(title = 'Processing Time (Statistics Summary)',
            series = [timer_source.processing_time]),
         DeviationChartView(title = 'Processing Factor (Chart)',
            right_y_series = processing_factors),
         FinalHistogramView(title = 'Processing Factor (Histogram)',
            series = processing_factors),
         FinalStatsView(title = 'Processing Factor (Statistics Summary)',
            series = processing_factors),
         FinalStatsView(title = 'Lost Items (Statistics Summary)',
            series = [queue1_source.enqueue_lost_count]),
         DeviationChartView(title = 'Queue Size (Chart)',
            right_y_series = [queue1_source.count,
                              queue2_source.count]),
         FinalStatsView(title = 'Queue Size (Statistics Summary)',
            series = [queue1_source.count_stats,
                      queue2_source.count_stats]),
         DeviationChartView(title = 'Queue Wait Time (Chart)',
            right_y_series = [queue1_source.wait_time,
                              queue2_source.wait_time]),
         FinalStatsView(title = 'Queue Wait Time (Statistics Summary)',
            series = [queue1_source.wait_time,
                      queue2_source.wait_time])]

# it will render the report
renderer = ExperimentRendererUsingDiagrams(views)

# it defines the simulation experiment with 1000 runs
experiment = Experiment(renderer, run_count = 1000)

# it compiles the model and runs the simulation experiment
model.run(specs, experiment)
