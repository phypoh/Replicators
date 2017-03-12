import discord
from discord.ext import commands
import pickle

keyBot = ""
startup_extensions = ["BOT_commands", 'VG_commands']
descriptionBOT = "EZLBot is a bot created for Discord to utilize the VG api!"

bot = commands.Bot(command_prefix='$', description=descriptionBOT)

OWNERS = ['198255568882761728', '164026892796690433', '102704301956149248', '139537219793715200']  # When you want to AUTHENTICATE the AUTHOR
serverprefixes = {}  # DICTIONARY of all SERVERS PREFIX


# Do when the BOT is ready to RUN
@bot.event
async def on_ready():
    print('Logged In As: ' + bot.user.name + "  ID:  " + bot.user.id + "\n\n")  # PRINT the IDENTIFIERS of the BOT
    await bot.change_presence(game=discord.Game(name='$help'))

    # Loads server prefix dict from pickle file
    try:
        with open('prefixes.pickle', 'rb') as handle:
            serverprefixes = pickle.load(handle)

    except:
        print('No Prefixes Yet')


# CHECK for server PREFIX
@bot.event
async def on_message(message):
    pr = serverprefixes.get(message.server.id, '$')
    bot.command_prefix = [pr]
    await bot.process_commands(message)

# # Used to CHANGE the PREFIX
# @bot.command(pass_context=True)
# async def prefix(raw, prefix=""):
#     """Used to change server's prefix."""
#
#     prefix = str(prefix)  # CONVERT PREFIX to STRING to prevent ERRORS
#
#     if prefix == "":
#         await bot.say("You need to give a **prefix**... :sweat_smile:")
#         return
#
#     if not raw.message.author.permissions_in(raw.message.channel).administrator:
#         await bot.say('Sorry, but you have to be an **admin** to change the prefix.')
#         return
#
#     serverprefixes[raw.message.server.id] = prefix
#     await bot.say("PREFIX CHANGED to {}".format(prefix))
#     await bot.say("Please don't forget your new prefix, **" + str(prefix) + "**. To reset it back to default just kick me out of the server and reinvite me.")
#     storePrefix()


# STORE PREFIXES into SERVERPREFIXES
def storePrefix():
    # Store data (serialize)
    with open('prefixes.pickle', 'wb') as handle:
        pickle.dump(serverprefixes, handle, protocol=pickle.HIGHEST_PROTOCOL)

# REMOVES PREFIX ON SERVER REMOVAL
@bot.event
async def on_server_remove(server):
    serverprefixes.pop(server.id, None)
    storePrefix()


# Group of commands for BOT DEVELOPERS
@bot.group(pass_context=True, hidden=True)
async def owner(ctx):
    """ONLY FOR BOT OWNERS"""
    pass


@owner.command(pass_context=True, hidden=True)
async def load(raw, module: str):
    if raw.message.author.id not in OWNERS:
        return

    bot.load_extension(module)
    await bot.say("K")


@owner.command(pass_context=True, hidden=True)
async def unload(raw, module: str):
    if raw.message.author.id not in OWNERS:
        return

    bot.unload_extension(module)
    await bot.say("K")

@owner.command(pass_context = True, hidden=True)
async def reload(ctx, module: str):
    if ctx.message.author.id not in OWNERS:
        return
    bot.unload_extension(module)
    bot.load_extension(module)
    await bot.say("K")

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    
    bot.run(keyBot)
