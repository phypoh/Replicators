# VG Commands:
# File containing all of VG commands for Discord
"""

List of Commands:
player
stats
match

"""

# IMPORTS
import gamelocker
from discord.ext import commands
import TOOL_module as tools
import VG_module
import VG_toolbox
import config
import pickle
import asyncio

# DISCORD EMBED VARIABLES--
botImageDISCORD = "http://i63.tinypic.com/9k6xcj.jpg"  # URL of BOTS IMAGE
signatureDISCORD = "Big Thanks to SEMC and MadGlory! Made with love."  # String used in FOOTER as MESSAGE
msgs = {}  # DICTIONARY OF ALL MATCHES MESSAGES

# Stores PLAYERVGQ DICT
def storePlayersVGQ():
    with open("playersVGQ.pickle", "wb") as handle:
        pickle.dump(config.playersVGQ, handle, protocol=pickle.HIGHEST_PROTOCOL)


# FOR DEBUGGING
# print(str(config.serverprefixes) + "   |   AFTER STORING")

# Checks if a NAME is VALID
def checkName(name):
    if name == "":
        return False

    elif tools.isIntTOOL(name) == True:
        return False

    elif len(name) < 3:
        return False

    elif len(name) > 16:
        return False

    else:
        return True


# Checks if a DATE is VALID
def checkDays(date):
    if date == "":
        return False

    elif tools.isIntTOOL(date) == False:
        return False

    elif date == False or date == True:
        return False

    else:
        return True


# Gives a VALID DATE
def giveDays(date):
    if checkDays(date) == False:
        return 31

    date = int(date)  # Convert DATE to INT to prevent ERRORS

    if date <= 0:
        return 1

    elif date > 93:
        return 93

    else:
        return date


# Checks if SERVER is Valid
def checkServer(server):
    if server == "":
        return False

    if tools.isIntTOOL(server) == True:
        return False

    server = str(server.lower())

    if VG_toolbox.isServerVG(server)== True:
        return True

    else:
        return False


# Gives a VALID SERVER
def giveServer(server):
    if checkServer(server) == False:
        return "na"

    server = str(server.lower())

    if server == "sea":
        return "sg"

    return server


# Checks if GAMEMODE is VALID
def checkGameMode(game_mode):
    if tools.isIntTOOL(game_mode) == True:
        return False

    game_modes = ["", "casual", "ranked", "royale", "blitz"]  # POSSIBLE GAME MODES
    game_mode = str(game_mode.lower())

    if game_mode in game_modes:
        return True

    else:
        return False


# Gives a VALID GAMEMODE
def giveGameMode(game_mode):
    if checkGameMode(game_mode) == False:
        return "any"

    game_mode = str(game_mode.lower())

    if game_mode == "":
        return "any"

    return game_mode

# Checks if AUTO is VALID
def checkAuto(auto):
    if auto == "":
        return False

    auto = str(auto)
    auto = str(auto.lower())

    if auto == "false" or auto == "true":
        return True

    else:
        return False

# Gives a VALID AUTO
def giveAuto(auto):
    if checkAuto(auto) == False:
        return False

    auto = str(auto)
    auto = str(auto.lower())

    if auto == "false":
        return False

    elif auto == "true":
        return True

    else:
        return False


# Checks if PAGES is VALID
def checkPages(pages):
    if pages == "":
        return False

    elif tools.isIntTOOL(pages) == False:
        return False

    elif pages == False or pages == True:
        return False

    else:
        return True


# GIVES VALID PAGES
def givePages(pages, mode=0):
    if checkPages(pages) == False:
        if mode == 0:
            return 25

        elif mode == 1:
            return 1

        else:
            return 1

    pages = int(pages)

    if pages <= 0:
        return 1

    elif pages > 50:
        return 50

    else:
        return pages

# CLASS containing ALL COMMANDS for THIS MODULE
class Vg():
    """All the commands in relation to Vainglory.

            Made with love and some Vainglory api, python - gamelocker.

    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def stats(self, raw, player_name="", server="na", game_mode="any", days="31", auto="False"):
        """Gets a players performance in the past days. Works with VGQ.

                >stats (player_name) (server) (game_mode) (days)
            player_name   ~   name of player to search for
            server        ~   the server to which the player belongs to    ~   default: na, options: na, eu, sea or sg, ea, sa
            game_mode     ~   game mode you would like performance check   ~   default: any, options: any, casual, ranked, royale, blitz
            days          ~   day range to search from                     ~   default: 31, options: maximum: 93, minimum: 1

            example:
                >stats player1 na casual 7

        """

        # AUTO IS A SECRET VARIABLE THAT MAKES COMPUTER CHECK EVERY SERVER FOR PLAYER !!!WASTE OF API KEY!!!
        # FALSE = WILL ONLY CHECK GIVEN SERVER, TRUE = WILL CHECK ALL SERVERS UNTIL FINDING PLAYER

        # Checks if NOTHING was GIVEN
        if player_name == "" and server == "na" and game_mode == "any" and days == "31" and auto == "False":

            # Get the AUTHORS ID
            discordID = raw.message.author.id

            # If author in VGQ then GET DATA
            data = config.playersVGQ.get(discordID, False)  # Get the AUTHORS VGQ INFO

            if data == False:
                await self.bot.say("You'll need to add yourself to the **VGQ** before using commands without arguments. :stuck_out_tounge:\nEnter the **help** command followed by **saveVG** to see more... :hugging:")
                return

            else:
                notice = "Looking at stats of **any** matches for **" + data["IGN"] + "** from the past **31** days in the **" + data["Region"] + "** region... :eyes:"  # MESSAGE being SENT BEFOREHAND

                msg = await self.bot.say(notice)
                output = VG_module.getPlayerPerformanceVG(data["IGN"], data["Region"], "", 31)

                if type(output) == str:
                    await self.bot.edit_message(msg, output)
                    return

                else:
                    await self.bot.edit_message(msg, embed=output)
                    return

        # FOR DEBUGGING
        # print("INPUT - PLAYER_NAME: " + str(player_name) + "   | GAME_MODE: " + str(game_mode) + "   | SERVER: " + str(server) + "   | DAYS: " + str(days) + "   | AUTO: " + str(auto))

        if checkName(player_name) == False:
            await self.bot.say("No valid player name was given... :sweat_smile:")
            return

        game_mode = giveGameMode(game_mode)

        server = giveServer(server)

        days = giveDays(days)

        auto = giveAuto(auto)

        # FOR DEBUGGING
        # print("NAME: " + player_name + "   | GAMEMODE: " + game_mode + "   | SERVER: " + server + "   | DAYS: " + str(days) + "   | AUTO: " + str(auto))

        notice = "Looking at stats of **" + str(game_mode) + "** matches for **" + str(player_name) + "** from the past **" + str(days) + "** days in the **" + str(server) + "** region... :eyes:"

        if auto == True:
            notice += "  -  **auto**"

        # NOTICE USER that THEIR COMMAND is being PROCESSED
        msg = await self.bot.say(notice)

        # RUNS PERFORMANCE FETCH and UPDATES MESSAGE once DONE
        output = VG_module.getPlayerPerformanceVG(player_name, server, game_mode, days, auto)
        if type(output) == str:
                await self.bot.edit_message(msg, output)
        else:
            await self.bot.edit_message(msg, embed=output)

    @commands.command(pass_context=True)
    async def player(self, raw, player_name="", server="na", auto="False"):
        """Checks if player exist in vainglory. Works with VGQ.

                >player (player_name) (server) (mode)
            player_name   ~   name of player to check for
            server        ~   the server to which the player belongs to    ~   default: na, options: na, eu, sea or sg, ea, sa

            Example:
                >player player1 na

        """

        # AUTO IS A SECRET VARIABLE THAT MAKES COMPUTER CHECK EVERY SERVER FOR PLAYER !!!WAIST OF API KEY!!!
        # FALSE = WILL ONLY CHECK GIVEN SERVER, TRUE = WILL CHECK ALL SERVERS UNTIL FINDING PLAYER

        # Checks if NOTHING was GIVEN
        if player_name == "" and server == "na" and auto == "False":

            # Get the AUTHORS ID
            discordID = raw.message.author.id

            # If author in VGQ then GET DATA
            data = config.playersVGQ.get(discordID, False)  # Get the AUTHORS VGQ INFO

            if data == False:
                await self.bot.say("You'll need to add yourself to the **VGQ** before using commands without arguments. :stuck_out_tounge:\nEnter the **help** command followed by **saveVG** to see more... :hugging:")
                return

            else:
                notice = "Looking for **" + str(data["IGN"]) + "** in the past **31** days in the **" + str(data["Region"]) + "** region... :eyes:"  # MESSAGE being SENT BEFOREHAND

                msg = await self.bot.say(notice)
                output = VG_module.getPlayerInfoVG(data["IGN"], data["Region"])

                if type(output) == str:
                    await self.bot.edit_message(msg, output)
                    return

                else:
                    await self.bot.edit_message(msg, embed=output)
                    return

        # FOR DEBUGGING
        # print("INPUT - PLAYER_NAME: " + str(player_name) + "   | SERVER: " + str(server) + "   | AUTO: " + str(auto))

        if checkName(player_name) == False:
            await self.bot.say("No valid player name was given... :sweat_smile:")
            return

        server = giveServer(server)

        auto = giveAuto(auto)

        # FOR DEBUGGING
        print("NAME: " + player_name + "   | SERVER: " + server + "   | AUTO: " + str(auto))

        notice = "Looking for **" + str(player_name) + "** in the past **31** days in the **" + str(server) + "** region... :eyes:"

        if auto == True:
            notice += "  -  **auto**"

        msg = await self.bot.say(notice)  # NOTICE USER that THEIR COMMAND is being PROCESSED
        output = VG_module.getPlayerInfoVG(player_name, server, auto)
        if type(output) == str:
            await self.bot.edit_message(msg, output)

        else:
            await self.bot.edit_message(msg, embed=output)  # RUNS ID TEST


    @commands.command(pass_context=True)
    async def latest(self, raw, player_name="", server="na", game_mode="any", auto="False"):
        """Fetched the latest Vainglory match. Works with VGQ.

                >latest (player_name) (server) (game_mode)
            player_name   ~   name of player to check for
            server        ~   the server to which the player belongs to    ~   default: na, options: na, eu, sea or sg, ea, sa
            game_mode     ~   game mode you would like performance check   ~   default: any, options: any, casual, ranked, royale, blitz

            Example:
                >latest player1 na casual

        """
        game_mode = game_mode.lower()

        # AUTO IS A SECRET VARIABLE THAT MAKES COMPUTER CHECK EVERY SERVER FOR PLAYER !!!WAIST OF API KEY!!!
        # FALSE = WILL ONLY CHECK GIVEN SERVER, TRUE = WILL CHECK ALL SERVERS UNTIL FINDING PLAYER

        # Checks if NOTHING was GIVEN
        if player_name == "" and server == "na" and game_mode == "any" and auto == "False":

            # Get the AUTHORS ID
            discordID = raw.message.author.id

            # If author in VGQ then GET DATA
            data = config.playersVGQ.get(discordID, False)  # Get the AUTHORS VGQ INFO

            if data == False:
                await self.bot.say("You'll need to add yourself to the **VGQ** before using commands without arguments. :stuck_out_tounge:\nEnter the **help** command followed by **saveVG** to see more... :hugging:")
                return

            else:
                notice = "Looking for **any** match from **" + data["IGN"] + "** from the past **31** days in the **" + data["Region"] + "** region... :eyes:"  # MESSAGE being SENT BEFOREHAND

                msg = await self.bot.say(notice)
                output = VG_module.getLatestMatchVG(data["IGN"], data["Region"], "")

                if type(output) == str:
                    await self.bot.edit_message(msg, output)
                    return

                else:
                    await self.bot.edit_message(msg, embed=output)
                    return

        # FOR DEBUGGING
        # print("INPUT - PLAYER_NAME: " + str(player_name) + "   | GAME_MODE: " + str(game_mode) + "   | SERVER: " + str(server) + "   | AUTO: " + str(auto))

        if checkName(player_name) == False:
            await self.bot.say("No valid player name was given... :sweat_smile:")
            return

        game_mode = giveGameMode(game_mode)

        server = giveServer(server)

        auto = giveAuto(auto)

        # FOR DEBUGGING
        print("NAME: " + player_name + "   | GAMEMODE: " + game_mode + "   | SERVER: " + server + "   | AUTO: " + str(auto))

        notice = "Looking for **" + str(game_mode) + "** match from **" + str(player_name) + "** from the past **31** days in the **" + str(server) + "** region... :eyes:"

        if auto == True:
            notice += "  -  **auto**"

        msg = await self.bot.say(notice)
        output = VG_module.getLatestMatchVG(player_name, server, game_mode, auto)
        if type(output) == str:
            await self.bot.edit_message(msg, output)
        else:
            await self.bot.edit_message(msg, embed=output)


    @commands.command(pass_context=True)
    async def saveVG(self, raw, player_name="", server="na"):
        """Save your Vainglory in-game name and region for quick looks ups.

                >saveVG (player_name) (server)
            player_name   ~   name of player to check for
            server        ~   the server to which the player belongs to    ~   default: na, options: na, eu, sea or sg, ea, sa

            Example:
                >saveVG player1 na
        """

        if checkName(player_name) == False:
            await self.bot.say("No valid player name was given... :sweat_smile:")
            return

        server = giveServer(server)

        author = raw.message.author
        discordID = raw.message.author.id

        # FOR DEBUGGING
        print("NAME: " + str(player_name) + "   | SERVER: " + str(server) + "   | Author: " + str(author) + "   | ID: " + str(discordID))

        # ADDS ID, NAME, IGN, REGION to PLAYERIGNVG
        config.playersVGQ[discordID] = {"Name": str(author), "IGN": str(player_name), "Region": server}

        await self.bot.say("Your In-game name, " + str(player_name) + ", and region, " + str(server) + ", has been saved to your account, " + str(author) + "... :hugging:")
        storePlayersVGQ()

    @commands.command(pass_context=True, hidden=True)
    async def VG(self, raw, data_type="player"):
        """Pull Vainglory data about yourself quick.

                >saveVG (quick_command)
            quick_command   ~   data type to pull   ~   default: player, options: player, stats, match

            Example:
                >VG stats
        """

        # Get the AUTHORS ID
        discordID = raw.message.author.id

        # If author in VGQ then GET DATA
        data = config.playersVGQ.get(discordID, False)  # Get the AUTHORS VGQ INFO

        if data == False:
            await self.bot.say("You need to add yourself to the **VGQ** first! :face_palm:\nEnter the help command followed by saveVG to see more... :stuck_out_tongue:")
            return

        if data_type == "player":
            notice = "Looking for **" + str(data["IGN"]) + "** in the past **31** days in the **" + str(data["Region"]) + "** region... :eyes:"  # MESSAGE being SENT BEFOREHAND

            msg = await self.bot.say(notice)
            output = VG_module.getPlayerInfoVG(data["IGN"], data["Region"])

            if type(output) == str:
                await self.bot.edit_message(msg, output)

            else:
                await self.bot.edit_message(msg, embed=output)

        elif data_type == "stats":
            notice = "Looking at stats of **any** matches for **" + data["IGN"] + "** from the past **31** days in the **" + data["Region"] + "** region... :eyes:"  # MESSAGE being SENT BEFOREHAND

            msg = await self.bot.say(notice)
            output = VG_module.getPlayerPerformanceVG(data["IGN"], data["Region"], "", 31)

            if type(output) == str:
                await self.bot.edit_message(msg, output)

            else:
                await self.bot.edit_message(msg, embed=output)

        elif data_type == "match":
            notice = "Looking for **any** match from **" + data["IGN"] + "** from the past **31** days in the **" + data["Region"] + "** region... :eyes:"  # MESSAGE being SENT BEFOREHAND

            msg = await self.bot.say(notice)
            output = VG_module.getLatestMatchVG(data["IGN"], data["Region"], "")

            if type(output) == str:
                await self.bot.edit_message(msg, output)

            else:
                await self.bot.edit_message(msg, embed=output)

        else:
            await self.bot.say("That isn't a quick command... :sweat_smile:")
            return

    # Make an EMBED of MATCHES to SORT THROUGH
    @commands.command(pass_context=True)
    async def matches(self, raw, player_name="", server="na", game_mode="any", page=1, pages=25):
        """Reaction menu for matches, for when you want review multiple matches at once. Works with VGQ.

                >matches (player_name) (server) (game_mode) (page) (pages)
            player_name   ~   name of player to check for
            server        ~   the server to which the player belongs to    ~   default: na, options: na, eu, sea or sg, ea, sa
            game_mode     ~   game mode you would like performance check   ~   default: any, options: any, casual, ranked, royale, blitz
            page          ~   page to start at                             ~   default: 1, options: maximum: 50, minimum: 1
            pages         ~   number of matches to load                    ~   default: 25, range: maximum: 50, minimum: 1

            Example:
                >matches player1 na casual 7 3

        """

        if player_name == "" and server == "na" and game_mode == "any" and page == 1 and pages == 25:

            # Get the AUTHORS ID
            discordID = raw.message.author.id

            # If author in VGQ then GET DATA
            data = config.playersVGQ.get(discordID, False)  # Get the AUTHORS VGQ INFO

            if data == False:
                await self.bot.say("You'll need to add yourself to the **VGQ** before using commands without arguments. :stuck_out_tounge:\nEnter the **help** command followed by **saveVG** to see more... :hugging:")
                return

            else:

                # FETCH PLAYER VGQ INFO
                player_name = data["IGN"]
                server = data["Region"]

        # Checks that NAME given is VALID
        if checkName(player_name) == False:
            await self.bot.say("No valid player name was given... :sweat_smile:")
            return

        # VALIDATES INPUT
        server = giveServer(server)
        game_mode = giveGameMode(game_mode)
        page = givePages(page, 1)
        pages = givePages(pages)

        # NOTICE to be SENT
        notice = "Looking for **" + str(game_mode) + "** matches of **" + str(player_name) + "** from the past **31** days in the **" + str(server) + "** region... :eyes:"

        # Sends NOTICE to CLIENT
        msg = await self.bot.say(notice)

        try:
            # Await self.bot.edit_message(msg, embed=VG_module.getEmbedMatchesVG(player_name, server, game_mode, days, pages))
            # Get MATCHES GIVEN INPUT
            matches = VG_module.getMatchesVG(pages, player_name, server, game_mode, 31)

            if matches == False:
                await self.bot.edit_message(msg, "Couldn't get **" + str(game_mode) + "** matches for **" + str(player_name) + "** in the **" + str(server) + "** region from the past **31**... :sweat_smile:")
                return

        except:
            await self.bot.edit_message(msg, "Couldn't get **" + str(game_mode) + "** matches for **" + str(player_name) + "** in the **" + str(server) +"** region from the past **31**... :sweat_smile:")
            return

        print("Player:   " + str(player_name) + "   |Match: " + str(matches[page]) + "   |GameMode: " + str(game_mode) + "   |Page: " + str(page) + "   |Pages: " + str(pages))

        # FETCH the EMBED
        embed = VG_module.getEmbedMatchesVG(player_name, matches[page], game_mode, page, pages)

        try:
            await self.bot.edit_message(msg, embed=embed)

            # SETUP REACTIONS
            # Get emojis from http://www.fileformat.info/info/unicode/char/27a1/browsertest.html or by messaging R. Danny in discordpy server
            await self.bot.add_reaction(msg, '\U00002b05')
            await self.bot.add_reaction(msg, '\U000027a1')

        except:
            await self.bot.edit_message(msg, "Couldn't set up your matches... :pensive:")

        # STORE MESSAGE DATA
        msgs[msg.id] = {"IGN": player_name, 'Matches': matches, "Game_Mode": game_mode, 'Page': page, 'Pages': pages}

        # WAIT TEN MINUTES then TRY to DELETING the MSG
        await asyncio.sleep(600)
        try:
            del msgs[msg.id]
            pass

        except:
            pass

    # RUNS whenever a REACTION is ADDED
    async def on_reaction_add(self, reaction, user):
        msg = reaction.message

        if msg.id in msgs.keys() and reaction.emoji == '➡' and msgs[msg.id]["Page"] <= msgs[msg.id]["Pages"]:
            # SET PAGE to CORRECT VALUE
            msgs[msg.id]["Page"] += 1
            # print(str(msgs[msg.id]["Page"]) + "   |   POSITION")

            # EDIT the MSG CORRESPONDING to the REACTION
            await self.bot.edit_message(reaction.message, embed=VG_module.getEmbedMatchesVG(str(msgs[msg.id]["IGN"]), msgs[msg.id]["Matches"][msgs[msg.id]["Page"]], str(msgs[msg.id]["Game_Mode"]), int(msgs[msg.id]["Page"] + 1), int(msgs[msg.id]["Pages"])))

        elif msg.id in msgs.keys() and reaction.emoji == '⬅' and msgs[msg.id]["Page"] > 0:
            # SET PAGE to CORRECT VALUE
            msgs[msg.id]["Page"] -= 1
            # print(str(msgs[msg.id]["Page"]) + "   |   POSITION")

            # EDIT the MSG CORRESPONDING to the REACTION
            await self.bot.edit_message(reaction.message, embed=VG_module.getEmbedMatchesVG(str(msgs[msg.id]["IGN"]), msgs[msg.id]["Matches"][msgs[msg.id]["Page"]], str(msgs[msg.id]["Game_Mode"]), int(msgs[msg.id]["Page"] + 1), int(msgs[msg.id]["Pages"])))

    # RUNS whenever a REACTION is REMOVED
    async def on_reaction_remove(self, reaction, user):
        msg = reaction.message

        if msg.id in msgs.keys() and reaction.emoji == '➡' and msgs[msg.id]["Page"] <= msgs[msg.id]["Pages"]:
            # SET PAGE to CORRECT VALUE
            msgs[msg.id]["Page"] += 1
            # print(str(msgs[msg.id]["Page"]) + "   |   POSITION")

            # EDIT the MSG CORRESPONDING to the REACTION
            await self.bot.edit_message(reaction.message, embed=VG_module.getEmbedMatchesVG(str(msgs[msg.id]["IGN"]), msgs[msg.id]["Matches"][msgs[msg.id]["Page"]], str(msgs[msg.id]["Game_Mode"]), int(msgs[msg.id]["Page"] + 1), int(msgs[msg.id]["Pages"])))

        elif msg.id in msgs.keys() and reaction.emoji == '⬅' and msgs[msg.id]["Page"] > 0:
            # SET PAGE to CORRECT VALUE
            msgs[msg.id]["Page"] -= 1
            # print(str(msgs[msg.id]["Page"]) + "   |   POSITION")

            # EDIT the MSG CORRESPONDING to the REACTION
            await self.bot.edit_message(reaction.message, embed=VG_module.getEmbedMatchesVG(str(msgs[msg.id]["IGN"]), msgs[msg.id]["Matches"][msgs[msg.id]["Page"]], str(msgs[msg.id]["Game_Mode"]), int(msgs[msg.id]["Page"] + 1), int(msgs[msg.id]["Pages"])))

def setup(bot):
    bot.add_cog(Vg(bot))
