"""
this module handles pip installation in unreal engine
"""

from pathlib import Path
import subprocess
import unreal
import pkg_resources


class PipCommands:
    """reference for pip commands"""
    INSTALL = 'install'
    UNINSTALL = 'uninstall'
    INSPECT = 'inspect'
    DOWNLOAD = 'download'
    FREEZE = 'freeze'
    LIST = 'list'
    SHOW = 'show'
    SEARCH = 'search'
    CHECK = 'check'
    CONFIG = 'config'
    WHEEL = 'wheel'
    HASH = 'hash'
    CACHE = 'cache'
    DEBUG = 'debug'


def get_python_interpreter_path() -> Path:
    """get the path to the python interpreter in the unreal engine installation"""
    interpreter_path = Path(unreal.get_interpreter_executable_path())
    assert interpreter_path.exists(), f"Python not found at '{interpreter_path}'"
    return interpreter_path


def _install(package_names: list, short_args: list = None, long_args: list = None):
    return _pip_cmd(
        command=PipCommands.INSTALL,
        short_args=short_args,
        long_args=long_args,
        args=package_names,
    )


def _uninstall(package_names: list, short_args: list = None, long_args: list = None):
    return _pip_cmd(
        command=PipCommands.UNINSTALL,
        short_args=short_args,
        long_args=long_args,
        args=package_names,
    )


def _pip_cmd(
        command: str = None,
        short_args: list = None,
        long_args: list = None,
        args: (set, list) = None,
):
    """
    pip-install python packages in Unreal. Doesn't filter missing packages.

    Args:
        command (str): names of PyPi packages to install
        short_args (list): - short option arguments, [(name, value), ...] e.g. [('r', 'C:/requirements.txt')]
        long_args (list): -- long option arguments, [(name, value), ...] e.g. [('requirement', 'C:/requirements.txt')]
        args (list): pure values, used for package names in install e.g. ['Pyside2', 'numpy']

    Flags without value use an empty string as value e.g. [('dry-run', '')]
    Don't wrap values in double quotes if they contain spaces
    """

    options = []  # list cause order matters

    if short_args:
        for option, value in short_args:
            options.append(f"-{option}")
            if value != "":  # allow 0 as value
                options.append(value)

    if long_args:
        for option, value in long_args:
            options.append(f"--{option}")
            if value != "":  # allow 0 as value
                options.append(value)

    if not args:
        args = []

    interpreter_path = get_python_interpreter_path()

    # don't show window
    info = subprocess.STARTUPINFO()
    info.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    process = subprocess.Popen(
        [interpreter_path, '-m', 'pip', command, *options, *args],
        startupinfo=info,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )

    while process.poll() is None:
        unreal.log(process.stdout.readline().strip())
        unreal.log_warning(process.stderr.readline().strip())
    return process.poll()


def install(package_names):
    """
    Install missing python packages with pip
    """
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing_packages = set(package_names) - installed

    # by default, pip installs to user appdata, not the project directory!
    # let's install to the project directory instead
    relative_engine_path = unreal.Paths.engine_dir()
    engine_path = unreal.Paths.convert_relative_path_to_full(relative_engine_path)
    target_path = Path(engine_path) / r"Binaries\ThirdParty\Python3\Win64\Lib\site-packages"

    if missing_packages:
        _install(missing_packages,
                 long_args=[('target', f'{target_path}')])
    else:
        unreal.log("All python requirements already satisfied")


def uninstall(package_names: (list, set)):
    """
    Uninstall python packages with pip
    """
    installed = {pkg.key for pkg in pkg_resources.working_set}
    packages_to_uninstall = set(package_names) & installed

    if packages_to_uninstall:
        _uninstall(packages_to_uninstall)
    else:
        unreal.log("All python packages are already uninstalled")
