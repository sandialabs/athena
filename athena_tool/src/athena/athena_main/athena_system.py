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
Athena System
"""
from typing import List, Tuple
from pathlib import Path
from ..athena_ir import athena_wrapper
from ..athena_ir import problem
from ..config import TLConfig, ProblemConversionMode
from enum import Enum
from ..athena_ir import accelergy_sonos_gen, timeloop_input, timeloop_output


class AthenaSystem:
    """
    Documentation - Athena System is the main object that manages the Athena state.
    Create this object, add problem layers using the athena ir tools, pass it configuration, and run / parse Athena
    """

    def __init__(
        self, system_config: TLConfig = None, max_pool_mode="batch", init_all=True
    ):
        self.config = system_config
        self.results = {}
        self.processed_cnn_list = []
        self.num_layers_processed = 0
        # For pooling calculations - need to keep track of the last layer's output channels.
        self.last_layer = None
        self.wrapper = None
        # Select output_parser based on energy system to use (Currently timeloop)
        if system_config.athena_backend == "timeloop":
            output_parser = generate
        # Select input_parser based on selected input type
        # Init athena_wrapper
        # Read input hardware def
        # Run hardware-specific init system (if needed)
        # Update athena_accelergy_plugin data with hardware-specific init data

        # ready to run

    def get_layer_stats(self, input_problem):
        self.num_layers_processed += 1
