# Main:
# Where all Discord events are handled

# IMPORTS
import discord
from discord.ext import commands
import BOT_module
import VG_module

# Discord Variables--
keyDISCORD = ""  # DISCORD_BOT_TOKEN_HERE"
bot = commands.Bot(command_prefix=">")


# Whenever BOT is READY
@bot.event
async def on_ready():
    print('Logged In As: ' + bot.user.name + "  ID:  " + bot.user.id + "\n\n")


# Whenever a MESSAGE is SENT STARTING with COMMAND PREFIX, ">".
@bot.command()
async def guide():  # BOT gives a list of possible commands in CURRENT CHANNEL
    await bot.say("```List of Commands:\n> ~ used to issue commands\n>catch\n>guide ~ a list of possible commands\n>bot help ~ a list of possible commands for bot module\n>vg help ~ a list of possible commands for VG module```")


@bot.command(pass_context=True)
async def computer(msg, part1="", part2=""):
    author = msg.message.author
    channel = msg.message.channel

    await BOT_module.commandBOT(bot, author, channel, part1, part2)


@bot.command()
async def vg(part1="", part2=""):
    await VG_module.commandVG(bot, part1, part2)

# RUNS BOT with Discord KEY
bot.run(keyDISCORD)
