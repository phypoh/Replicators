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
import config
import main
from discord.ext.commands.cooldowns import BucketType

# BOT VARIABLES
nameBOT = "EZLBot"
OWNERS = ['198255568882761728', '164026892796690433', '102704301956149248', '139537219793715200']  # When you want to AUTHENTICATE the AUTHOR
# serverprefixes = {}

# EMBED VARIABLES
NAME = "EZLBot"
FOOTER = "Thanks to SEMC and MadGlory made with love ~ xoxo"
PROFILEIMG = "http://i64.tinypic.com/2q24gsj.jpg"

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

            notice = "I'm in **" + str(len(self.bot.servers)) + "** servers total!"

            await self.bot.edit_message(msg, notice)

        elif command == "notice":
            msg = raw.message.content
            msg = msg.split("notice")

            # FOR DEBUGGING
            # print(msg)

            for server in self.bot.servers:
                try:
                    await self.bot.send_message(server.default_channel, msg[1])

                except:
                    try:
                        print("Couldn't send notice to:   " + str(server.name))

                    except:
                        pass
        else:
            try:
                await self.bot.say(str(command) + " isn't a valid extension command... :sweat_smile:")
            except:
                pass

    # Gives a LINK from where one CAN add THIS BOT
    @commands.command()
    async def invite(self):
        """When you want to invite this bot to another server."""

        await self.bot.say("You can invite me to any server at:\nhttp://ezlgg.com/bot")

    # Gives a DESCRIPTION of the BOT
    @commands.command()
    async def about(self):
        """Gives you some info on this bot."""

        embed = discord.Embed(title="About", url="https://discordapp.com", description="Hi, I'm **" + str(NAME) + "**, developed by Halcyon Hackers with love, python, and VG API. I'm a growing community bot that has new features added regularly. For now I control VG soon I will control the world. :smiley:")

        embed.set_author(name="EZLBot", url="http://ezlgg.com/bot", icon_url=PROFILEIMG)
        embed.set_footer(text=FOOTER, icon_url=PROFILEIMG)

        embed.add_field(name="What Can I Do?", value="For a quick look at what I can do type $help, but for a detailed list, please check http://ezlgg.com/ezlbot-documentation/")
        embed.add_field(name="Talk To My Developers!", value="Come join us at http://discord.me/EZLBot. If you believe you found a bug, error, need to report something contact us by sending a message. $report message Fair warning, use this too much and you will lose it. With great power comes great responsibility.")
        embed.add_field(name="Bot Status:", value="Servers I'm In: " + str(len(self.bot.servers)))

        await self.bot.say(embed=embed)

    # Used to CHANGE the PREFIX
    @commands.command(pass_context=True)
    async def prefix(self, raw, prefix=""):
        """Used to change server's prefix.

                >prefix (new_prefix)
            new_prefix   ~   Any combinations of character that isn't separated with space

            Example:
                >prefix Ezl1!
        """

        prefix = str(prefix)  # CONVERT PREFIX to STRING to prevent ERRORS

        if prefix == "":
            await self.bot.say("You need to give a **prefix**... :sweat_smile:")
            return

        if not raw.message.author.permissions_in(raw.message.channel).administrator:
            await self.bot.say('Sorry, but you have to be an **admin** to change the prefix.')
            return

        config.serverprefixes[raw.message.server.id] = prefix

        await self.bot.say("**prefixed changed to " + str(
            prefix) + "**\nPlease don't forget your new prefix.\nWant me good as new? Just kick me out of the server and reinvite me.")
        main.storePrefix()

    # Used to SEND a COMPLAINT
    @commands.command(pass_context=True)
    @commands.cooldown(1, 3600, BucketType.user)
    async def report(self, raw, prefix=""):
        """Report an instance involving the bot.

                >complaint (message)
            message   ~   Report message

            Example:
                >report My guild was taken by someone else contact me at player1#7777

        """

        msg = raw.message.content
        author = raw.message.author
        server = raw.message.server
        msg = msg.split("report ", 1)

        # FOR DEBUGGING
        # print(msg)

        report = "FROM: " + str(author) + " | SERVER: " + str(server) + "\nMSG:   " + str(msg[1])

        try:
            await self.bot.send_message(self.bot.get_channel("292168218385055744"), report)
            await self.bot.say("Report Sent :ok_hand:")

        except:
            print("Couldn't send report:   " + str(msg[1]))

def setup(bot):
    bot.add_cog(Bot(bot))
