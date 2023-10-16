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

import shutil
import os
from pathlib import Path
import click
from dataclasses import dataclass
import subprocess
import yaml


@dataclass
class BaseSysConfig:
    base_path: Path
    home_path: Path


class SysConfig(BaseSysConfig):
    def __init__(self, *args, **kwargs):
        super(*args, **kwargs)

        self.plugin_path = self.home_path / "accelergy_plugins"
        self.extern_repo_path = self.home_path / "external_repos"
        self.cacti_plugin_path = self.extern_repo_path / "accelergy-cacti-plug-in"
        self.table_plugin_path = (
            self.extern_repo_path / "accelergy-table-based-plug-ins"
        )
        self.sonos_plugin_path = self.home_path / "src"
        self.sonos_plugin_path = self.sonos_plugin_path / "accelergy-sonos-plugin"
        self.plugin_paths = [
            self.cacti_plugin_path,
            self.table_plugin_path,
            self.sonos_plugin_path,
        ]
        self.base_yml = yaml.load(open(self.base_path / "accelergy_config.yaml", "r"))

    def init_accelergy_plugins(self):
        for plugin in self.plugin_paths:
            subprocess.run("python setup.py build", cwd=plugin)
            subprocess.run("python setup.py install", cwd=plugin)
            self.base_yml["estimator_plug_ins"].append(str(plugin.absolute()))

    def init_accelergy_config(self):
        config_path = self.home_path / ".config/accelergy/accelergy_config.yaml"
        click.echo(f"{config_path}")
        click.echo(f"{self.base_yml}")
        click.echo(f'{open(config_path,"r").read()}')
        open(config_path, "w").write(yaml.dump(self.base_yml))
        click.echo(f'{open(config_path,"r").read()}')


@click.command()
@click.option("-b", "--base-path", default="./docker_build")
@click.argument("home_path")
def cli(base_path, home_path):
    print(f"Pre-Init Athena / Accelergy")
    base_path = Path(base_path)
    home_path = Path(home_path)
    config = SysConfig(base_path, home_path)
    click.echo(f"{base_path=} | {home_path=}")
    click.echo("init plugins...")
    config.init_accelergy_plugins()
    click.echo("init config...")
    config.init_accelergy_config()
    click.echo("done")
