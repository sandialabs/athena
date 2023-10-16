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

""" Contains functions used to initialize the ATHENA tool.
"""

import os, subprocess
import yaml
import click
from pathlib import Path
from dotenv import find_dotenv, load_dotenv, set_key

## Project environment variables
envvars_path = find_dotenv()
load_dotenv(envvars_path)

home_path = Path(os.environ["PATH_TO_ATHENA_HOME"])
accelergy_config_path = Path(os.environ["PATH_TO_ACCELERGY_CONFIG"])
init_flag = int(os.environ["ATHENA_TOOL_INIT"])


def check_accelergy_config():
    """Checks for existence of accelergy configuration file."""
    if accelergy_config_path.exists():
        print("Accelergy Configuration file already exists.")
    else:
        # run accelergy once to generate the file
        subprocess.run("accelergy", stdout=subprocess.DEVNULL)
        print("File `accelergy_config.yaml` generated.")


def check_accelergy_tables():
    """Checks the accelergy config file for table plug-ins."""
    with open(accelergy_config_path) as config_file:
        config = yaml.safe_load(config_file)
    if "table_plug_ins" not in config.keys():
        # run accelergyTables to modify the configuration file
        subprocess.run("accelergyTables", stdout=subprocess.DEVNULL)
        print("Added 'table_plug_ins' key to `accelergy_config.yaml`")


def add_plug_ins():
    """Finds and adds any addition plug-ins to accelergy config file."""
    print("Adding additional plug-ins to `accelergy_config.yaml`...")
    with open(accelergy_config_path) as current_config_file:
        config = yaml.safe_load(current_config_file)
    # get current estimator/table paths to check for update
    current_plug_in_paths = config["estimator_plug_ins"].copy()
    update_estimators_flag = False
    current_table_roots = config["table_plug_ins"]["roots"].copy()
    update_tables_flag = False

    # find the current plug-ins
    current_plug_ins = []
    for plug_in in os.scandir(current_plug_in_paths[0]):
        if plug_in.is_dir():
            current_plug_ins.append(plug_in.name)

    # find additional plug-ins and add to config file
    new_plug_ins = []
    new_tables = []
    for root, subdirs, _ in os.walk(home_path):
        for subdir in subdirs:
            full_path = os.path.join(root, subdir)

            # check for estimator plug-ins
            if (
                "plug-in" in subdir
                and subdir not in current_plug_ins
                and full_path not in current_plug_in_paths
            ):
                config["estimator_plug_ins"].append(full_path)
                filename = os.path.basename(full_path)
                print("  + {} to estimator_plug_ins".format(filename))

            # check for table plug-ins
            if "estimation_tables" in subdir and full_path not in current_table_roots:
                config["table_plug_ins"]["roots"].append(full_path)
                filename = os.path.basename(full_path)
                print("  + {} to table_plug_ins".format(filename))

    # check if config_file needs to be overwritten
    updated_plug_in_paths = config["estimator_plug_ins"].copy()
    if current_plug_in_paths == updated_plug_in_paths:
        print("  all estimator plug-ins already in `accelergy_config.yaml`")
    else:
        update_estimators_flag = True

    updated_table_roots = config["table_plug_ins"]["roots"].copy()
    if current_table_roots == updated_table_roots:
        print("  all table plug-ins already in `accelergy_config.yaml`")
    else:
        update_tables_flag = True

    if update_estimators_flag or update_tables_flag:
        with open(accelergy_config_path, "w") as updated_config_file:
            yaml.dump(config, updated_config_file)
        print("Updated `accelergy_config.yaml`")


@click.command(name="init", options_metavar="")
def initialize_athena():
    """Initializes ATHENA."""
    if init_flag and accelergy_config_path.exists():
        click.echo("ATHENA already initialized.")
    else:
        click.echo("Initializing ATHENA...")
        check_accelergy_config()
        check_accelergy_tables()
        add_plug_ins()
        set_key(envvars_path, "ATHENA_TOOL_INIT", "1")
