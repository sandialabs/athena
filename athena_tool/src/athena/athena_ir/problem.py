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
from typing import Dict, Any, List
from enum import Enum
from bidict import bidict
import pyaml
import configparser
import torch
from typing import Union
from layer_types import BaseConvolutionalLayer, BasePoolingLayer, KnownLayerTypes

"""
Example dimensions from Timeloop scripts:
CONV:
    W, H, C, N, K, S, R, Wpad, Hpad, Wstride, Hstride
# AlexNet Layer 1:
    C, Hdilation, Hstride, M, N, P, Q, R, S, Wdilation, Wstride
    Dimensions:
        C,  M,  R,  S,  N,  P,  Q
    With explicitly defined "coefficients" and data-spaces:
        Hdilation, Hstride, Wdilation, Wstride
    
# GEMM:
    M, N, K
    With Projections (A, B, Z)

# 
## Examples from Maestro Configs:
#
Resnet50 Dimensions:
    K, C, Y, X, R, S
    
    Strides: (Redf. X, Y)
    
Network Resnet50 {
	Layer CONV1 {
		Type: CONV
		Stride { X: 2, Y: 2 }		
		Dimensions { K: 64, C: 3, R: 7, S: 7, Y:224, X:224 }
		Dataflow {
			TemporalMap (1,1) K;
			TemporalMap (1,1) C;
			TemporalMap (Sz(R),1) Y;
			SpatialMap (Sz(S),1) X;
			TemporalMap (Sz(R),Sz(R)) R;
			TemporalMap (Sz(S),Sz(S)) S;
		}
	}
	Layer FC1000 {
		Type: CONV
		Stride { X: 1, Y: 1 }		
		Dimensions { K: 1000, C: 2048, R: 7, S: 7, Y: 7, X: 7 }
		Dataflow {
			TemporalMap (1,1) K;
			TemporalMap (1,1) C;
			TemporalMap (Sz(R),1) Y;
			SpatialMap (Sz(S),1) X;
			TemporalMap (Sz(R),Sz(R)) R;
			TemporalMap (Sz(S),Sz(S)) S;
		}

	}
#####
GEMM Examples:
// BLAS 3 - Dense Matrix-Dense Matrix multiplication
// Constants are in GEMM convention; (MxK matrix) x (KxN matrix) = (MxN matrix)
Constant SzM 100;
Constant SzN 100;
Constant SzK 100;
"""


class Problem:
    """The problem class represents a complete problem for Athena to run.
    In the case of CNNs, this class contains a list of dimensions, each
    element of corresponding to a layer of the network or a GEMM operation.
    """

    def __init__(
        self,
        type=None,
        problem_list: List[Union[BaseConvolutionalLayer, BasePoolingLayer]] = None,
        name="Generic",
    ):
        """

        :param type:
        :param problem_list:
        """
        if problem_list is None:
            problem_list = []
        self.problem_layers = problem_list
        if type is None:
            type = "CNN"
        self.type = type
        self.name = name

    @property
    def problem_layers(self):
        return self._problem_list

    @problem_layers.setter
    def problem_layers(self, value):
        self._problem_list = value

    def add_problem_layer(self, layer):
        if (
            layer.type_en == KnownLayerTypes.POOL
            or layer.type_en == KnownLayerTypes.CONV
        ):
            # Check for overrides:
            if len(self.problem_layers) != 0:
                if layer.sources[0] is None:
                    layer.sources[0] = self._problem_list[-1].name
                p_layer = self._problem_list[-1]
                dest_name = layer.name
                if p_layer.destinations[0] is None:
                    p_layer.destinations.pop()
                p_layer.destinations.append(dest_name)
                self._problem_list[-1] = p_layer
        self._problem_list.append(layer)

    def to_pretty_string(self):
        prob_str = "layer #, Var"
        if len(self.problem_layers) == 0:
            return "Layer #, "

        prob_str += "\n".join(
            [
                " ".join([f"{dim}:{size}" for dim, size in layer])
                for layer in self.problem_layers
            ]
        )
        return prob_str

    def to_timeloop_cfg(self):
        return ""

    def to_timeloop_yml(self):
        return ""
