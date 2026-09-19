#thank you to EviVirus' fnafw client and Mewlif's old FFPS client for helping me understand how clickteam studio clients function <3
from __future__ import annotations

import Utils
import os


import bsdiff4
import asyncio

from CommonClient import *

from worlds import BKClown

import bsdiff4
class BKCLOWNPROCESSOR(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_patch(self):
        """Patch FFPS"""
        with open(Utils.user_path("BKCLOWN", "Pizzeria Simulator.exe"), "rb") as f:
            patchfile = bsdiff4.patch(f.read(), BKClown.data_path("BKClown.bsdiff"))
        with open(Utils.user_path("BKCLOWN", "BKCLOWN.exe"), "wb") as f:
            f.write(patchfile)
        self.output(f"Finished Patch!")


class BKClownContext(CommonContext):
    command_processor = BKCLOWNPROCESSOR
    game = "BKClown"
    items_handling = 0b111  # full remote
 
    def __init__(self, server_adress, password):
        super().__init__(server_adress, password)
        self.syncing = False
        self.FruitProgressiveChild = 0
        self.LemonadeProgressiveChild = 0
        self.game = 'BKClown'

    def on_package(self, cmd: str, args: dict):
        asyncio.create_task(process_bkclown_stuff(self, cmd, args))

    def run_gui(self):
        from kvui import GameManager

        class BKClownManager(GameManager):
            logging_pairs = [("Client", "Archipelago")]
            base_title = f"Archipelago BKClown Client"

        self.ui = BKClownManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    async def server_auth(self, password_requested: bool = False):

        if password_requested and not self.password:
            await super().server_auth(password_requested)

        await self.get_username()
        await self.send_connect(game = self.game)

async def main(args):

    ctx = BKClownContext(args.connect, args.password)
    ctx.run_gui()

    await ctx.exit_event.wait()
    await ctx.shutdown()

async def process_bkclown_stuff(ctx: BKClownContext, cmd: str, args: dict):
    if cmd == 'Connected':

        path = os.path.expandvars(r"%appdata%\MMFApplications\BKClown")

        if os.path.exists(path):
            with open(path, "w") as f:
                f.write("[]\n")
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write("[]\n")
        ctx.finished_game = False
        ctx.FruitProgressiveChild = 9
        ctx.LemonadeProgressiveChild = 9
        ctx.LemonAdded = args["slot_data"]["LemonAdded"]
        
        if os.path.exists(os.path.expandvars(r"%appdata%\MMFApplications\BKClown")):
            with open(path, "w") as f:
                f.write(
                    "[]\n"
                    "fruitpunchunlocked=1\n"
                    "perfectscore=0\n"
                    "previousscore=0\n" 
                    "highscore=0\n"      
                    )
                
    elif cmd == 'ReceivedItems':

        start_index = args["index"]

        if start_index == 0:
            ctx.items_received = []

        if start_index != len(ctx.items_received):
            sync_msg = [{'cmd': 'Sync'}]

            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks",
                "locations": list(ctx.locations_checked)})

            await ctx.send_msgs(sync_msg)


        else:
            path = os.path.expandvars(r"%appdata%\MMFApplications\BKClown")

            readlines = []

            if os.path.exists(os.path.expandvars(r"%appdata%\MMFApplications\BKClown")):

                childrentoappend = []
                lemonadded = False

                with open(path, "r") as f:
                    readlines = f.readlines()
                existinglines = {lines.strip() for lines in readlines}
                    
                for item in args['items']:
                    ctx.items_received.append(NetworkItem(*item))
                for itm in ctx.items_received:
                    if itm.item == 4:
                        lemonadded = True

                fruitchildcount = sum(1 for itm in ctx.items_received if itm.item == 1)



                if fruitchildcount >= ctx.FruitProgressiveChild:
                    fruitchildcount = ctx.FruitProgressiveChild

                lemonadechildcount = 0

                if ctx.LemonAdded:
                    lemonadechildcount = sum(1 for itm in ctx.items_received if itm.item == 2)
    
                    if lemonadechildcount >= ctx.LemonadeProgressiveChild:
                        fruitchildcount = ctx.LemonadeProgressiveChild

                for i in range(fruitchildcount):
                    childrentoappend.append("progressivekid" + str(i) + "=1\n")
                for i in range(lemonadechildcount):
                    childrentoappend.append("progressivelemonadekid" + str(i) + "=1\n")
                if lemonadded:
                    if not existinglines.__contains__("lemonadeunlocked"):
                        childrentoappend.append("lemonadeunlocked=1\n")
                        childrentoappend.append("previouslemonadescore=0\n")
                        childrentoappend.append("lemonadehighscore=0\n")
                elif ctx.LemonAdded == False:
                    childrentoappend.append("lemonadeunlocked=NEVER\n")
                lastappend = []
                for line in childrentoappend:
                    if line.strip() not in existinglines:
                        lastappend.append(line)

                if lastappend:
                    with open(path, "a") as f:
                        f.writelines(lastappend)

async def game_watcher(ctx:BKClownContext):

    scorescheck = [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 11800]
    lemonscores = [150, 300, 450, 600, 750, 900, 1050, 1200, 6350]
    path = os.path.expandvars(r"%appdata%\MMFApplications\BKClown")

    while not ctx.exit_event.is_set():

        if ctx.syncing:
            sync_msg = [{'cmd': 'Sync'}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
                
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False

        locationcheck = []
        linesread = ""
        victory = False

        if os.path.exists(path):
                
                try:
                    with open(path, "r") as f:
                        linesread = f.read()

                except IOError:
                    pass

                for scores in scorescheck:
                    if f"highscore={scores}" in linesread and not linesread.__contains__("highscore=0"):
                        match = scores // 200
                        locationcheck.append(match)

                    if f"highscore=0" in linesread or f"previousscore=0" in linesread:
                        locationcheck.append(int(100))

                    if linesread.__contains__("highscore=11800"):
                        locationcheck.append(int(9))
                if linesread.__contains__("lemonadeunlocked=1"):
                    for scores in lemonscores:

                        if f"lemonadehighscore=0" in linesread or f"previouslemonadescore=0" in linesread:
                            locationcheck.append(101)
                        
                        if f"lemonadehighscore={scores}" in linesread:
                            locationcheck.append(scores)

                        if linesread.__contains__("highscore=11800") and linesread.__contains__("lemonadehighscore=6350"):
                            victory = True
                elif linesread.__contains__("lemonadeunlocked=NEVER"):
                    if linesread.__contains__("highscore=11800"):
                        victory = True

        if not ctx.finished_game and victory:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

        if locationcheck != set(ctx.locations_checked):           
            ctx.locations_checked = locationcheck
            message = [{"cmd": 'LocationChecks', "locations": locationcheck}]
            await ctx.send_msgs(message)

        await asyncio.sleep(1.0)

    Utils.init_logging("BKCLOWNCLIENT", exception_logger="Client")
    async def _main():
        parser = get_base_parser(description="BKClown Client, for text interfacing.")   
        args = parser.parse_args()

        ctx = BKClownContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        progression_watcher = asyncio.create_task(
            game_watcher(ctx), name="BKClownProgressionWatcher")
        if not os.path.exists(os.getcwd() + "/BKCLOWN"):
            os.mkdir(os.getcwd() + "/BKCLOWN")
        await ctx.exit_event.wait()

        ctx.server_address = None 

        await progression_watcher

        await ctx.shutdown()

    import colorama

    colorama.init()

    asyncio.run(_main())
    colorama.deinit()


if __name__ == "__main__":
    main()

                                

