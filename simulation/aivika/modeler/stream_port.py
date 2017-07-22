# Copyright (c) 2017 David Sorokin <david.sorokin@gmail.com>
#
# Licensed under BSD3. See the LICENSE.txt file in the root of this distribution.

from simulation.aivika.modeler.model import *
from simulation.aivika.modeler.port import *

def expect_stream_port(port):
    """Expect the port to be a stream."""
    data_type = port.get_data_type()
    if len(data_type) == 0 or data_type[0] != 'Stream':
        raise InvalidPortException('Expected ' + port.get_name() + ' to be a stream')

def empty_stream(model, item_data_type):
    """Return an empty stream by the specified model and item data type."""
    base_comp = model.get_base_comp()
    data_type = []
    data_type.append('Stream')
    if not (base_comp is None):
        data_type.append(base_comp)
    data_type.append(item_data_type)
    y = PortOnce(model, data_type)
    y.write('return emptyStream')
    return y

def terminate_stream(port):
    """Terminate the stream."""
    expect_stream_port(port)
    model = port.get_model()
    code = 'runProcessInStartTime $ sinkStream ' + port.get_mangled_name()
    port.bind_to_output()
    model.add_action(code)

def delay_stream(delay_interval, port):
    """Delay the stream by the specified delay interval and return a new stream."""
    expect_stream_port(port)
    model = port.get_model()
    data_type = port.get_data_type()
    code = 'return $ mapStreamM (\\a -> do { holdProcess '
    code += str(delay_interval)
    code += '; return a }) '
    code += port.read()
    y = PortOnce(model, data_type)
    y.write(code)
    y.bind_to_input()
    port.bind_to_output()
    return y

def split_stream(count, port):
    """Split the stream into the specified number of output streams and return them as a list."""
    expect_stream_port(port)
    model = port.get_model()
    model.add_package_import('array')
    model.add_module_import('import Data.Functor')
    model.add_module_import('import Data.Array')
    data_type = port.get_data_type()
    code0 = 'splitStream ' + str(count) + ' ' + port.get_mangled_name()
    code0 = 'fmap (listArray (0, ' + str(count) + ' - 1)) $ ' + code0
    ys0 = PortOnce(model, data_type)
    ys0.write(code0)
    ys0.bind_to_input()
    port.bind_to_output()
    ys = [ PortOnce(model, data_type) for i in range(0, count) ]
    for i in range(0, count):
        y = ys[i]
        code = 'return $ ' + ys0.get_mangled_name() + ' ! ' + str(i)
        y.write(code)
        y.bind_to_input()
    ys0.bind_to_output()
    return ys

def merge_streams(ports):
    """Merge the list of streams in one resulting stream."""
    if len(ports) == 0:
        raise InvalidPortException('Required at least one port')
    else:
        p0 = ports[0]
        expect_stream_port(p0)
        for i in range(1, len(ports)):
            pi = ports[i]
            expect_stream_port(pi)
            if p0.get_model() != pi.get_model():
                raise InvalidPortException('Expected ports ' + p0.get_name() + ' and ' + pi.get_name() + ' to belong to the same model')
            if p0.get_data_type() != pi.get_data_type():
                raise InvalidPortException('Expected ports ' + p0.get_name() + ' and ' + pi.get_name() + ' to be of the same data type')
        model = p0.get_model()
        y = PortOnce(model, p0.get_data_type())
        for port in ports:
            port.bind_to_output()
        y.bind_to_input()
        code = ', '.join([ port.read() for port in ports ])
        code = '[' + code + ']'
        code = 'return $ mergeStreams ' + code
        y.write(code)
        return y
