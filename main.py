import discord
from discord.ext import commands
import pickle

keyBot = ""
startup_extensions = ["BOT_commands", 'VG_commands']
descriptionBOT = "EZLBot is a bot created for Discord to utilize the VG api!"

bot = commands.Bot(command_prefix='$', description=descriptionBOT)

OWNER = ['198255568882761728', '164026892796690433', '102704301956149248', '139537219793715200']
serverprefix = {}

#loads serverprefix dict from pickle file
try:
    with open('prefixes.pickle', 'rb') as handle:
        serverprefix = pickle.load(handle)
except:
    print('No Prefixes Yet')

def storePrefix():
    # Store data (serialize)
    with open('prefixes.pickle', 'wb') as handle:
        pickle.dump(serverprefix, handle, protocol=pickle.HIGHEST_PROTOCOL)

#Checks for server prefix
@bot.event
async def on_message(message):
    pr = serverprefix.get(message.server.id, '$')
    bot.command_prefix = [pr]
    await bot.process_commands(message)

@bot.event
async def on_server_join(server):
    await bot.send_message(server.default_channel, 'Hey! Thanks for the invite <3 Use {}help to get started'.format(bot.command_prefix[0]))

#Removes prefix on server removal
@bot.event
async def on_server_remove(server):
    serverprefix.pop(server.id, None)
    storePrefix()
#Used to change the prefix

@bot.command(pass_context=True)
async def specialannouncement(ctx, *, msg: str):
    if ctx.message.author.id not in OWNER:
        return
    for i in bot.servers:
        await bot.send_message(i.default_channel, msg)
        
@bot.command(pass_context=True)
async def prefix(ctx, prefix: str):
    """
    Used to change server's prefix.
    """
    if not ctx.message.author.permissions_in(ctx.message.channel).administrator:
        await bot.say('Sorry, but you have to be an admin to change the prefix.')
    serverprefix[ctx.message.server.id] = prefix
    await bot.say("PREFIX CHANGED to {}".format(prefix))
    await bot.say("Please don't forget your new prefix. To reset it back to default just kick me out of the server and reinvite me.")
    storePrefix()

@bot.group(pass_context=True)
async def owner(ctx):
    """ONLY FOR BOT OWNERS"""
    pass

@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name='$help'))
    
@owner.command(pass_context=True)
async def load(ctx, module: str):
    if ctx.message.author.id not in OWNER:
        return
    bot.load_extension(module)
    await bot.say("K")

@owner.command(pass_context=True)
async def unload(ctx, module: str):
    if ctx.message.author.id not in OWNER:
        return
    bot.unload_extension(module)
    await bot.say("K")

@owner.command(pass_context = True)
async def reload(ctx, module: str):
    if ctx.message.author.id not in OWNER:
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
