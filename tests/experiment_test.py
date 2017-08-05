#!/usr/local/bin/python3

# NOTE: The model itself is quite meaningless. The purpose is
#       to check all possible cases. Consider it like an unit-test

from simulation.aivika.modeler import *

model = MainModel()

data_type = TransactType(model, 'Transact')

input_stream = uniform_random_stream(data_type, 3, 7)

input_queue = create_queue(model, data_type, 10, name = 'queue')
input_queue.add_result_source()

enqueue_stream_or_remove_item(input_queue, input_stream)

server = uniform_random_server(data_type, 1, 2, name = 'server')
server.add_result_source()

output_stream = server_stream(server, dequeue_stream(input_queue))
terminate_stream(output_stream)

specs = Specs(0, 100, 0.1)

views = [ExperimentSpecsView(title = 'Puper title', descr = 'Some long description follows...')]
renderer = ExperimentRendererUsingDiagrams(views)
experiment = Experiment(renderer, run_count = 3)

model.run(specs, experiment)
