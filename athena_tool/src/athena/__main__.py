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

import os, sys, subprocess, shutil
import yaml
import click
from pathlib import Path
from dotenv import find_dotenv, load_dotenv, set_key
from .config import *  # see config/__init__.py for more info
from .utils import *  # see utils/__init__.py for more info


### Project environment variables
envvars_path = find_dotenv()
load_dotenv(envvars_path)

### Set up project environment variables
home_path = Path(os.environ["PATH_TO_ATHENA_HOME"])
accelergy_config_path = Path(os.environ["PATH_TO_ACCELERGY_CONFIG"])
init_flag = int(os.environ["ATHENA_TOOL_INIT"])

### Make sure init env variable reflects status of tool
if not accelergy_config_path.exists() and init_flag:
    init_flag = 0
    set_key(envvars_path, "ATHENA_TOOL_INIT", "0")

### Set up configuration of chosen architecture
path_to_arch_folder = (
    home_path / "accelergy_architectures" / "sonos_pim"
)  # make required arg?
problem_files = [(path_to_arch_folder / "example_layer.yaml")]  # make required arg?


### Main CLI function
@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    "-a",
    "--arch",
    default=path_to_arch_folder,
    metavar="DIRPATH",
    type=click.Path(exists=True),
    help="Folder path to chosen architecture",
)
@click.option(
    "-i",
    "--inputs",
    cls=OptionGetAll,
    default=problem_files,
    metavar="[FILEPATH ..]",
    type=list,
    help="Paths of input files to analyze",
)
@click.option(
    "-o",
    "--outputs",
    metavar="DIRPATH",
    type=click.Path(exists=True),
    help="Redirects the outputs to this folder if specified; the folder must exist before using ATHENA",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="If verbose flag is set, then a longer summary message is printed and saved to the summary .csv file.",
)
def cli(ctx, arch, inputs, outputs, verbose):
    """
    \b
        ___  ________  _________   ____\|/ ,___, |/|/
       /   |/_  __/ / / / ____/ | / /   |/ (0,0)/ |/_
      / /| | / / / /_/ / __/ /  |/ / /| |/ /)_) |/_
     / ___ |/ / / __  / /___/ /|  / ___ |\_ "" |/_
    /_/  |_/_/ /_/ /_/_____/_/ |_/_/  |_| \|_|/

    Main CLI for using Athena

    To modify architecture configuration, edit the `<arch>_config.yaml` file in
    the architecture folder. This file will define which base architecture is
    chosen, what component files are used, which mapper and constraints are applied,
    and where the outputs should be stored.

    \b
    For more information on available commands,
    run `athena <command> --help`.
    """

    # if trying to run athena and not initialized, tell user to init
    if ctx.invoked_subcommand != "init" and not init_flag:
        sys.exit("ATHENA not initialized; run `athena init` to set up tool.")

    # if not running a tool subcommand, run the base athena tool
    if ctx.invoked_subcommand is None and init_flag:
        # set up architecture configuration based on arg input
        ARCH_CONFIG = get_arch_config(arch, inputs, outputs)
        click.echo("Running ATHENA with {}".format(ARCH_CONFIG.folder_path))
        click.echo(
            "  > using `{}` as base architecture".format(ARCH_CONFIG.architecture.name)
        )

        # double check configuration and add primitive components if necessary
        if not check_arch_config(ARCH_CONFIG):
            sys.exit("Check architecture configuration.")
        add_arch_components(ARCH_CONFIG, accelergy_config_path)

        # run timeloop on the architecture configuration
        run_mapper(ARCH_CONFIG, verbose)
        gather_outputs(ARCH_CONFIG.output_folder, verbose)


#        print('')
#        print('ARCH CONFIG:')
#        for key, value in ARCH_CONFIG.asdict().items():
#            print(key,':')
#            print(value)
#        print('')
#        click.echo(ctx.__dict__)
#        click.echo('')

# add subcommands to CLI
cli.add_command(initialize_athena)
cli.add_command(sanitize_file)


if __name__ == "__main__":
    # execute the command line interface
    cli(prog_name="athena")
