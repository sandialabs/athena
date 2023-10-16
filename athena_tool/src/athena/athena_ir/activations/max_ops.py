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


class MaxOpRep:
    """
    Object that represents a custom-implemented Max function.
    This object computes the number of bits compared based on the operation, the style
    of implementation, and the number of bits used to represent a feature.

    Used by MaxPoolLayer and ReLU values currently.
    """

    known_modifiers = ["batch", "stream"]

    def __init__(
        self,
        x_features=128,
        y_features=128,
        channels=3,
        function_type="ReLU",
        max_bitwise_compare_cost=1,
        max_bitwise_relu_cost=1,
        word_size=32,
        num_out_channels=3,
        mod_type="batch",
        num_batch_grouped_features=0,
    ):
        self.max_bitwise_compare_cost = max_bitwise_compare_cost
        self.max_bitwise_relu_cost = max_bitwise_relu_cost
        self.word_size = word_size

        self.total_features = x_features * y_features * channels
        self.x_features = x_features
        self.y_features = y_features
        self.channels = channels
        self.function_type = function_type
        self.mod_type = mod_type
        valid = any([x in mod_type.lower() for x in self.known_modifiers])
        if not valid:
            raise RuntimeError(
                "Invalid mod type given to max op stat object " + mod_type
            )

        self.total_feature_ops = x_features * y_features * channels
        self.num_out_channels = num_out_channels

        self.num_features_at_once = num_batch_grouped_features

    def __stat_gen(self, feat, bit, lat):
        return {"comp": [feat, bit], "latency": lat}

    def _relu_batch_gen(self):
        pass

    def _relu_stream_gen(self):
        pass

    def _pool_batch_gen(self):
        """
        computes the total number of compare ops,
        based on the naive comparison: input_x_features * input_y_features * channels

        :return:
        """
        if self.num_features_at_once == 0:
            total_feature_ops = self.total_feature_ops
        else:
            total_feature_ops = self.total_feature_ops / self.num_features_at_once

        bitwise_ops = total_feature_ops * self.word_size * self.max_bitwise_compare_cost
        latency = 1  # @TODO: Add dynamic latency calculations
        return self.__stat_gen(total_feature_ops, bitwise_ops, latency)

    def _pool_stream_gen(self):
        """
        Computes the total number of compare ops (Max operations)
        Assumes that the data is streamed to the dedicated hardware.
        |z_1| -> ReLu -> |out mem|
        |z_2| ->
        |z_3|
        :return:
        """
        pass

    def _relu_op_stats(self):
        if "stream" in self.mod_type:
            return self._relu_stream_gen()
        else:
            return self._relu_batch_gen()

    def _pool_op_stats(self):
        if "stream" in self.mod_type:
            return self._pool_batch_gen()
        else:
            return self._pool_batch_gen()

    def get_num_comps(self):
        if self.function_type is "pool":
            return self._pool_op_stats()["comp"]
        elif self.function_type is "relu":
            return self._relu_op_stats()

    def get_latency(self):
        if self.function_type is "pool":
            return self._pool_op_stats()["latency"]


def test_max_op():
    pass
