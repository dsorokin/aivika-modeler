Aivika Modeler is a simulation modeling tool for Python
=======================================================

Using Aivika Modeler, you can create quite fast discrete event simulation
models that are translated into native code. Also you can run the simulation
experiments by the Monte Carlo method, specifying that how the results should
be processed. It can plot Time Series, Deviation chart by the confidence
interval, plot histograms, save the results in the CSV files for the
further analysis and more. All is defined in just a few lines of code written
in Python. Then the report of the simulation experiment with charts, statistics
summary and links to the saved CSV files is automatically opened in your Web
browser.

Example
-------

To take a taste of Aivika Modeler, here is a complete simulation model and
the corresponding experiment that define a simple queue network. The model
contains a transact generator, two bounded queues, two servers and the arrival
timer that measures the processing of transacts. The experiment launches
1000 simulation runs in parallel, plots charts and then opens a report with
the results of simulation in the Web browser. The compilation, simulation
and chart plotting took about 1 minute on my laptop.

  Example: *Work Stations in Series*

  This is a model of two work stations connected in a series and separated by
  finite queues. It is described in different sources [1, 2]. So, this is
  chapter 7 of [2] and section 5.14 of [1].

  [1] A. Alan B. Pritsker, Simulation with Visual SLAM and AweSim, 2nd ed.

  [2] Труб И.И., Объектно-ориентированное моделирование на C++: Учебный курс. - СПб.: Питер, 2006

  The maintenance facility of a large manufacturer performs two operations.
  These operations must be performed in series; operation 2 always follows
  operation 1. The units that are maintained are bulky, and space is available
  for only eight units including the units being worked on. A proposed design
  leaves space for two units between the work stations, and space for four units
  before work station 1. [..] Current company policy is to subcontract
  the maintenance of a unit if it cannot gain access to the in-house facility.

  Historical data indicates that the time interval between requests for
  maintenance is exponentially distributed with a mean of 0.4 time units.
  Service times are also exponentially distributed with the first station
  requiring on the average 0.25 time units and the second station, 0.5 time
  units. Units are transported automatically from work station 1 to work
  station 2 in a negligible amount of time. If the queue of work station 2 is
  full, that is, if there are two units awaiting for work station 2, the first
  station is blocked and a unit cannot leave the station. A blocked work
  station cannot server other units.

.. code:: python

  #!/usr/local/bin/python3

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

After running the simulation experiment, you will see the Deviation charts
that will show the confidence intervals by rule 3 sigma. Also you will see
a general information about the experiment as well as histograms and summary
statistics sections for some properties such as the queue size, queue wait time,
the processing time of transacts and the server processing factor
in the final time point.

How It Works
------------

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
