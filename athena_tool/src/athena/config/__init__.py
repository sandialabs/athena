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

from .athena_config import TLConfig, get_arch_config
from .config_helpers import check_arch_config, add_arch_components
from .click_helpers import OptionGetAll

#### Set the package environment variables used by the tool ###
# from pathlib import Path
#
## envvar names
# envvar_names = ['PATH_TO_ATHENA_HOME', 'PATH_TO_ACCELERGY_CONFIG', 'ATHENA_TOOL_INIT']
#
## envvar values
# home_path = Path(''.join(Path.cwd().parts[0:2]))
# if home_path.name == 'home':
#    home_path = home_path / 'ath_usr'
# accelergy_config_path = Path('/root/.config/accelergy/accelergy_config.yaml')
# init_flag = 0
# envvar_values = [home_path, accelergy_config_path, init_flag]
#
## check for existing .env file and create one if needed
# dotenv_path = Path.cwd() / '.env' # home_path / 'src/athena/.env'
# dotenv_text = ''
# for name, val in zip(envvar_names, envvar_values):
#    dotenv_text += "{}='{}'\n".format(name, str(val))
# dotenv_path.write_text(dotenv_text)
