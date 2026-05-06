# Realpath polyfill, notably absent macOS and some debian distros
absolute_path() {
  echo "$(cd "$(dirname "${1}")" && pwd)/$(basename "${1}")"
}

# Get build directory from args position 1, or use default
DEFAULT_BUILD_DIR=../Launcher/bin/Debug/
BUILD_DIR=${1:-$DEFAULT_BUILD_DIR}
BUILD_DIR=$(absolute_path "${BUILD_DIR}")

WORKSPACE_DIR=$(absolute_path "$(dirname "${0}")/..")
PYTHONNET_DYLIB="${WORKSPACE_DIR}/.conda/lean-py311/lib/libpython3.11.dylib"
JUPYTER_BIN="${WORKSPACE_DIR}/.conda/lean-py311/bin/jupyter-lab"
DOTNET_ROOT_HOMEBREW="/opt/homebrew/opt/dotnet/libexec"

#Add our build directory to python path for python kernel
export PYTHONPATH="${PYTHONPATH}:${BUILD_DIR}"

# Prefer the repo-local Lean Python environment when available.
if [ -f "${PYTHONNET_DYLIB}" ]; then
  export PYTHONNET_PYDLL="${PYTHONNET_DYLIB}"
fi

if [ -x "${DOTNET_ROOT_HOMEBREW}/dotnet" ]; then
  export DOTNET_ROOT="${DOTNET_ROOT_HOMEBREW}"
fi

# Mirror Windows mklink behavior on macOS by linking IPython startup script.
IPYTHON_STARTUP_DIR="$HOME/.ipython/profile_default/startup"
IPYTHON_STARTUP_FILE="${IPYTHON_STARTUP_DIR}/start.py"
STARTUP_SOURCE="${BUILD_DIR}/start.py"
if [ -f "${STARTUP_SOURCE}" ]; then
  mkdir -p "${IPYTHON_STARTUP_DIR}"
  ln -sfn "${STARTUP_SOURCE}" "${IPYTHON_STARTUP_FILE}"
fi

# Launch jupyter-lab
if [ -x "${JUPYTER_BIN}" ]; then
  exec "${JUPYTER_BIN}" --allow-root --no-browser --notebook-dir="$BUILD_DIR" --LabApp.token=''
fi

exec jupyter-lab --allow-root --no-browser --notebook-dir="$BUILD_DIR" --LabApp.token=''