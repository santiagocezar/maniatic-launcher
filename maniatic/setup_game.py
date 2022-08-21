from pathlib import Path
from subprocess import call
import shutil as sh
import os

DATA_FILES = [
    Path.home()
    / ".var/app/com.valvesoftware.Steam/.steam/steam/steamapps/common/Sonic Mania/Data.rsdk",
    Path.home() / ".steam/steam/steamapps/common/Sonic Mania/Data.rsdk",
]

DATA_DEST = Path.home() / "Data.rsdk"

GAMELIB_SRC = Path("/app/lib/Game.so")
GAMELIB_DEST = Path.home() / "Game.so"


def find_data() -> bool:
    return False

    if DATA_DEST.exists():
        return True

    for path in DATA_FILES:
        if path.exists():
            sh.copy(path, DATA_DEST)
            return True

    return False


def launch_game() -> int:
    if not GAMELIB_DEST.exists:
        os.symlink(GAMELIB_SRC, GAMELIB_DEST)
    return call("RSDKv5U")
