from utils.rtext import *
import time
import shutil

# ================== Part Can Modifie Start ==================

# The folder contians the world folder and the server.jar file of the survival server.
SurvivalServerPath = "../survival/server"
# The folder contians the world folder and the server.jar file of the mirror server.
MirrorServerPath = "./server"
# World list to sync
# For Vanilla servers: world_list = ["world",]
# For Spoiget servers: WorldNames = ['world','world_nether','world_the_end']
WorldNames = ["world",]
# The count down after executing "!!mirror commit"
CountDown = 10
# owner	4	Highest level for those who have the ability to access the physical server
# admin	3	People with power to control the MCDR and the server
# helper	2	A group of admin's helper
# user	1	A group that normal player will be in
# guest	0	The lowest level for guest or trollers
MinimumPermissionLevel = 3
# The command prefix
Prefix = "!!mirror"

# ================== Part Can Modifie End ==================

plugin_name = "MirrorSync"
help_msg = '''
======MCDR-MirrorSync======
§6{0} §rShow this message
§6{0} sync §aSync §rsurvival suit archive to mirror suit
§6{0} commit §aConfirmation of §roperation
§6{0} abort §cTermination of §roperation'''.format(Prefix)
format_error_msg = f"§cFormatting error！Use §6{Prefix}§cfor help！"

NEED_COMMIT = False
COUNTING = False
ABORT = False

def tell_msg(server, content, tell = False, player = None):
    global plugin_name
    content = f"[{plugin_name}] " + content
    if tell:
        if player != None:
            server.tell(player, content)
            return True
        else:
            return False
    else:
        server.say(content)

def sync_world(server):
    global SurvivalServerPath, MirrorServerPath, WorldNames

    for world in WorldNames:
        server.logger.info(f"[MirrorSync] Deleting world [{world}]")
        shutil.rmtree(f"{MirrorServerPath}/{world}")

    for world in WorldNames:
        server.logger.info(f"[MirrorSync] Copying world [{world}]")
        shutil.copytree(f"{SurvivalServerPath}/{world}", f"{MirrorServerPath}/{world}")

    server.logger.info("[MirrorSync] Done!")
    return True


def on_info(server, info):
    global MinimumPermissionLevel, CountDown
    global NEED_COMMIT, COUNTING, ABORT
    content = info.content
    cmd = content.split()
    if len(cmd) == 0 or cmd[0] != Prefix:
        return
    del cmd[0]

    if server.get_permission_level(info) < MinimumPermissionLevel:
        tell_msg(server, "§cYou do not have permission to execute this command", True, info.player)
        return

    if len(cmd) == 0:
        tell_msg(server, help_msg, True, info.player)
        return

    if cmd[0] == "sync":
        if len(cmd) != 1:
            tell_msg(server, format_error_msg, True, info.player)
            return
        NEED_COMMIT = True
        tell_msg(server, "§aPlease enter §6!!mirror commit §ato confirm the operation", False)

    if cmd[0] == "commit":
        if len(cmd) != 1:
            tell_msg(server, format_error_msg, True, info.player)
            return
        if NEED_COMMIT == False:
            tell_msg(server, "§cThere is nothing to confirm", False)
            return

        tell_msg(server, "§aOperation confirmation", False)
        NEED_COMMIT = False

        ### COUNT DOWN AND SYNC ###

        COUNTING = True

        for countdown in range(0, CountDown):
            tell_msg(server, f"还有{CountDown-countdown}秒")
            if ABORT:
                ABORT = False
                break
            time.sleep(1)

        server.stop()
        server.logger.info("[MirrorSync] Waiting for server to stop.")
        server.wait_for_start()

        sync_world(server)

        server.start()

        return

    if cmd[0] == "abort":
        if COUNTING == True or NEED_COMMIT == True:
            tell_msg(server, "§cOperation termination", False)
            ABORT = True
            COUNTING = NEED_COMMIT = False
            return
        tell_msg(server, "§cThere is nothing to end", False)
        
def on_load(server, old_module):
    global Prefix
    server.add_help_message(Prefix, "MirrorSync Help")