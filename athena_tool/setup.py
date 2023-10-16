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

"""
    Setup file for athena.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 4.0rc1.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
from setuptools import setup
from distutils.command.build_py import build_py
from pathlib import Path
import os


def generate_env():
    envvar_names = [
        "PATH_TO_ATHENA_HOME",
        "PATH_TO_ACCELERGY_CONFIG",
        "ATHENA_TOOL_INIT",
    ]
    envvar_values = [
        Path("/home/ath_usr"),
        Path("/root/.config/accelergy/accelergy_config.yaml"),
        0,
    ]
    dotenv_text = ""
    for name, val in zip(envvar_names, envvar_values):
        dotenv_text += "{}='{}'\n".format(name, str(val))
    return dotenv_text


class my_build_py(build_py):
    def run(self):
        if not self.dry_run:
            target_dir = os.path.join(self.build_lib, "athena")
            self.mkpath(target_dir)
            with open(os.path.join(target_dir, ".env"), "w") as fobj:
                fobj.write(generate_env())

        build_py.run(self)


if __name__ == "__main__":
    #    setup(use_pyscaffold=False,cmdclass={'build_py': my_build_py})
    #    exit()
    dkr = os.getenv("DOCKER")
    if dkr is not None or dkr == "1" or dkr == 1:
        setup(use_pyscaffold=False, cmdclass={"build_py": my_build_py})
    else:
        try:
            setup(
                use_scm_version={
                    "version_scheme": "no-guess-dev",
                    "fallback_version": "0.1",
                    "root": "../",
                },
                cmdclass={"build_py": my_build_py},
            )

        except:  # noqa
            print(
                "\n\nAn error occurred while building the project, "
                "please ensure you have the most updated version of setuptools, "
                "setuptools_scm and wheel with:\n"
                "   pip install -U setuptools setuptools_scm wheel\n\n"
            )
            setup(use_pyscaffold=False, cmdclass={"build_py": my_build_py})
