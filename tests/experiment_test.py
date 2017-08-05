#!/usr/local/bin/python3

# NOTE: The model itself is quite meaningless. The purpose is
#       to check all possible cases. Consider it like an unit-test

from simulation.aivika.modeler import *

model = MainModel()

data_type = TransactType(model, 'Transact')

input_stream = uniform_random_stream(data_type, 3, 7)

input_queue = create_queue(model, data_type, 10, name = 'queue')
input_queue_source = input_queue.add_result_source()

enqueue_stream_or_remove_item(input_queue, input_stream)

server = uniform_random_server(data_type, 1, 2, name = 'server')
server_source = server.add_result_source()

arrival_timer = create_arrival_timer(model, name = 'arrivalTimer')
arrival_timer_source = arrival_timer.add_result_source()

output_stream0 = server_stream(server, dequeue_stream(input_queue))
output_stream  = arrival_timer_stream(arrival_timer, output_stream0)

terminate_stream(output_stream)

specs = Specs(0, 100, 0.1)

unbounded_queue = create_unbounded_queue(model, data_type, name = 'unboundedQueue')
unbounded_queue_source = unbounded_queue.add_result_source()

views = [ExperimentSpecsView(title = 'Puper title',
            descr = 'Some long description follows...'),
         TableView(title = 'Some table',
                   descr = 'Some description',
                   series = [input_queue_source,
                             server_source],
                   separator = ';',
                   link_text = 'Download the CSV file',
                   run_link_text = '$LINK / Run $RUN_INDEX of $RUN_COUNT'),
         TableView(title = 'Testing Queue Properties',
                   series = input_queue_source.expand_results()),
         TableView(title = 'Testing Unbounded Queue Properties',
                   series = unbounded_queue_source.expand_results()),
         TableView(title = 'Testing Server Properties',
                   series = server_source.expand_results()),
         TableView(title = 'Testing Arrival Timer Properties',
                   series = arrival_timer_source.expand_results())]

renderer = ExperimentRendererUsingDiagrams(views)
experiment = Experiment(renderer, run_count = 3)

model.run(specs, experiment)
