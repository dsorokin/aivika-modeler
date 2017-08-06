#!/usr/local/bin/python3

from simulation.aivika.modeler import *

model = MainModel()

# the transacts can have assignable and updatable fields, but it is not used here
data_type = TransactType(model, 'Transact')

# we have two input random streams of different nature
input_stream1 = uniform_random_stream(data_type, 3, 7)
input_stream2 = exponential_random_stream(data_type, 5)

# then merge two different streams to create a new combined stream
input_stream  = merge_streams([input_stream1, input_stream2])

# this is the bounded queue with capacity = 5
queue = create_queue(model, data_type, 5, name = 'queue', descr = 'The input queue')
queue_source = queue.add_result_source()

# try to enqueue the input stream or remove the items when the queue is full
enqueue_stream_or_remove_item(queue, input_stream)

# the server represents some activivity that we model by random delays
server = exponential_random_server(data_type, 2, name = 'server', descr = 'The server')
server_source = server.add_result_source()

# it measures the processing time of transacts
timer = create_arrival_timer(model, name = 'arrivalTimer', descr = 'The arrival timer')
timer_source = timer.add_result_source()

# now we create an output stream that originates from the queue
output_stream1 = dequeue_stream(queue)
output_stream2 = server_stream(server, output_stream1)
output_stream  = arrival_timer_stream(timer, output_stream2)

# this is a terminator which may be considered as a motor of the entire model
terminate_stream(output_stream)

# reset the statistics at t = 150
reset_queue(queue, 150)
reset_server(server, 150)
reset_arrival_timer(timer, 150)

specs = Specs(0, 480, 0.1)

views = [ExperimentSpecsView(),
         InfoView(series = [timer_source, queue_source, server_source]),
         DeviationChartView(title = 'Processing Time and Queue Size',
                            left_y_series = [timer_source.processing_time],
                            right_y_series = [queue_source.count]),
         DeviationChartView(title = 'Queue Lost Item Count',
                            right_y_series = [queue_source.enqueue_lost_count]),
         DeviationChartView(title = 'Server Processing Factor',
                            right_y_series = [server_source.processing_factor]),
         FinalStatsView(title = 'Statistics Summary',
                        series = [queue_source.count_stats,
                                  queue_source.wait_time,
                                  timer_source.processing_time,
                                  server_source.processing_time,
                                  server_source.processing_factor])]

renderer = ExperimentRendererUsingDiagrams(views)

# as the simulation is quite fast, we can run 1000 simulation experiments
experiment = Experiment(renderer, run_count = 1000)

# it runs the simulation experiment by the Monte Carlo method
model.run(specs, experiment)
