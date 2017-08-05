#!/usr/local/bin/python3

# NOTE: The model itself is quite meaningless. The purpose is
#       to check all possible cases. Consider it like an unit-test

from simulation.aivika.modeler import *

model = MainModel()

data_type = TransactType(model, 'Transact')

input_stream = uniform_random_stream(data_type, 3, 7)

input_queue = create_queue(model, data_type, 10, name = 'queue', descr = 'The input queue')
input_queue_source = input_queue.add_result_source()

enqueue_stream_or_remove_item(input_queue, input_stream)

server = uniform_random_server(data_type, 1, 2, name = 'server', descr = 'The server')
server_source = server.add_result_source()

arrival_timer = create_arrival_timer(model, name = 'arrivalTimer', descr = 'The arrival timer')
arrival_timer_source = arrival_timer.add_result_source()

output_stream0 = dequeue_stream(input_queue)
output_stream1 = server_stream(server, output_stream0)
output_stream  = arrival_timer_stream(arrival_timer, output_stream1)

terminate_stream(output_stream)

specs = Specs(0, 100, 0.1)

views = [ExperimentSpecsView(title = 'Testing Experiment Title',
            descr = 'Some long description follows...'),
         InfoView(title = 'Testing InfoView Title',
                  descr = 'Testing InfoView Description',
                  series = [arrival_timer_source,
                            input_queue_source,
                            server_source]),
         DeviationChartView(title = 'Testing DeviationChartView Title',
                  descr = 'Testing DeviationChartView Description',
                  width = 800,
                  height = 500,
                  left_y_series = [arrival_timer_source.processing_time],
                  right_y_series = [server_source.processing_time],
                  plot_title = 'Testing Plot Title'),
         TimeSeriesView(title = 'Testing TimeSeriesView Title',
                  descr = 'Testing TimeSeriesView Description',
                  width = 800,
                  height = 500,
                  left_y_series = [arrival_timer_source.processing_time.min_value,
                                   arrival_timer_source.processing_time.max_value],
                  right_y_series = [arrival_timer_source.processing_time.mean_value],
                  plot_title = 'Testing Plot Title',
                  run_plot_title = '$PLOT_TITLE / Run $RUN_INDEX of $RUN_COUNT'),
         XYChartView(title = 'Testing XYChartView Title',
                  descr = 'Testing XYChartView Description',
                  width = 800,
                  height = 500,
                  x_series = arrival_timer_source.processing_time.mean_value,
                  left_y_series = [arrival_timer_source.processing_time.min_value,
                                   arrival_timer_source.processing_time.max_value],
                  right_y_series = [arrival_timer_source.processing_time.mean_value],
                  plot_title = 'Testing Plot Title',
                  run_plot_title = '$PLOT_TITLE / Run $RUN_INDEX of $RUN_COUNT'),
         FinalXYChartView(title = 'Testing FinalXYChartView Title',
                  descr = 'Testing FinalXYChartView Description',
                  width = 800,
                  height = 500,
                  x_series = arrival_timer_source.processing_time.mean_value,
                  left_y_series = [arrival_timer_source.processing_time.min_value,
                                   arrival_timer_source.processing_time.max_value],
                  right_y_series = [arrival_timer_source.processing_time.mean_value],
                  plot_title = 'Testing Plot Title'),
         HistogramView(title = 'Testing HistogramView Title',
                  descr = 'Testing HistogramView Description',
                  width = 800,
                  height = 500,
                  series = [arrival_timer_source.processing_time.mean_value],
                  plot_title = 'Testing Plot Title',
                  run_plot_title = '$PLOT_TITLE / Run $RUN_INDEX of $RUN_COUNT'),
         FinalHistogramView(title = 'Testing FinalHistogramView Title',
                  descr = 'Testing FinalHistogramView Description',
                  width = 800,
                  height = 500,
                  series = [arrival_timer_source.processing_time.mean_value],
                  plot_title = 'Testing Plot Title')]

renderer = ExperimentRendererUsingDiagrams(views)
experiment = Experiment(renderer, run_count = 3)

model.run(specs, experiment)
