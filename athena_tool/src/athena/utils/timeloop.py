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

"""Functions used in the ATHENA tool to run the timeloop-mapper,
   gather timeloop-mapper outputs, and create a summary file of
   the output results. Uses additional functionality of parse_stats.
"""

## Dependencies
import os, subprocess, shutil, tempfile
import yaml
import time
import click
from pathlib import Path
from natsort import natsorted


## Functions
def run_mapper(ARCH, verbose=False):
    """Calls the timeloop-mapper to run on the filepaths
    stored in the TLConfig for a chosen architecture.
    """
    # warn user about possibly overwriting any current files in output folder
    output_folder_contents = [f for f in ARCH.output_folder.iterdir()]
    if output_folder_contents:
        print("")
        msg = "Output files already in {}, do you want to save them? (y/n)".format(
            ARCH.output_folder.name
        )
        choice = click.prompt(msg)
        assert choice in ["y", "n"], "Not an allowed choice"

        if choice == "y":
            save_folder = click.prompt("Enter folder name")
            save_folder_path = ARCH.folder_path / save_folder
            save_folder_path.mkdir()
            for item in output_folder_contents:
                moved = shutil.move(
                    item, save_folder_path, copy_function=shutil.copytree
                )
            print("Contents moved to {}".format(save_folder_path))
        elif choice == "n":
            print("Removing contents from output folder...")
            for item in output_folder_contents:
                if item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
                elif item.is_file():
                    os.remove(item)
                else:
                    pass
        else:
            pass

    # edit mappers to show live status based on verbose flag
    #    for mapper_path in ARCH.mapper_files:
    #        with open(mapper_path) as current_mapper:
    #            mapper = yaml.safe_load(current_mapper)
    #        if 'live-status' in mapper['mapper'].keys():
    #            if verbose:
    #                mapper['mapper']['live-status'] = True
    #            else:
    #                mapper['mapper']['live-status'] = False
    #            with open(mapper_path, 'w') as new_mapper:
    #                yaml.dump(mapper, new_mapper)
    #        else:
    #            print('{} does not have entry `live-status`'.format(mapper_path.name))
    print("")
    print("Calling timeloop-mapper...")
    # store the paths needed to run timeloop
    tl_mapper_cmd = ["timeloop-mapper"]
    for key, value in ARCH.asdict().items():
        if key not in [
            "folder_path",
            "problem_files",
            "output_folder",
            "problem_input_type",
            "athena_backend",
        ]:
            if isinstance(value, list):
                for val in value:
                    tl_mapper_cmd.append(str(val))
            else:
                tl_mapper_cmd.append(str(value))

    # call timeloop for each given input in ARCH problem files
    total_runtime = 0
    ordered_filenames = natsorted([str(prob) for prob in ARCH.problem_files])
    for input in ordered_filenames:
        print("  running timeloop on `{}`...".format(Path(input).stem))
        run_log = "timeloop-mapper.{}.log".format(Path(input).stem)
        run_start = time.time()
        with open(run_log, "w") as log:
            subprocess.run(tl_mapper_cmd + [input], stdout=log, stderr=log)
        run_elapsed = time.time() - run_start
        runtime_msg = "    > timeloop-mapper execution took {} seconds".format(
            round(run_elapsed, 3)
        )
        print(runtime_msg)
        total_runtime += run_elapsed

        # find all of the generated files in current dir
        tl_mapper_files = [
            Path(file)
            for file in os.listdir(os.getcwd())
            if os.path.isfile(file) and file.startswith("timeloop-mapper.")
        ]

        # find log files for this input
        log_filepaths = []
        for file in tl_mapper_files:
            if file.suffix == ".log":
                log_filepaths.append(file)

        # merge logs into a single log file for this input and move to output folder
        output_log_path = ARCH.output_folder / "{}.log".format(Path(input).stem)
        if output_log_path.exists():
            os.remove(output_log_path)
        with open(output_log_path, "w") as outlog:
            for logpath in log_filepaths:
                with open(logpath) as inlog:
                    outlog.write(inlog.read())
                outlog.write("\n")
            outlog.write(runtime_msg)
            outlog.write("\n")
        #        print('    > log stored at {}'.format(output_log_path))

        # move the stats to output folder
        stats_filepath = Path.cwd() / "timeloop-mapper.map+stats.xml"
        if stats_filepath.exists():
            output_stats_path = ARCH.output_folder / "{}.map+stats.xml".format(
                Path(input).stem
            )
            # check to see if output stats path exists to ensure overwrite
            if output_stats_path.exists():
                os.remove(output_stats_path)
            os.rename(stats_filepath, output_stats_path)
        #            print('    > timeloop stats stored in {}'.format(output_stats_path))
        else:
            print("    > no stats generated for {}".format(Path(input).stem))
            print("      check {} for more information".format(output_log_path))

        # remove files from current directory
        for file in tl_mapper_files:
            if file.exists():
                os.remove(file)

    print("")
    print("Total runtime took {} seconds".format(total_runtime))
