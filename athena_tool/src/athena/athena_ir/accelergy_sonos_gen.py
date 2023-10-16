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

from problem import Problem
from layer_types import BaseConvolutionalLayer
import yaml
from pathlib import Path
from sonos_accelerator.buildAccelerator import (
    allocateHardware,
    allocateTiles,
    calculateTileEnergyArea,
)

max_cols = 257
max_rows = 1151


class SonosAccelergy:
    def __init__(
        self,
        problem: Problem,
        topology_template_path="../../../accelergy_architectures/sonos_pim/arch/system_SONOS.yaml",
        tile_template_path="./data/tile.yaml",
        destination_arch_path="../../../generated_sonos_arch",
    ):
        self.layer_params = None
        self.arch_params = None
        self.tiles = None
        self.area_layers = None
        self.nn_layers = None
        self.problem = problem
        self.topology_template_path = Path(topology_template_path).absolute()
        self.tile_template_path = Path(tile_template_path).absolute()
        self.destination_arch_path = Path(destination_arch_path).absolute()
        self.topology_template = yaml.load(open(self.topology_template_path, "r"))
        self.tile_template = yaml.load(open(self.tile_template_path, "r"))

    def compute_topology(self, default_dims=None, activation=True):
        if default_dims is None:
            default_dims = [1152, 256]
        layers = []
        layer_num = 0
        problem = self.problem
        for layer in problem.problem_layers:
            out_layer = {}
            if "conv" in layer.name.lower():
                out_layer["type"] = layer.type_sonos

                out_layer["name"] = layer.name

            if layer_num == 0:
                out_layer["signedInputs"] = True
            else:
                out_layer["signedInputs"] = False

            out_layer["Kx"] = layer.kernel_size[0]
            out_layer["Ky"] = layer.kernel_size[0]
            out_layer["S"] = layer.dimensions["S"]
            out_layer["bias"] = layer.bias
            out_layer["Sources"] = layer.sources
            out_layer["Destinations"] = layer.destinations
            out_size = layer.output_layer_size()
            out_layer["Nix"] = layer.input_size[0]
            out_layer["Niy"] = layer.input_size[1]
            out_layer["Nic"] = layer.in_channels
            out_layer["Nox"] = out_size[0]
            out_layer["Noy"] = out_size[1]
            out_layer["Noc"] = layer.out_channels
            out_layer["Nweights"] = (
                out_layer["Kx"] * out_layer["Ky"] * out_layer["Nic"] + 1
            ) * out_layer["Noc"]
            out_layer["Nmacs"] = (
                out_layer["Nweights"] * out_layer["Nox"] * out_layer["Noy"]
            )

            layers.append(out_layer)
            layer_num += 1

        arch_params = {
            "SWorder": 2,
            "memorySizeKb": 64,
            "receiveBufferSizeKb": 8,
            "tileOutBufferSizeKb": 4,
            "maxMPoutputs": 1000,
            "Nbc_pool_factor": 50000,
            "A_router": 107526e-12,
            "P_router": 11.8e-3 * 2,
            "model": problem.name,
            "ArrayDims": default_dims,
            "NoutputsTile": 1024,
            "heterogeneousTiling": False,
            "Ncycles_target": 32,
            "Nbits": 8,
            "Nbanks": 32,
            "Ncycles_machine": 295,
            "digital_bias": True,
            "t_clk": 1e-9,
            "I_read": 3200e-9,
            "Vdd_digital": 1.1,
            "Vdd_analog": 2.5,
            "Vref": 1.0,
            "CoreOutKb": 1.0,
            "A_lowV": 0.15e-12,
            "A_highV": 0.653e-12,
            "area_fraction_wiring": 0.2500,
            "area_fraction_control": 0.0500,
            "NcoreOut_cycle": 8,
            "Nwrite_inputReg": 8,
            "Nread_outputReg": 16,
            "Nread_tileOut": 16,
            "Nports_receiveBuffer": 16,
            "useShiftRegisters": True,
            "weightReorder": True,
            "Nimages": 1,
            "Ncycles_delay": 0,
        }

        # Process

        # Area inflation factors:
        # 1) area_fraction_wiring is % of area dedicated to wiring/layout overhead in certain blocks
        # 	Applied everywhere except SONOS array and SRAM
        # 2) area_fraction_control is % of tile area dedicated to control unit and instruction memory

        # Data widths

        # Other settings

        nn_layers, layer_params, arch_params = allocateHardware(layers, arch_params)
        nn_layers, layer_params, tiles = allocateTiles(
            nn_layers, layer_params, arch_params
        )
        layer_params, arch_params, area_layers = calculateTileEnergyArea(
            layer_params, layers, arch_params
        )

        self.layer_params = layer_params
        self.arch_params = arch_params
        self.tiles = tiles
        self.area_layers = area_layers
        self.nn_layers = nn_layers

        return nn_layers, layer_params, arch_params, tiles

    def generate_tile(self, num, scratchpad_parms, mac_parms):
        template = self.tile_template.copy()
        template = template[0]
        template["name"] = f"PE{num}"
        for k, v in scratchpad_parms.items():
            template["local"][0]["attributes"][k] = v
        for k, v in mac_parms.items():
            template["local"][1]["attributes"][k] = v
            template["local"][1]["arguments"][k] = v

        return template

    def generate_multi_tile(self, num_total, scratchpad_parms, mac_parms):
        return self.generate_tile(f"0..{num_total}", scratchpad_parms, mac_parms)

    def generate_layer_tiles(self, layer_number):
        mem_args = {}
        compute_args = {}
        layer_elms = ["NcolsActive", "NrowsActive", "Ntiles"]
        ram_energy_elms = [k for k in self.arch_params.keys() if "RAM" in k]

    def generate_accelergy_yaml_per_layer(self, layers):
        topology_path = Path(self.topology_path).absolute()
        print(f"{topology_path=}")
        print(f"{topology_path.exists()}")
        arch_dict = yaml.load(open(topology_path, "r"))
        dest_folder = topology_path.absolute().parent
        subtree_tile = arch_dict
        tile_template = yaml.load(open(self.tile_template_path, "r"))
        chip = arch_dict["architecture"]["subtree"][0]["subtree"][0]["subtree"]

        chip.pop()
        chip.pop()


if __name__ == "__main__":
    test_layer1 = BaseConvolutionalLayer("conv2d", name="conv1")
    test_layer2 = BaseConvolutionalLayer(name="conv2")
    test_problem = Problem()
    test_problem.add_problem_layer(test_layer1)
    test_problem.add_problem_layer(test_layer2)
    topo = SonosAccelergy(problem=test_problem)

    l, p, a, tiles = topo.compute_topology()
    print("enable")
    # generate_accelergy_yaml_per_layer(l, p, a, tiles)
