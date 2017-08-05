Aivika Modeler allows building and running discrete event simulation models in Python
=====================================================================================

Using Aivika Modeler, you can create fast enough discrete event simulation
models that are executed in native code. Also you can run the simulation
experiments by the Monte Carlo method, specifying that how the results should 
be processed. It can plot Time Series, Deviation Chart by the confidence
interval, plot histograms, save the results in the CSV files for the 
further analysis and more. All is defined in just a few lines of code written 
in Python. Then the results of the simulation experiment with charts, statistics 
summary and links to the saved CSV files is automatically opened in the Web 
browser.

The model written in Python is translated into its Haskell representation 
based on using the Aivika simulation libraries, namely `aivika 
<http://hackage.haskell.org/package/aivika>`_ and `aivika-transformers 
<http://hackage.haskell.org/package/aivika-transformers>`_. 
Then the translated model is compiled by GHC into native code and executed. 
The simulation itself should be quite fast and efficient.

For the first time, the process of compiling and preparing the model 
for running may take a few minutes. On next time, it may take just 
a few seconds.

There is one prerequisite, though. To use Aivika Modeler, you must have 
`Stack <http://docs.haskellstack.org/>`_ installed on your computer.
The main operating systems are supported: Windows, Linux and macOS.

In most cases you do not need to know the Haskell programming language. 
The knowledge of Python will be sufficient to create and run the simulation 
models. But if you will need a non-standard component, for example, to simulate 
the TCP/IP protocol, then you or somebody else will have to write its 
implementation in Haskell and then create the corresponding wrapper in 
Python so that it would be possible to use the component from Python. 

There is a separation of concerns. Python is used as a high-level glue for 
combining components to build the complete simulation model, while Haskell is 
used as a high-level modeling language for writing such components.

You can find a more full information on website `www.aivikasoft.com
<http://www.aivikasoft.com>`_.
