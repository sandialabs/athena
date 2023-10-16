"""
MIT License

Copyright (c) 2023 National Technology & Engineering Solutions of Sandia, LLC (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

"""
Base object containing an input reader, a set of input problem layers, a set of hardware defs, and an output object
"""


class AthenaWrapper:
    _input_problem_layers = []

    @property
    def input_problem_layers(self):
        if len(self._input_problem_layers) > 0:
            return self._input_problem_layers
        else:
            return None

    @input_problem_layers.setter
    def input_problem_layers(self, value):
        self._input_problem_layers = value

    def add_layer(self, problem_layer):
        self._input_problem_layers.append(problem_layer)

    def __init__(
        self,
        output_parser,
        input_parser=None,
        initial_input_layers=None,
        initial_hardware_config=None,
    ):
        """
        AthenaWrapper class - manages the input parsing and output generation for a given set of problem-spaces. If
        initialized with an input_parser  AthenaWrapper will use that to generate a set of layers, and hardware
        configurations.  Input_parser is optional - if not specified, a set of initial input layers and a hardware
        configuration must be specified. output_parser is used to generate the output. @see layer_types.py,
        timeloop_output.py for layers and output parsing.

        If only one of initial_input_layers or initial_hardware_config is specified, input_parser will be used
        to read the missing data.

        Args:
            input_parser: An input parser - to read in a Torch or MLIR spec
            output_parser: Output generation object - used to generate output files/data for the underlying system
            initial_input_layers: Use this to skip using the input parser.
            initial_hardware_config: Use this to skip using the input parser for hardware.
        """

        self.output_parser = output_parser
        self.input_parser = input_parser

        if initial_input_layers is not None:
            self.input_problem_layers = initial_input_layers
            self.do_read_layers = False
        else:
            self.do_read_layers = True

        if initial_hardware_config is not None:
            self.hardware_config = initial_hardware_config
            self.do_read_hardware = False
        else:
            self.do_read_hardware = True

        self.init_problem()

    def init_problem(self):
        if self.do_read_hardware:
            self.hardware_config = self.input_parser.load_hardware()
        if self.do_read_layers:
            self.input_problem_layers = self.input_parser.load_problem()

    def get_hardware_output(self):
        return self.output_parser.generate_hardware_config(self.hardware_config)

    def get_layers_output(self):
        return self.output_parser.generate_layers(self.input_problem_layers)
