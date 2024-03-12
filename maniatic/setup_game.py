from configparser import ConfigParser
from pathlib import Path
from subprocess import call
import shutil as sh
import os
import urllib.request
import io
import zipfile


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

def install_mod(mod_url: str):
    MODS_DEST.mkdir(exist_ok=True)

    res = urllib.request.urlopen(mod_url.split(",")[0])
    length = int(res.getheader('content-length'))

    print(f"downloading {length} bytes")

    Path("mods").mkdir(exist_ok=True)

    with open("/tmp/mod.zip", "wb") as mod_zip:
        size = 0
        while True:
            block = res.read(4096)
            if not block:
                break
            mod_zip.write(block)
            size += len(block)
            if length:
                print('{:.2f}% done'.format(size / length * 100))

    print(f"extracting...")

    with zipfile.ZipFile("/tmp/mod.zip", "r") as zipf:
        zipf.extractall("mods")


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
