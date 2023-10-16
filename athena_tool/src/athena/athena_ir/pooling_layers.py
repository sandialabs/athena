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

from enum import unique
from typing import List, Dict, Union
from . import G_PREV_LAYER_CHANNELS
from layer_types import BaseConvolutionalLayer, KnownLayerTypes
from warnings import warn


class AveragePoolLayer(BaseConvolutionalLayer):
    """
    Average Pool Layer -
    Represents an average pooling layer.
    This class converts the pooling layer into a convolutional layer
    """

    def __init__(
        self,
        stride: List,
        input_x: int,
        input_y: int,
        padding: int,
        kernel_size: Union[int, List[int]] = -1,
        layer_name="avg_pool1",
        prev_layer_channels: int = -1,
        layer_type: KnownLayerTypes = KnownLayerTypes.AVGPOOL,
    ):
        global G_PREV_LAYER_CHANNELS
        if prev_layer_channels == -1:
            prev_layer_channels = G_PREV_LAYER_CHANNELS
            self.in_channels = G_PREV_LAYER_CHANNELS
            self.out_channels = G_PREV_LAYER_CHANNELS
        else:
            self.in_channels = prev_layer_channels
            self.out_channels = prev_layer_channels

        # assert (isinstance(nn_child, torch.nn.AvgPool2d))
        try:
            stride = [stride[0], stride[1]]
        except:
            stride = [2, 2]
            warn(
                f"Pooling layer set with no stride, defaulting to 2,2:\n{layer_name=} \t {input_x=} \t {input_y=}"
            )

        if isinstance(kernel_size, int):
            if kernel_size > -1:
                kernel_size = [kernel_size, kernel_size]
            else:
                warn(f"child has no kernel size, defaulting to 1 ")
                kernel_size = [1, 1]

        padding = padding

        # TODO: Remove this once things are done.

        super().__init__(
            layer_type,
            name=layer_name,
            stride=stride,
            input_x=input_x,
            input_y=input_y,
            layer_name=layer_name,
            is_pool=True,
            net_type=KnownLayerTypes.AVGPOOL,
        )

        if not isinstance(padding, list):
            padding = [padding, padding]
        self.output_layer_size(padding=padding)
        self.input_x = input_x
        self.input_y = input_y
        self.layer_name = layer_name
        # self.h_out = int( ((input_x + 2 * padding[0] - kernel_size[0]) / stride[0]) + 1)
        # self.w_out = int( ((input_y + 2 * padding[1] - kernel_size[1]) / stride[1]) + 1)
        self.stride = stride
        self.kernel_size = kernel_size
        self.padding = padding


class MaxPoolLayer(AveragePoolLayer):
    """
    Represents a maxpool layer.
    Right now, this is assumed to be handled by lots of MACs, just like an average pooling layer.
    """

    def __init__(
        self,
        stride: List,
        input_x: int,
        input_y: int,
        padding: int,
        kernel_size: Union[int, List[int]] = -1,
        layer_name="max_pool1",
        prev_layer_channels: int = -1,
        max_bit_compare_cost=1,
        wordsize=8,
    ):
        layer_type = KnownLayerTypes.MAXPOOL
        super().__init__(
            stride,
            input_x,
            input_y,
            padding,
            kernel_size,
            layer_name,
            prev_layer_channels,
            layer_type,
        )
        # super().__init__(nn_child, input_x, input_y, layer_name)
        out_layer_sz = self.output_layer_size(self.padding)
        # self.max_ops = MaxOpRep(x_features=out_layer_sz[0],y_features=out_layer_sz[1],
        #                        channels=self.out_channels,function_type="pool",
        #                        max_bitwise_compare_cost=max_bit_compare_cost,word_size=wordsize)

    @property
    def max_pool_calc(self):
        # TODO: moved this calculation to the energy_system file, calculations are done there for max pooling.
        return 0
