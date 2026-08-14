# Local Python Setup

This repo's Docker images use Python 3.11 with pinned packages from these files:

- `DockerfileLeanFoundation`
- `Dockerfile`
- `DockerfileJupyter`
- `DockerfileLeanFoundationARM`

For local macOS development, the practical target is the shared Lean runtime subset from those images:

- Python 3.11.11
- `pandas`, `numpy`, `scipy`, `wrapt`
- `jupyterlab`, `ipywidgets`, `jupyterlab-widgets`
- `clr-loader` and `pythonnet` for PythonNet research support
- `debugpy` for current debugger compatibility

Avoid installing `quantconnect` and `quantconnect-stubs` in the same runtime kernel used for `%run start.py`, because they can shadow Lean's .NET `QuantConnect` namespaces during PythonNet imports.

The full foundation package set in the Linux Docker images includes many Linux-only, GPU-only, or container-oriented dependencies. Those are better consumed through Docker or Lean CLI research containers instead of a local macOS environment.

The Docker runtime image also installs `ptvsd` and `pydevd-pycharm` for legacy remote-debug workflows inside containers. They are intentionally excluded from the validated macOS manifest here because the Lean local workflow already supports `debugpy`, which is the current path in the repo.

## Create The Environment

From the repo root:

```bash
conda env create -f environment.python311.yml
conda create --prefix ./.conda/lean-py311 --clone lean-py311
conda activate ./.conda/lean-py311
```

If the environment already exists:

```bash
conda env update -f environment.python311.yml --prune
conda create --prefix ./.conda/lean-py311 --clone lean-py311 --yes
conda activate ./.conda/lean-py311
```

The workspace is configured to prefer `./.conda/lean-py311/bin/python` in VS Code.

## One-Click Setup (macOS/Linux + Windows)

Use the cross-platform setup script from the repo root:

```bash
python3 scripts/setup_research_env.py
```

This script:

- Creates or updates conda env `lean-py311` from `environment.python311.yml`
- Recreates the repo-local clone at `./.conda/lean-py311`
- Builds Lean in Debug mode if `Launcher/bin/Debug` artifacts are missing
- Ensures `Launcher/bin/Debug/start.py` and `Launcher/bin/Debug/AlgorithmImports.py` exist
- Creates/updates IPython startup link:
  - `~/.ipython/profile_default/startup/start.py` -> `<repo>/Launcher/bin/Debug/start.py`
  - On Windows, it attempts a symlink first and falls back to copying if symlink permissions are unavailable

Optional wrappers:

- macOS/Linux: `./scripts/setup_research_env.sh`
- Windows PowerShell: `./scripts/setup_research_env.ps1`
- Windows CMD: `scripts\\setup_research_env.cmd`

Useful flags:

```bash
python3 scripts/setup_research_env.py --skip-conda
python3 scripts/setup_research_env.py --skip-build
python3 scripts/setup_research_env.py --force-copy
```

## Configure PythonNet

Lean needs `PYTHONNET_PYDLL` to point at the Python 3.11 dynamic library inside the active conda environment:

```bash
export PYTHONNET_PYDLL="$CONDA_PREFIX/lib/libpython3.11.dylib"
```

To persist that for this repo in `zsh`, add it after activating the env in your shell startup, or export it before launching Lean from the terminal.

## Verify The Environment

```bash
python -c "import sys, pandas, wrapt, clr_loader, debugpy; print(sys.version)"
python -c "from pathlib import Path; import os; print(os.environ.get('PYTHONNET_PYDLL', 'unset'))"
```

## Run Lean With Python

Build Lean first, then run from the launcher output directory with the conda environment active:

```bash
cd Launcher/bin/Debug
dotnet QuantConnect.Lean.Launcher.dll
```

For local research notebooks, start Jupyter from the same directory and run `%run "start.py"` in the first Python notebook cell.

On macOS, this repo now mirrors the Windows `mklink` behavior by creating/updating:

- `~/.ipython/profile_default/startup/start.py` -> `<repo>/Launcher/bin/Debug/start.py`

The link is refreshed automatically by `.vscode/launch_research.sh` each time you start research.

## Notes

- If you want the exact full research image, prefer `lean research` or the Docker-based workflow.
- If a specific strategy needs extra libraries from `DockerfileLeanFoundation`, add them incrementally to `environment.python311.yml` instead of trying to reproduce the full Linux image on macOS.
