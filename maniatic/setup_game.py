from configparser import ConfigParser
from pathlib import Path
from subprocess import call
import shutil as sh
import os

DATA_FILES = [
    Path.home()
    / ".var/app/com.valvesoftware.Steam/.steam/steam/steamapps/common/Sonic Mania/Data.rsdk",
    Path.home() / ".local/share/Steam/steamapps/common/Sonic Mania/Data.rsdk",
]

DATA_DEST = Path.home() / "Data.rsdk"


def find_data() -> bool:
    if DATA_DEST.exists():
        return True

    for path in DATA_FILES:
        if path.exists():
            sh.copy(path, DATA_DEST)
            return True

    return False


MODS_DEST = Path.home() / "mods"
MOD_NAME = "OpenGL-Shaders"
OGL_MOD_PATH = Path("/app/share") / MOD_NAME


def install_shaders():
    MODS_DEST.mkdir(exist_ok=True)
    if not (MODS_DEST / MOD_NAME).exists():
        (MODS_DEST / MOD_NAME).symlink_to(OGL_MOD_PATH, target_is_directory=True)

        mods = ConfigParser()
        mods.optionxform = str
        mods.read(MODS_DEST / "modconfig.ini")

        if "Mods" not in mods:
            mods["Mods"] = {}
        mods["Mods"][MOD_NAME] = "y"

        with open(MODS_DEST / "modconfig.ini", "wt") as f:
            mods.write(f)


def launch_game() -> int:
    if not DATA_DEST.exists():
        return 1

    return call(
        "RSDKv5U",
        # load Game.so from /app/lib instead of symlinking to the cwd
        env=dict(
            os.environ,
            LD_LIBRARY_PATH="/app/lib",
        ),
    )
