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

""" Helper functions to make configuration work
"""

## Dependencies
import yaml
from pathlib import Path


## Functions
def check_arch_config(ARCH):
    """Used to check the TLConfig object that stores
    relevant information for the chosen architecture.
    """
    # first, check if the architecture folder exists
    if not ARCH.folder_path.exists():
        print("Architecture folder {} does not exist".format(ARCH.folder_path))
        return False

    # if it does exists, then check all the paths in the TLConfig object
    config_paths = []
    exclude_keys = ["problem_input_type", "athena_backend"]
    for key, value in ARCH.asdict().items():
        if key not in exclude_keys:
            if isinstance(value, list):
                for val in value:
                    config_paths.append(val)
            else:
                config_paths.append(value)

    for path in config_paths:
        if not path.exists():
            print("Directory or File `{}` was not found.".format(path))
            print(
                "Check location of missing item and `{}/*_config.yaml`".format(
                    ARCH.folder_path
                )
            )
            return False

    # return true if everything is in place
    return True


def add_arch_components(ARCH, accelergy_config_path):
    """Adds any additiona primitive components in architecture
    folder that are not already in the accelergy configuration
    file.
    """
    print("Checking primitive components in `accelergy_config.yaml`...")
    # open the accelergy_config file
    with open(accelergy_config_path) as current_config_file:
        config = yaml.safe_load(current_config_file)

    # check for any `.lib.yaml` files in the architecture folder
    component_libs = [str(c_lib) for c_lib in ARCH.folder_path.glob("**/*.lib.yaml")]

    # if there are primitive component libs found, check the config file and add if needed
    update_flag = False
    if component_libs:
        for c_lib in component_libs:
            if c_lib not in config["primitive_components"]:
                config["primitive_components"].append(c_lib)
                print("  + {} to primitive_components".format(c_lib))
                update_flag = True

    # update the config file
    if update_flag:
        with open(accelergy_config_path, "w") as updated_config_file:
            yaml.dump(config, updated_config_file)
        print("Updated `accelergy_config.yaml`")
