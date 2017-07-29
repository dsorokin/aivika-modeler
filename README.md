Aivika Modeler allows building and running simulation models in Python

The model written in Python is translated into its Haskell representation 
based on using the Aivika Simulation libraries, namely 
[aivika](http://hackage.haskell.org/package/aivika) and
[aivika-transformers](http://hackage.haskell.org/package/aivika-transformers). 
Then the translated model is compiled by GHC into native code and executed. 
The simulation itself should be quite fast and efficient.

There is one prerequisite, though. To use Aivika Modeler, you must have 
[Stack](http://docs.haskellstack.org/) installed on your computer.
The main operating systems are supported: Windows, Linux and macOS.

In most cases you do not need to know the Haskell programming language. 
The knowledge of Python will be sufficient to create and run the simulation 
models.

But if you will need a non-standard component, for example, to simulate 
the TCP/IP protocol, then you or somebody else will have to write its 
implementation in Haskell and then create the corresponding wrapper in 
Python so it would be possible to use the component from Python. 

There is a separation of responsibilities. Python is used as a high-level glue for 
combining components to build the complete simulation model, while Haskell is used as 
a high-level modeling language for writing such components.

The represented Python package is under heavy development and 
is not ready for production use yet.
