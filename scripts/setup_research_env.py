#!/usr/bin/env python3
"""One-click local Lean research setup for macOS/Linux/Windows.

This script automates the repetitive steps needed for local Research notebooks:
- create/update the conda base environment from environment.python311.yml
- clone it to the repo-local prefix (./.conda/lean-py311)
- ensure Launcher/bin/Debug has start.py and AlgorithmImports.py
- create/update the IPython startup link to Launcher/bin/Debug/start.py
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

START_FILE_NAME = "start.py"
ALGORITHM_IMPORTS_FILE_NAME = "AlgorithmImports.py"


def _run(cmd: list[str], cwd: Path | None = None) -> None:
    pretty = " ".join(cmd)
    print(f"[run] {pretty}")
    completed = subprocess.run(cmd, cwd=str(cwd) if cwd else None)
    if completed.returncode != 0:
        raise RuntimeError(f"Command failed ({completed.returncode}): {pretty}")


def _command_exists(command: str) -> bool:
    return shutil.which(command) is not None


def _conda_env_exists(env_name: str) -> bool:
    try:
        output = subprocess.check_output(["conda", "env", "list", "--json"], text=True)
    except Exception:
        return False

    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return False

    for env_path in data.get("envs", []):
        if Path(env_path).name == env_name:
            return True
    return False


def _ensure_conda_env(repo_root: Path, env_name: str, env_prefix: Path) -> None:
    env_file = repo_root / "environment.python311.yml"
    if not env_file.exists():
        raise FileNotFoundError(f"Missing environment file: {env_file}")

    if not _command_exists("conda"):
        raise RuntimeError("conda is required but was not found in PATH")

    if _conda_env_exists(env_name):
        _run(["conda", "env", "update", "-f", str(env_file), "--prune"])
    else:
        _run(["conda", "env", "create", "-f", str(env_file)])

    if env_prefix.exists():
        _run(["conda", "env", "remove", "--prefix", str(env_prefix), "--yes"])

    _run(["conda", "create", "--prefix", str(env_prefix), "--clone", env_name, "--yes"])


def _ensure_build_output(repo_root: Path, build_dir: Path, skip_build: bool) -> None:
    runtime_config = build_dir / "QuantConnect.Lean.Launcher.runtimeconfig.json"
    if runtime_config.exists():
        return

    if skip_build:
        print("[warn] Build output missing and --skip-build was set; continuing")
        return

    # Build once so startup artifacts are available under Launcher/bin/Debug.
    _run(
        [
            "dotnet",
            "build",
            str(repo_root / "QuantConnect.Lean.sln"),
            "/p:Configuration=Debug",
            "/p:DebugType=portable",
            "/p:WarningLevel=1",
        ],
        cwd=repo_root,
    )


def _copy_if_missing(source: Path, destination: Path) -> None:
    if source.exists() and not destination.exists():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        print(f"[info] Copied {source} -> {destination}")


def _ensure_startup_files(repo_root: Path, build_dir: Path) -> Path:
    build_dir.mkdir(parents=True, exist_ok=True)

    start_source = build_dir / START_FILE_NAME
    _copy_if_missing(repo_root / "Research" / START_FILE_NAME, start_source)

    algo_imports = build_dir / ALGORITHM_IMPORTS_FILE_NAME
    _copy_if_missing(repo_root / "Common" / ALGORITHM_IMPORTS_FILE_NAME, algo_imports)

    if not start_source.exists():
        raise FileNotFoundError(
            f"Could not find startup script at {start_source}. Build Lean first or provide start.py."
        )

    return start_source


def _ipython_startup_target() -> Path:
    home = Path.home()
    return home / ".ipython" / "profile_default" / "startup" / "start.py"


def _remove_existing_target(target: Path) -> None:
    if not target.exists() and not target.is_symlink():
        return
    if target.is_dir() and not target.is_symlink():
        raise RuntimeError(f"Startup target path is a directory: {target}")
    target.unlink()


def _link_or_copy_startup(source: Path, target: Path, force_copy: bool) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.is_symlink() and target.resolve() == source.resolve():
        print(f"[ok] Startup link already points to {source}")
        return

    _remove_existing_target(target)

    if force_copy:
        shutil.copy2(source, target)
        print(f"[ok] Copied startup file to {target}")
        return

    try:
        os.symlink(str(source), str(target))
        print(f"[ok] Linked {target} -> {source}")
    except OSError as error:
        # Windows can reject symlink creation when Developer Mode/admin is unavailable.
        shutil.copy2(source, target)
        print(f"[warn] Symlink failed ({error}); copied file instead: {target}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Set up local Lean research environment"
    )
    parser.add_argument(
        "--workspace",
        default=str(Path(__file__).resolve().parents[1]),
        help="Lean workspace root (defaults to this repo root)",
    )
    parser.add_argument(
        "--build-dir",
        default="Launcher/bin/Debug",
        help="Path (relative to workspace unless absolute) to launcher build output",
    )
    parser.add_argument(
        "--env-name",
        default="lean-py311",
        help="Conda environment name defined in environment.python311.yml",
    )
    parser.add_argument(
        "--env-prefix",
        default=".conda/lean-py311",
        help="Repo-local conda clone prefix (relative to workspace unless absolute)",
    )
    parser.add_argument(
        "--skip-conda",
        action="store_true",
        help="Skip conda environment creation/update",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip dotnet build even if launcher output is missing",
    )
    parser.add_argument(
        "--force-copy",
        action="store_true",
        help="Copy startup file instead of creating a symlink",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.workspace).resolve()

    build_dir = Path(args.build_dir)
    if not build_dir.is_absolute():
        build_dir = (repo_root / build_dir).resolve()

    env_prefix = Path(args.env_prefix)
    if not env_prefix.is_absolute():
        env_prefix = (repo_root / env_prefix).resolve()

    if not repo_root.exists():
        raise FileNotFoundError(f"Workspace not found: {repo_root}")

    print(f"[info] Workspace: {repo_root}")
    print(f"[info] Build dir: {build_dir}")

    if not args.skip_conda:
        _ensure_conda_env(repo_root, args.env_name, env_prefix)

    _ensure_build_output(repo_root, build_dir, args.skip_build)
    start_source = _ensure_startup_files(repo_root, build_dir)

    startup_target = _ipython_startup_target()
    _link_or_copy_startup(start_source, startup_target, args.force_copy)

    print("[done] Lean research setup complete")
    print(
        f"[next] Start research with: {repo_root / '.vscode' / 'launch_research.sh'} {build_dir}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[error] {exc}", file=sys.stderr)
        raise SystemExit(1)
