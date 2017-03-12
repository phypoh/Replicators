# Body Commands:
# File containing all of the BOT commands for Discord
"""

List of Commands:
developer   ~   extension commands: servers
invite
bot

"""

# IMPORTS
from discord.ext import commands
import main

# BOT VARIABLES
nameBOT = "EZLBot"
OWNERS = ['198255568882761728', '164026892796690433', '102704301956149248', '139537219793715200']  # When you want to AUTHENTICATE the AUTHOR
# serverprefixes = {}

# CLASS containing ALL COMMANDS for THIS MODULE
class Bot():
    """Basic bot Commands.

            Made using Discord.py

    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, hidden=True)
    async def developer(self, raw, command=""):
        """A command used by developers.

                >developer (command)

            command   ~   Command you would like to run   ~   Options: servers - list of all servers I'm in, notice - send message to all servers I'm in

            Example:
                >player notice This is the message I'll be sending to all the servers!!!

        """

        # author = msg.message.author  # Get the AUTHOR of the MESSAGE
        # channel = msg.message.channel  # Get the CHANNEL of the MESSAGE
        discordID = str(raw.message.author.id)
        # FOR DEBUGGING
        # print(discordID)
        if discordID in OWNERS:
            pass

        else:
            await self.bot.say("You aren't a developer! :stuck_out_tongue_closed_eyes:")
            return

        if command == "":
            await self.bot.say("You need to input an extension command... :sweat_smile:")
            return

        if command == "servers":
            msg = await self.bot.say("Running " + str(command) + "... :eyes:")

            notice = "I'm in **" + str(len(self.bot.servers)) + "** servers total!\nNames are the Following:\n"

            for server in self.bot.servers:
                notice += str(server.name)

            await self.bot.edit_message(msg, notice)

        if command == "notice":
            msg = raw.message.content
            msg = msg.split("notice")

            # FOR DEBUGGING
            # print(msg)

            for server in self.bot.servers:
                await self.bot.send_message(server.default_channel, msg[1])

        else:
            await self.bot.say(str(command) + " isn't a valid extension command... :sweat_smile:")

    # Gives a LINK from where one CAN add THIS BOT
    @commands.command()
    async def invite(self):
        """When you want to invite this bot to another server."""

        await self.bot.say("You can invite me to any server at:\nhttp://ezlgg.com/bot")

    # Gives a DESCRIPTION of the BOT
    @commands.command()
    async def about(self):
        """Gives you some info on this bot."""

        await self.bot.say("Hi, I'm *" + str(nameBOT) + "*, and I've been developed in Python and have grown with lots of love. You can see a list of our commands with the **help** command!")

    # STORE PREFIXES into SERVERPREFIXES
    # def storePrefix():
    #     # Store data (serialize)
    #     with open('prefixes.pickle', 'wb') as handle:
    #         pickle.dump(serverprefixes, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Used to CHANGE the PREFIX
    @commands.command(pass_context=True)
    async def prefix(self, raw, prefix=""):
        """Used to change server's prefix."""

        prefix = str(prefix)  # CONVERT PREFIX to STRING to prevent ERRORS

        if prefix == "":
            await self.bot.say("You need to give a **prefix**... :sweat_smile:")
            return

        if not raw.message.author.permissions_in(raw.message.channel).administrator:
            await self.bot.say('Sorry, but you have to be an **admin** to change the prefix.')
            return

        main.serverprefixes[raw.message.server.id] = prefix
        # list = [raw.message.server.id, prefix]

        await self.bot.say("**prefixed changed to " + str(prefix) + "**\nPlease don't forget your new prefix.\nWant me good as new? Just kick me out of the server and reinvite me.")
        main.storePrefix()

def setup(bot):
    bot.add_cog(Bot(bot))
