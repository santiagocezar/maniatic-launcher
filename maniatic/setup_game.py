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


def find_data() -> bool:
    if DATA_DEST.exists():
        return True

    for path in DATA_FILES:
        if path.exists():
            sh.copy(path, DATA_DEST)
            return True

    return False


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
