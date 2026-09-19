from __future__ import annotations

from worlds.AutoWorld import World
from worlds.LauncherComponents import Component, components
from multiprocessing import Process

from .world import BKClownWorld as BKClownWorld
from . import components as components

def run_client():
    from .BKCLOWNCLIENT import main
    p = Process(target=main)
    p.start()

components.append(Component("BKClown Client", func=run_client))

def data_path(file_name: str):
    import pkgutil
    return pkgutil.get_data(__name__, "patchfile/" + file_name)