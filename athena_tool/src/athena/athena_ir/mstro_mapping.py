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

import re
from pathlib import Path
import io
from typing import Union

DSCONV_R = re.compile("DSCONV")
DIMS_R = re.compile("Dimensions")


def create_mapping_model(
    source_model: str, dataflow: str = "rs", base_data_path: str = "./data/"
):
    base_data = Path(base_data_path)
    fd = base_data / f"{dataflow}.m"
    fd = fd.open("r")
    fdpt = base_data / "dpt.m"
    fdpt = fdpt.open("r")
    fo = io.StringIO()
    fm = io.StringIO(source_model)
    dsconv = 0
    for line in fm:
        if DSCONV_R.search(line):
            dsconv = 1
        if DIMS_R.search(line):
            fo.write(line)
            if dsconv:
                fdpt.seek(0)
                fo.write(fdpt.read())
            else:
                fd.seek(0)
                fd.write(fd.read())
            dsconv = 0
        else:
            fo.write(line)
    return f"{fo}"


def create_mapping_from_model_file(
    source_model: Path, dataflow: str, base_data_path: str = "./data/"
):
    model = source_model.open("r").read()
    return create_mapping_model(model, dataflow, base_data_path)
