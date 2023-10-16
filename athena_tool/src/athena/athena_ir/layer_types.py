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

from dataclasses import dataclass
from typing import Dict, Any, List, Mapping
import pyaml
import torch
from enum import Enum
from . import G_PREV_LAYER_CHANNELS


class KnownLayerTypes(Enum):
    BASE = 1
    CONV = 2
    POOL = 3
    AVGPOOL = 4
    MAXPOOL = 5
    GEMM = 6


@dataclass
class BaseProblemLayer:
    """
    ProblemLayer represents a layer of a problem - Either a layer of the input network or a GEMM operation.
    Problem layers contain dimensions of the input layer / problem (instance in TimeLoop)
    Also contains projection info.

    This base layer contains a generic storage format for more specialized layers which subclass this object
    """

    projection: List[Any]
    dimension_dict: Dict[str, int]
    dim_vars: List[str]
    type: str
    type_en: KnownLayerTypes

    def to_str_list(self):
        return [
            f"{dimension=}: {size=}" for dimension, size in self.dimension_dict.items()
        ]

    @property
    def type_sonos(self):
        return self.type_en.name.lower()


class BaseConvolutionalLayer(BaseProblemLayer):
    """
    BaseConvolutionalLayer represents a Convolutional layer.
    By subclassing BaseProblemLayer this class contains the basic data interface for this data,
    and allows for customized constructors.

    """

    known_types = {
        "conv2d",
        torch.nn.Conv2d,
        "conv3d",
        torch.nn.Conv3d,
        "conv1d",
        torch.nn.Conv1d,
    }
    _id = None
    _output_layer_size = []

    @property
    def in_channels(self):
        return self.dimensions["C"]

    @in_channels.setter
    def in_channels(self, value):
        self.dimensions["C"] = value

    @property
    def kernel_size(self):
        return self.dimensions["R"], self.dimensions["S"]

    @kernel_size.setter
    def kernel_size(self, value):
        self.dimensions["R"] = value[0]
        self.dimensions["S"] = value[1]

    @property
    def out_channels(self):
        return self.dimensions["K"]

    @out_channels.setter
    def out_channels(self, value):
        self.dimensions["K"] = value

    @property
    def input_size(self):
        return (self.dimensions["X"], self.dimensions["Y"])

    # TODO: Document these for overriding layer sizes (quantizaiton feature)
    @input_size.setter
    def input_size(self, value):
        self.dimensions["X"] = value[0]
        self.dimensions["Y"] = value[1]

    @property
    def stride(self):
        return self._stride

    @stride.setter
    def stride(self, value):
        self._stride["X"] = value[0]
        self._stride["Y"] = value[1]

    @property
    def name(self):
        return self.layer_name

    @name.setter
    def name(self, value):
        self.layer_name = value

    @property
    def type(self):
        return self.layer_type

    @type.setter
    def type(self, value):
        self.layer_type = value

    def __init__(
        self,
        net_type: KnownLayerTypes = KnownLayerTypes.CONV,
        name="conv_1",
        stride: Mapping[str, int] = None,
        dimensions: Mapping[str, int] = None,
        dim_vars: List[str] = None,
        bias=True,
        sources=None,
        destinations=None,
    ) -> None:
        if sources is None:
            sources = [None]
        if destinations is None:
            destinations = [None]
        self.bias = bias
        self._stride = None
        if dim_vars is None:
            dim_vars = ["G", "N", "C", "Y", "X", "K", "Y'", "X'", "R", "S"]
        if dimensions is None:
            dimensions = {"K": 32, "C": 3, "R": 1, "S": 1, "Y": 224, "X": 224}
        if stride is None:
            stride = {"X": 2, "Y": 2}
        self._stride = stride
        self.name = name
        self.dimensions = dimensions
        self.dim_vars = dim_vars
        self.sources = sources
        self.destinations = destinations

        self.layer_type = net_type

        # super(BaseConvolutionalLayer, self).__init__([], dimensions, dim_vars, net_type, kt)

    def output_layer_size(self, padding: list = None) -> list:
        if padding is None:
            padding = [0, 0]
        elif isinstance(padding, int):
            padding = [padding, padding]
        if len(self._output_layer_size) == 0:
            w_o = (
                self.input_size[0] - self.kernel_size[0] + (2 * padding[0])
            ) / self.stride["X"] + 1
            h_o = (
                self.input_size[1] - self.kernel_size[1] + (2 * padding[1])
            ) / self.stride["Y"] + 1
            self._output_layer_size = [w_o, h_o]
            return [w_o, h_o]
        else:
            return self._output_layer_size

    @property
    def name(self):
        return self.layer_name

    @name.setter
    def name(self, value):
        self.layer_name = value

    def __str__(self):
        return " ".join([f"{k},{v}" for k, v in self.__dict__.items()])
