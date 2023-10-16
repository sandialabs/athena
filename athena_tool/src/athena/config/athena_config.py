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

""" Configuration file containing templates for users to define
    different data classes used in the ATHENA tool.
"""

## Dependencies
import yaml
from pathlib import Path
from typing import List
from datadict import dataclass
from enum import Enum


class ProblemConversionMode(Enum):
    NO_CONVERT = 1
    PYTORCH = 2
    MLIR = 3


## Parent Classes
@dataclass
class TLConfig:
    folder_path: Path
    architecture: Path
    component_files: List[Path]
    mapper_files: List[Path]
    constraint_files: List[Path]
    problem_files: List[Path]
    output_folder: Path
    # path_to_athena_accelergy_plugin: Path
    problem_input_type: ProblemConversionMode = ProblemConversionMode.NO_CONVERT
    athena_backend: str = "timeloop"


## Helper Functions
def get_arch_config(path_to_arch_folder, problem_files, output_folder):
    """Creates TLConfig object for use inside the
    the main ATHENA CLI script.
    """
    # make sure architecture directory input is correct type
    if not isinstance(path_to_arch_folder, Path):
        path_to_arch_folder = Path(path_to_arch_folder)

    path_to_arch_config = [f for f in path_to_arch_folder.rglob("*_config.yaml")]
    with open(path_to_arch_config[0]) as config_file:
        config = yaml.safe_load(config_file)

    path_to_base_arch = path_to_arch_folder / config["arch_paths"]["main_yaml"]
    path_to_components = path_to_arch_folder / config["arch_paths"]["components"]
    path_to_mappings = path_to_arch_folder / config["mapping_paths"]["mapper"]
    path_to_constraints = path_to_arch_folder / config["mapping_paths"]["constraints"]

    if output_folder is None:
        # use default output folder specified in <arch>_config.yaml
        path_to_outputs = path_to_arch_folder / config["output_path"]
    else:
        # override with option provided in CLI
        path_to_outputs = Path(output_folder)

    path_to_problems = [Path(path) for path in problem_files]

    ARCH = TLConfig(
        folder_path=path_to_arch_folder,
        architecture=path_to_base_arch,
        component_files=[f for f in path_to_components.rglob("*.yaml")],
        mapper_files=[f for f in path_to_mappings.rglob("*.yaml")],
        constraint_files=[f for f in path_to_constraints.rglob("*.yaml")],
        problem_files=path_to_problems,
        output_folder=path_to_outputs,
    )

    return ARCH
