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

""" Helper functions used to clean up, refactor, or reformat
    certain files used in the ATHENA tool.
"""

import yaml
import click
from pathlib import Path


def sanitize_yaml(loaded_yaml, yaml_filename=None, sanitized_key=""):
    """Sanitizes a preloaded yaml file by removing duplicate values
    found in each key of the file.
    """
    if yaml_filename is not None:
        print("Sanitizing `{}`...".format(yaml_filename))

    no_sanitize_flag = True
    for key, values in loaded_yaml.items():
        if isinstance(values, dict):
            nested_key_suffix = key + ":"
            _, no_sanitize_flag = sanitize_yaml(values, sanitized_key=nested_key_suffix)
        elif isinstance(values, list):
            if len(values) == len(set(values)):
                pass
            else:
                no_sanitize_flag = False
                seen = set()
                unique_vals = []
                for val in values:
                    if val not in seen:
                        unique_vals.append(val)
                        seen.add(val)
                loaded_yaml[key] = unique_vals
                key_str = "  removed duplicated from " + sanitized_key + key
                print(key_str)
        else:
            pass

    return loaded_yaml, no_sanitize_flag


@click.command(name="sanitize", options_metavar="")
@click.argument("filepaths", nargs=-1, metavar="[FILEPATH ..]")
def sanitize_file(filepaths):
    """Sanitizes files given their filepaths."""
    if not filepaths:
        click.echo("No filepaths provided.")
        return

    for filepath in filepaths:
        filepath = Path(filepath)
        if not filepath.exists():
            path_msg = "`{}` does not exist. Did you enter the full filepath?".format(
                filepath
            )
            click.echo(path_msg)
            continue

        if filepath.suffix == ".yaml":
            with open(filepath) as dirty_file:
                contents = yaml.safe_load(dirty_file)

            filename = filepath.name
            contents, no_sanitize_flag = sanitize_yaml(contents, yaml_filename=filename)
            if no_sanitize_flag:
                print("  No duplicate values found.")
            else:
                # overwrite existing file with clean version
                with open(filepath, "w") as clean_file:
                    yaml.dump(contents, clean_file)
        else:
            print("Currently supports only `.yaml` files")
