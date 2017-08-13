#!/usr/local/bin/python3

# NOTE: The model itself is quite meaningless. The purpose is
#       to check some features. Consider it like an unit-test

from simulation.aivika.modeler import *

model = MainModel()
submodel1 = SubModel(model, name = 'submodel1')
submodel2 = SubModel(submodel1, name = 'submodel2')

data_type = TransactType(model, 'Transact')

input_stream = uniform_random_stream(data_type, 3, 7)

input_queue = create_queue(submodel1, data_type, 10, name = 'queue', descr = 'The input queue')
input_queue_source = input_queue.add_result_source()

enqueue_stream_or_remove_item(input_queue, input_stream)

server = uniform_random_server(data_type, 1, 2, name = 'server', descr = 'The server')
server_source = server.add_result_source()

arrival_timer = create_arrival_timer(submodel2, name = 'arrivalTimer', descr = 'The arrival timer')
arrival_timer_source = arrival_timer.add_result_source()

output_stream0 = dequeue_stream(input_queue)
output_stream1 = server_stream(server, output_stream0)
output_stream  = arrival_timer_stream(arrival_timer, output_stream1)

terminate_stream(output_stream)

specs = Specs(0, 100, 0.1)

model.run(specs)
