import time

# Edit this to change the delay
DELAY = 1

Prefix = "!!perimeter"
help_msg = '''========== Perimeter Maker ==========
§6{0}§r Show this message
§6{0} make §b<length> <width>§r Clear a perimeter centred on the current position
§6{0} commit§r Use after using make to confirm the operation
§6{0} abort§r Interrupt the operation at any time'''.format(Prefix)
CHUNK = 16

ABORT = False
WORKING = False
NEED_COMMIT = False

p1 = None
p2 = None
p3 = None
p4 = None

def on_info(server, info):
    global help_msg, Prefix, DELAY
    global CHUNK, ABORT, WORKING, NEED_COMMIT
    global p1, p2, p3, p4
    content = info.content
    cmd = content.split()
    if len(cmd) == 0 or cmd[0] != Prefix:
        return
    del cmd[0]
    # !!perimeter help
    if len(cmd) == 1 and cmd[0] == "help":
        server.reply(info, help_msg)
        return
    # !!perimeter abort
    if len(cmd) == 1 and cmd[0] == "abort":
        if not WORKING and not NEED_COMMIT:
            server.reply(info, "§cNo operations requiring interruption")
            return
        ABORT = True
        NEED_COMMIT = False
        server.reply(info, "§cTermination of operation！")
        return
    # !!perimeter abort <length> <width>
    if len(cmd) == 3 and cmd[0] == "make":
        if WORKING:
            server.reply(info, "§cCurrently being cleared, please wait for the making of the perimeter to be completed！")
        try:
            p1 = -int(cmd[1])/2 * CHUNK
            p2 = int(cmd[1])/2 * CHUNK
            p3 = -int(cmd[2])/2 * CHUNK
            p4 = int(cmd[2])/2 * CHUNK
        except:
            server.reply(info, "§cInput is not a number！")
        
        NEED_COMMIT = True
        server.reply(info, "§aPlease enter§6{} commit §aConfirmation of operation！".format(Prefix))

    if len(cmd) == 1 and cmd[0] == "commit":

        if not NEED_COMMIT:
            server.reply(info, "§cThere are no operations that require confirmation")
            return

        server.say("§aStart the operation! Please wait patiently in §cin place §a, §cdo not move")
        NEED_COMMIT = False

        server.execute("carpet fillLimit 1000000")
        
        WORKING = True
        for i in range(0, 254):
            if ABORT:
                ABORT = False
                WORKING = False
                break
            y = 255 - i
            command = "execute at {} run fill ~{} {} ~{} ~{} {} ~{} air".format(info.player, p1, y, p3, p2, y, p4)
            server.say("Layer {} is being replaced".format(y))
            time.sleep(DELAY)
            server.execute(command)
        WORKING = False

def on_load(server, old_module):
    global Prefix
    server.add_help_message(Prefix + " help", "Create perimeter help")