# Copyright (c) 2020 Yannan Wu
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import gc
import time
from typing import Union
from mpmath import mpf

import pandas as pd
import numpy as np
from pathlib import Path
from pathlib import Path
import pyaml
from diskcache import Cache
from io import StringIO

# timer.py

from contextlib import ContextDecorator
from dataclasses import dataclass, field
import time
from typing import Any, Callable, ClassVar, Dict, Optional


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


@dataclass
class Timer(ContextDecorator):
    """Time your code using a class, context manager, or decorator"""

    timers: ClassVar[Dict[str, float]] = dict()
    name: Optional[str] = None
    text: str = "Elapsed time: {:0.4f} seconds"
    logger: Optional[Callable[[str], None]] = print
    _start_time: Optional[float] = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        """Initialization: add timer to dict of timers"""
        if self.name:
            self.timers.setdefault(self.name, 0)

    def start(self) -> None:
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter_ns()

    def stop(self) -> float:
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        # Calculate elapsed time
        elapsed_time = time.perf_counter_ns() - self._start_time
        elapsed_time = mpf(elapsed_time) * mpf(1e-9)
        elapsed_time = np.float(elapsed_time)

        self._start_time = None

        # Report elapsed time
        if self.logger:
            self.logger(self.text.format(elapsed_time))
        if self.name:
            self.timers[self.name] += elapsed_time

        return elapsed_time

    def __enter__(self) -> "Timer":
        """Start a new timer as a context manager"""
        self.start()
        return self

    def __exit__(self, *exc_info: Any) -> None:
        """Stop the context manager timer"""
        self.stop()


# memoization
et_cache = Cache("./cache_ert")
rt_cache = Cache("./cache_rt")

SRAM_hardcode = StringIO(
    """technology,datawidth,width,depth,latency,action,address_delta,data_delta,energy,area,comment
32nm,16,16,1152,1ns,read,1,1,1.23E+00,2870,energy in pJ;  area in um^2
32nm,16,16,1152,1ns,write,1,1,1.23E+00,2870,
32nm,16,16,1024,1ns,read,1,1,1.03E+00,2100,
32nm,16,16,1024,1ns,write,1,1,1.03E+00,2100,
32nm,16,16,128,1ns,read,1,1,1.92E-01,770,
32nm,16,16,128,1ns,write,1,1,1.92E-01,770,
32nm,16,16,128,1ns,idle,1,1,0,0,
"""
)


def mprint(*args, **kwargs):
    return
    if len(args) > 1 and isinstance(args[1], bool):
        print(*args)


def find_neighbours(value, df, colname):
    exactmatch = df[df[colname] == value]
    if not exactmatch.empty:
        return exactmatch.index
    else:
        lowerneighbour_ind = df[df[colname] < value][colname].idxmax()
        upperneighbour_ind = df[df[colname] > value][colname].idxmin()
        return [lowerneighbour_ind, upperneighbour_ind]


# ========================================================================
PLUG_IN_ACCURACY = 90  # Please set the accuracy of your plug-in here


# ========================================================================
@et_cache.memoize()
def generate_energy_table(arch_params, area_data, technology, actions):
    formed_data = {
        "technology": [],
        "active_cols": [],
        "allow_negatives": [],
        "active_rows": [],
        "energy": [],
        "area": [],
        "action": [],
    }
    row_num = 0
    tech_row = 0
    action_row = 0

    lut_size = len(arch_params.items()) * list(arch_params.values())[0].shape[0]

    num_actions = len(actions) % lut_size
    print(f"num actions in table: {num_actions}")
    print(f"{len(actions)=}")
    # if len(actions) < lut_size:
    #     num_actions = lut_size
    # print(f'total: {num_actions=}')
    while num_actions > 0:
        for k, v in arch_params.items():
            ncols = int(k)
            allow_negatives = 0 if ncols < 0 else 1
            ncols = abs(ncols)
            row_num = row_num % len(area_data)
            tech_row = (
                tech_row % len(technology) if isinstance(technology, np.ndarray) else 0
            )
            action_row = (
                action_row % len(actions) if isinstance(actions, np.ndarray) else 0
            )
            for active_rows in range(v.shape[0]):
                energy = v[active_rows]
                area = area_data[row_num]
                formed_data["active_cols"].append(ncols)
                formed_data["allow_negatives"].append(allow_negatives)
                formed_data["active_rows"].append(active_rows)
                formed_data["energy"].append(energy)
                if isinstance(technology, list) or isinstance(technology, np.ndarray):
                    tech = technology[tech_row]
                else:
                    tech = technology
                formed_data["technology"].append(tech)
                formed_data["area"].append(area)
                if isinstance(actions, np.ndarray):
                    action = actions[action_row]
                else:
                    action = actions
                formed_data["action"].append(action)
            row_num += 1
            tech_row += 1
        num_actions -= 1
        action_row += 1
    formed_data = pd.DataFrame(formed_data)

    return formed_data


class SonosEstimator:
    # an estimation plug-in wrapper class that implements the necessary interface functions for Accelergy-Plugin communications
    _SRAM_table = None

    @property
    def SRAM_table(self):
        # TODO: Move from hardcoded values
        if self._SRAM_table is None:
            self._SRAM_table = pd.read_csv(SRAM_hardcode)

        return self._SRAM_table

    @SRAM_table.setter
    def SRAM_table(self, value):
        self._SRAM_table = value

    # -------------------------------------------------------------------------------------
    # Interface functions below,
    #   function name, input arguments, and output format CANNOT be changed
    # -------------------------------------------------------------------------------------
    def __init__(
        self,
        storage_lut_location=None,
        compute_lut_location=str(Path(__file__).parent) + "/analog_core/sonos_luts.npz",
        generated_sonos_data_file="./sonos_arch_detail.yaml",
    ):
        """ " initialize function that will be called inside Accelergy to instantiate the estimation plug-in"""
        self.estimator_name = "sonos_estimator"  # please enter your plug-in's name here
        self.time = Timer("Athena energy estimate")
        self.time.start()
        # Start timer:
        with Timer(name="System init"):
            start_time = time.perf_counter_ns()
            mprint("ACCELERGY", True)

            if storage_lut_location is None:
                storage_lut_location = (
                    str(Path(__file__).parent) + "/sonos_cell_storage.csv"
                )

            self.compute_lut = compute_lut_location

            # compute_lut_location = str(Path(__file__).parent) + '/sonos_compute.csv'
            # self.compute_lut = pd.read_csv(compute_lut_location)

            self.storage_lut = pd.read_csv(storage_lut_location)
            self.supported_types = [
                "sonos_cell_storage",
                "sonos_compute",
                "sonos_dummy_storage",
                "sonos_cell_dummy",
            ]

            gsdf = Path(generated_sonos_data_file)
            if gsdf.exists():
                self.system_data = gsdf
                self.custom_sonos = True
            else:
                self.system_data = None
                self.custom_sonos = False

            self.local_log = {"entries": [], "values": []}

            end_time = time.perf_counter_ns()
            print(f"Init complete. Took {end_time - start_time} ")

    compute_lut_data = None
    _compute_lut_pd = None

    @property
    def compute_lut(self):
        return self._compute_lut_pd

    @compute_lut.setter
    def compute_lut(self, value: Union[str, pd.DataFrame]):
        if isinstance(value, str):
            if ".csv" in value:
                self._compute_lut_pd = pd.read_csv(value)
            else:
                d = np.load(Path(value), allow_pickle=True)
                # self.compute_lut_data = d['tile_mvm_energy']
                self.compute_lut_data = d["tile_mvm_energy"].item()
                self.technology = d["technology"].item()
                try:
                    self.area_lut_data = d["tile_area"].item()
                except ValueError:
                    self.area_lut_data = d["tile_area"]

                self.init_numpy_data(data_type="compute", d=d)
        else:
            self._compute_lut_pd = value

    def init_numpy_data(self, data_type, d):
        if data_type == "compute":
            energy_data = self.compute_lut_data
            self._compute_lut_pd = generate_energy_table(
                energy_data, self.area_lut_data, self.technology, d["action"]
            )

    def is_supported(self, cname, tv="na"):
        supported = False
        if cname == "dummy_storage" and tv == "dummy_buffer_sonos_chip":
            supported = True
        for st in self.supported_types:
            if cname == st:
                supported = True
        if "compute" in cname or "sonos_cell_dummy" in cname or "fat" in cname:
            supported = True
        if supported:
            return [True, PLUG_IN_ACCURACY]
        else:
            return [False, 0]

    def primitive_action_supported(self, interface: dict):
        """interface function for checking if a component action is supported by this plug-in"""

        # this function is called inside Accelergy as the initial check to see whether a component action is supported

        # ================
        # Input
        # ================
        # `interface` input is a dictionary that contains 4 keys:
        # (1) class_name: the value for this key is a string that describes the name of the primitive component class
        # (2) attributes: the value for this key is another dictionary that
        #                 describes the attributes name-value pairs of the primitive component under evaluation
        # (3) action_name: the value for this key is a string that describes the name of the primitive action under evaluation
        # (4) arguments: the value for this key is another dictionary that
        #                describes the arguments name-value pairs (if any) of the primitive action under evaluation

        # ================
        # Output
        # ================
        # If the plug-in suppor the specific request sent from Accelergy
        #    this function should be the accuracy of the estimation plug-in,
        # if not supported, please return 0

        # example extractions of the information provided in the interface
        class_name = interface["class_name"]
        attributes = interface["attributes"]
        action_name = interface["action_name"]
        arguments = interface["arguments"]

        # self.local_log['entries'].append(interface)

        # mprint(f' WITH PARAMS: attributes = {attributes}, arguments = {arguments}')

        return self.is_supported(class_name)[1]  # if not supported, please return 0

    def get_rowv(
        self,
        attributes,
        arguments,
        action_name,
        component="compute",
        class_name="",
        fat=False,
    ):
        if (
            component == "compute"
            or class_name == "sonos_compute"
            or class_name == "sonos_fat"
        ):
            active_rows = arguments["active_rows"]
            active_cols = arguments["active_cols"]
            # mprint('-'*30)
            # mprint(f'active_rows = {active_rows}   active_cols = {active_cols}')
            # mprint(f'AR: {active_rows}, AC: {active_cols}')
            # mprint(f'attributes = {attributes}')
            cellwidth = attributes["cellwidth"]
            if isinstance(cellwidth, str):
                cellwidth = 1

            er = self.compute_lut[self.compute_lut["active_rows"].eq(active_rows)]
            erc = er[er["active_cols"].eq(active_cols)]

        elif class_name == "sonos_cell_dummy" or (
            arguments is not None and arguments.get("sonos_dummy") is not None
        ):
            data_delta = arguments["data_delta"]
            address_delta = arguments["address_delta"]
            # mprint(f'DUMMY READ/WRITE SIZE: data_delta = {data_delta}, address_delta = {address_delta}')
            er = self.compute_lut[self.compute_lut["active_rows"].eq(data_delta)]
            erc = er[er["active_cols"].eq(address_delta)]

            if action_name == "write":
                return 0
            elif action_name == "read":
                action_name = "compute"

        else:
            mprint(
                f"attributes = {attributes} \n arguments = {arguments} \n action_name = {action_name} \n class_name = {class_name}"
            )
            cellwidth = attributes["cellwidth"]
            if isinstance(cellwidth, str):
                cellwidth = 1
            mprint(f"Cellwidth on storage: {cellwidth}")

            temp_erc = self.storage_lut[self.storage_lut["cellwidth"].eq(cellwidth)]
            erc = temp_erc.copy()
            erc["energy"] = temp_erc["power(W)"]
        #            erc['energy'] = erc['power(W)']
        #            erc.loc[:,'energy'] = erc.loc[:,'power(W)']

        # mprint(erc)
        # erc = erc[erc['cellwidth'].eq(cellwidth)]
        erc = erc[erc["action"].eq(action_name)]
        # mprint(erc['energy'].values)
        try:
            eng = erc["energy"].values[0]
        except:
            eng = 0.01

        eng = float(eng)

        if class_name == "sonos_fat" or fat:
            # print('FAT MODE')
            array_energy = eng
            prehiph_energy = 0.0

            eng = array_energy + prehiph_energy

        return eng
        # ep = self.compute_lut['active_rows'].eq(active_rows)['active_cols'].eq(active_cols)
        # if action_name == 'idle':

    rt_cache.memoize()

    def estimate_energy(self, interface):
        """Interface function for performing the actual energy estimations of the request sent from Accelergy"""

        # this function will only be called if this plug-in is selected to be the most accurate plug-in by Accelergy,
        # it should perform the energy estimation for the request

        # ================
        # Input
        # ================
        # `interface` input contains the same information as described in the `primitive_action_supported` function,
        #     please refer back to the comments above

        # ================
        # Output
        # ================
        # please return the estimated energy
        # note that this value will be rounded inside Accelergy,
        #       default rounding is 3 decimal points, but precision can be set via the -d flag when running Accelergy

        arguments = interface["arguments"]
        class_name = interface["class_name"]
        attributes = interface["attributes"]
        action_name = interface["action_name"]
        # if "compute" in action_name:
        #    return 0.00000000888

        fat = False
        if attributes is not None:
            fat = "fat" in attributes
        if arguments is not None:
            fat = "fat" in arguments or fat
            fat = "fat_grid" in arguments or fat

        # for k,v in interface.items():
        #     if isinstance(k,str):
        #         pass
        #     else:
        #         for kk,vv in interface[k].items():
        #             if 'fat' in vv:
        #                 mprint(f'GOT FAT: k = {k} v = {v} kk = {kk} vv = {vv}', True)
        #                 fat = True

        atr = {k: v for k, v in list(attributes.items())}
        try:
            arg = {k: v for k, v in list(arguments.items())}
        except:
            arg = {}
        # self.local_log['entries'].append({'cn': class_name, 'action': action_name, 'args': arg, 'atts': atr})
        mprint(f"arguments = {arguments} \n attributes = {attributes}")
        mprint(
            f" gathering arguments. attributes = {attributes} || action_name = {action_name} || arguments = {arguments} "
        )
        # mprint(arguments)
        # mprint(self.compute_lut.columns)
        # mprint(f'Class name: {class_name}\n ----- FAC: {action_name=}', True)

        if (
            "SRAM" in class_name
        ):  # TODO: Put this in a lookup table since we are getting dense
            return self.get_sram_energy(class_name, arguments, attributes, action_name)
        elif "A2D" in class_name.upper():
            return self.get_adc_energy(class_name, arguments, attributes, action_name)
        elif (
            class_name == "sonos_cell_storage"
            or class_name == "sonos_storage"
            or class_name == "storage_cell"
        ):
            if action_name == "write":
                energy = 1000
            else:
                energy = 0

                # energy = self.get_rowv(attributes, arguments, action_name, 'storage')
        else:
            mprint(f"Got class_name = {class_name}")
            if action_name == "mac_gated":
                print("MAC GATED TEST")
            else:
                try:
                    energy = self.get_rowv(
                        attributes,
                        arguments,
                        action_name,
                        "",
                        class_name=class_name,
                        fat=fat,
                    )
                    # energy = energy * 100000
                except:
                    return (
                        0.000000000  # TODO: Fix this once we start re-adding components
                    )

        mprint(f"Action: {action_name} was {energy}")
        mprint(
            f"class_name = {class_name}\taction_name = {action_name}\tattributes = {attributes}\targuments = {arguments}\tenergy = {energy}"
        )
        interface["energy"] = energy
        # self.local_log['values'].append(interface)

        if isinstance(energy, float):
            return energy
        else:
            mprint(f"error in energy: value {energy}")
            return energy

    def primitive_area_supported(self, interface):
        """interface function for checking if a component's area is supported by this plug-in"""

        # input and output of this function format is the same as the `primitive_action_supported` function
        # note that this is a check for area estimation instead of energy estimation;
        #      if this plug-in does not support area estimation sof components, zero should be returned
        class_name = interface["class_name"]
        if self.is_supported(class_name):
            return PLUG_IN_ACCURACY  # if not supported, please return 0
        else:
            return 0.1

    def estimate_area(self, interface):
        """Interface function for performing the actual area estimations of the request sent from Accelergy"""
        # input and output of this function is the same format as the `estimate_energy` function

        return 1

    #
    def __del__(self):
        try:
            self.time.stop()
        except TimerError as e:
            print(e)

        import yaml

        # df = yaml.dump(self.local_log)
        # with open('accelergy_plugin.yaml', 'w') as f:
        #     f.write(df)

    def get_sram_energy(self, class_name, arguments, attributes, action_name):
        actions = self.SRAM_table[self.SRAM_table["action"].eq(action_name)]

        try:
            depth = arguments["depth"]
            energy = find_neighbours(depth, actions, "depth")[0]
        except:
            energy = 0
        if energy == 0:
            mprint(
                f"\n----\nclass_name = {class_name}\taction_name = {action_name}\tattributes = {attributes}\targuments = {arguments}\tenergy={energy}",
                False,
            )
        # mprint(f'{class_name=} --- {action_name=}',True)
        return float(energy)

    def get_adc_energy_stats(self, class_name, arguments, attributes, action_name):
        return 0

    def get_adc_energy(self, class_name, arguments, attributes, action_name):
        return 0


import click


@click.command()
@click.option("--active_rows")
@click.option("--active_cols")
@click.option("--use_negatives", is_flag=True, default=False)
@click.option("--alg_comp")
def check_lut(active_rows, active_cols, use_negatives, alg_comp):
    data = SonosEstimator()
    clas = "sonos_array"
    interface = {}
    interface["arguments"] = {"active_rows": active_rows, "active_cols": active_cols}
    interface["class_name"] = clas
    interface["attributes"] = {"active_rows": active_rows, "active_cols": active_cols}
    interface["action_name"] = "compute"

    energy_estimate = data.estimate_energy(interface)
    print(
        f"Input: {active_rows=}, {active_cols=},{alg_comp=} \n Energy: {energy_estimate}"
    )


if __name__ == "__main__":
    data = SonosEstimator()
    check_lut()

    # dfdat = data.compute_lut
    # vx = dfdat.to_csv("energy_lut.csv")
    # if vx is None:
    #     print("none")
    # else:
    #     print(vx)
