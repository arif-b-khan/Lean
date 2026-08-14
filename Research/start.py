# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean Algorithmic Trading Engine v2.0. Copyright 2014 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This Python script can be loaded in a notebook (ipynb file)
# in order to reference QuantConnect assemblies
#
# Usage:
# %run "start.py"

import clr_loader
import os
import sys
from pythonnet import get_runtime_info, set_runtime


def _find_dotnet_root():
    candidates = [
        os.environ.get("DOTNET_ROOT"),
        "/opt/homebrew/opt/dotnet/libexec",
        "/usr/local/share/dotnet",
        os.path.expanduser("~/.dotnet"),
    ]
    for candidate in candidates:
        if candidate and os.path.isfile(os.path.join(candidate, "dotnet")):
            return candidate
    return None


# The runtimeconfig.json is stored alongside start.py, but start.py may be a
# symlink and the directory start.py is stored in is not necessarily the
# current working directory. We therefore construct the absolute path to the
# start.py file, and find the runtimeconfig.json relative to that.
runtime_config = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "QuantConnect.Lean.Launcher.runtimeconfig.json",
)
dotnet_root = _find_dotnet_root()
launcher_dir = os.path.dirname(os.path.realpath(__file__))

if launcher_dir not in sys.path:
    sys.path.insert(0, launcher_dir)

# Keep startup behavior deterministic regardless of notebook launch directory.
os.chdir(launcher_dir)

# Startup scripts can be executed multiple times in notebook sessions.
if get_runtime_info() is None:
    coreclr_kwargs = {"runtime_config": runtime_config}
    if dotnet_root:
        coreclr_kwargs["dotnet_root"] = dotnet_root
    set_runtime(clr_loader.get_coreclr(**coreclr_kwargs))

from AlgorithmImports import *

# Used by pythonNet
AddReference("Fasterflect")

Config.Reset()
Config.Set("composer-dll-directory", launcher_dir)
Initializer.Start()
api = Initializer.GetSystemHandlers().Api
algorithmHandlers = Initializer.GetAlgorithmHandlers(researchMode=True)

# Required to configure pythonpath with additional paths the user may have
# set in the config, like a project library.
PythonInitializer.Initialize(False)

try:
    get_ipython().run_line_magic("matplotlib", "inline")
except NameError:
    # can happen if start is triggered from python and not Ipython
    pass
