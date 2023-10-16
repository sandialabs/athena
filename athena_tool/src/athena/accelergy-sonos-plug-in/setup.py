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

from setuptools import setup
import os


def generate_data_files():
    """generate all the data files that need to be included in the share folder"""
    # include all table identifiers
    all_files = {}
    sets_of_tables_path = os.getcwd() + os.sep + "analog_core"
    for root, directories, file_names in os.walk(sets_of_tables_path):
        for file_name in file_names:
            relative_root = os.path.relpath(root, os.getcwd())
            if relative_root not in all_files:
                all_files[relative_root] = [relative_root + os.sep + file_name]
            else:
                all_files[relative_root].append(relative_root + os.sep + file_name)

    data_files = []
    share_root = "share/accelergy/estimation_plug_ins/sonos_plugin/"
    for relative_root, list_of_files in all_files.items():
        root = share_root + relative_root
        subfolder_tuple = (root, list_of_files)
        data_files.append(subfolder_tuple)
    # include top-level py and yaml files
    data_files.append(
        (
            share_root,
            [
                "sonos_estimator.py",
                "sonos.estimator.yaml",
                "sonos_cell_storage.csv",
                "sonos_compute.csv",
            ],
        )
    )
    print(data_files)
    return data_files


setup(
    name="sonos-accelergy-plug-in",
    version="0.1",
    description="An energy estimation plug-in for Accelergy framework using CACTI",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    ],
    keywords="accelerator hardware energy estimation",
    author="Mark Plagge",
    author_email="mplagge@sandia.gov",
    license="MIT",
    install_requires=["pyYAML"],
    python_requires=">=3.6",
    data_files=generate_data_files(),
    # data_files=[
    #             ('share/accelergy/estimation_plug_ins/accelergy-plug-in',
    #               ['plugin.estimator.yaml',
    #                'sonos_estimation.py',
    #                'analog_core/'])
    #             ],
    include_package_data=True,
    entry_points={},
    zip_safe=False,
)
