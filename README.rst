Aivika Modeler is a discrete event simulation modeling tool for Python
======================================================================

Using Aivika Modeler, you can create quite fast discrete event simulation
models that are translated into native code. Also you can run the simulation
experiments by the Monte Carlo method, specifying that how the results should
be processed. It can plot Time Series, Deviation Chart by the confidence
interval, plot histograms, save the results in the CSV files for the
further analysis and more. All is defined in just a few lines of code written
in Python. Then the results of the simulation experiment with charts, statistics
summary and links to the saved CSV files are automatically opened in your Web
browser.

Example
-------

To take a taste of Aivika Modeler, here is a complete simulation model and
the corresponding experiment that define a simple queue network. The model
contains two generators, a bounded queue, server, the arrival timer
which measures the processing of transacts. The experiment launches
1000 simulation runs in parallel, plots charts and then opens a report with
the results of simulation in the Web browser. The compilation, simulation
and chart plotting took about 1 minute on my laptop.

.. code:: python

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
           DeviationChartView(left_y_series = [timer_source.processing_time],
                              right_y_series = [queue_source.count]),
           DeviationChartView(right_y_series = [queue_source.enqueue_lost_count]),
           DeviationChartView(right_y_series = [server_source.processing_factor]),
           FinalStatsView(series = [queue_source.count_stats,
                                    queue_source.wait_time,
                                    timer_source.processing_time,
                                    server_source.processing_time,
                                    server_source.processing_factor])]

  renderer = ExperimentRendererUsingDiagrams(views)

  # as the simulation is quite fast, we can run 1000 simulation experiments
  experiment = Experiment(renderer, run_count = 1000)

  # it runs the simulation experiment by the Monte Carlo method
  model.run(specs, experiment)

After running the simulation experiment, you will see the Deviation charts
that will show the confidence intervals by rule 3 sigma. Also you will see
a general information about the experiment as well as a summary statistics
for some properties such as the queue size, queue wait time,
the processing time of transacts and the server processing factor
in the final time point.

How does it work
----------------

The model written in Python is translated into its Haskell representation
based on using the Aivika simulation libraries, namely `aivika
<http://hackage.haskell.org/package/aivika>`_ and `aivika-transformers
<http://hackage.haskell.org/package/aivika-transformers>`_.
Then the translated model is compiled by GHC into native code and executed.
The simulation itself should be quite fast and efficient.

For the first time, the process of compiling and preparing the model
for running may take a few minutes. On next time, it may take just
a few seconds.

Installation
------------

There is one prerequisite, though. To use Aivika Modeler, you must have
`Stack <http://docs.haskellstack.org/>`_ installed on your computer.
The main operating systems are supported: Windows, Linux and macOS.

Then you can install the ``aivika-modeler`` package using *pip* in usual way.

Combining Haskell and Python
-------------------------------

In most cases you do not need to know the Haskell programming language.
The knowledge of Python will be sufficient to create and run many simulation
models. But if you will need a non-standard component, for example, to simulate
the TCP/IP protocol, then you or somebody else will have to write its
implementation in Haskell and then create the corresponding wrapper in
Python so that it would be possible to use the component from Python.

There is a separation of concerns. Python is used as a high-level glue for
combining components to build the complete simulation model, while Haskell is
used as a high-level modeling language for writing such components.

Website
--------

You can find a more full information on website `www.aivikasoft.com
<http://www.aivikasoft.com>`_.
