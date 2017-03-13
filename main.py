import discord
from discord.ext import commands
import config
import pickle

keyBot = ""
startup_extensions = ["BOT_commands", 'VG_commands']
descriptionBOT = "EZLBot is a bot created for Discord to utilize the VG api!"

bot = commands.Bot(command_prefix='$', description=descriptionBOT)

OWNERS = ['198255568882761728', '164026892796690433', '102704301956149248', '139537219793715200']  # When you want to AUTHENTICATE the AUTHOR
# serverprefixes = {}  # DICTIONARY of all SERVERS PREFIX

# Loads serverprefixes dict from the pickle file
try:
    with open('prefixes.pickle', 'rb') as handle:
        config.serverprefixes = pickle.load(handle)

    with open('playersVGQ.pickle', 'rb') as handle:
        config.playersVGQ = pickle.load(handle)

    # FOR DEBUGGING
    # print(str(config.serverprefixes) + "   |   LOADED PREFIXES")
    # print(str(config.playersVGQ) + "   |   LOADED PLAYERVGQ")

except:
    print("No Prefixes Yet")

# Do when the BOT is ready to RUN
@bot.event
async def on_ready():
    print('Logged In As: ' + bot.user.name + "  ID:  " + bot.user.id + "\n\n")  # PRINT the IDENTIFIERS of the BOT
    await bot.change_presence(game=discord.Game(name='$help'))


# CHECK for server PREFIX
@bot.event
async def on_message(message):
    # FOR DEBUGGING
    # print(str(config.serverprefixes) + "   |   REAL TIME PREFIXES")

    prefix = config.serverprefixes.get(message.server.id, '$')  # Get the PREFIX for SERVER
    bot.command_prefix = [prefix]
    await bot.process_commands(message)


# STORE PREFIXES into SERVERPREFIXES
def storePrefix():
    # Store data (serialize)
    with open('prefixes.pickle', 'wb') as handle:
        pickle.dump(config.serverprefixes, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # FOR DEBUGGING
    # print(str(config.serverprefixes) + "   |   AFTER STORING")


# REMOVES PREFIX ON SERVER REMOVAL
@bot.event
async def on_server_remove(server):
    config.serverprefixes.pop(server.id, None)
    storePrefix()


    # FOR DEBUGGING
    # print(config.serverprefixes)


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


@owner.command(pass_context=True, hidden=True)
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
