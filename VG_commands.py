
# VG Commands:
# File containing all of VG commands for Discord
"""
List of Commands:
player
stats
match
"""

# IMPORTS
import gamelocker, discord
from discord.ext import commands
import TOOL_module as tools
import VG_module
import VG_toolbox
import config
import pickle
from VG_module import getMatches, apiVG
import dateutil.parser,asyncio

# DISCORD EMBED VARIABLES--
botImageDISCORD = "http://i63.tinypic.com/9k6xcj.jpg"  # URL of BOTS IMAGE
signatureDISCORD = "Big Thanks to SEMC and MadGlory! Made with love."  # String used in FOOTER as MESSAGE
msgs = dict()

# Stores PLAYERVGQ DICT
def storePlayersVGQ():
    with open("playersVGQ.pickle", "wb") as handle:
        pickle.dump(config.playersVGQ, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
def storeTrophies():
    with open("playersTrophies.pickle", "wb") as handle:
        pickle.dump(config.playersTrophies, handle, protocol=pickle.HIGHEST_PROTOCOL)
                


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
        game_mode = "any"

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


# CLASS containing ALL COMMANDS for THIS MODULE
class Vg():
    """All the commands in relation to Vainglory.
            Made with love and some Vainglory api, python - gamelocker.
    """

    def __init__(self, bot):
        self.bot = bot

    async def on_reaction_add(self, reaction,user):
        if reaction.message.id in msgs.keys() and reaction.emoji == '➡' and msgs[reaction.message.id]['page'] < msgs[reaction.message.id]['num']:
            msg = reaction.message
            msgs[msg.id]['page'] += 1
            page = msgs[msg.id]['page']
            await self.bot.edit_message(reaction.message,new_content='Embed: ', embed=getMatches(msgs[msg.id]['ign'], msgs[msg.id]['m'][page-1], msgs[msg.id]['region'],page,msgs[msg.id]['num']))
        elif reaction.message.id in msgs.keys() and reaction.emoji == '⬅' and msgs[reaction.message.id]['page'] > 1:
            msg = reaction.message
            msgs[msg.id]['page'] -= 1
            page = msgs[msg.id]['page']
            await self.bot.edit_message(reaction.message,new_content='Embed: ', embed=getMatches(msgs[msg.id]['ign'], msgs[msg.id]['m'][page-1], msgs[msg.id]['region'],page,msgs[msg.id]['num']))

    async def on_reaction_remove(self, reaction,user):
        if reaction.message.id in msgs.keys() and reaction.emoji == '➡' and msgs[reaction.message.id]['page'] < msgs[reaction.message.id]['num']:
            msg = reaction.message
            msgs[msg.id]['page'] += 1
            page = msgs[msg.id]['page']
            await self.bot.edit_message(reaction.message,new_content='Embed: ', embed=getMatches(msgs[msg.id]['ign'], msgs[msg.id]['m'][page-1], msgs[msg.id]['region'],page,msgs[msg.id]['num']))
        elif reaction.message.id in msgs.keys() and reaction.emoji == '⬅' and msgs[reaction.message.id]['page'] > 1:
            msg = reaction.message
            msgs[msg.id]['page'] -= 1
            page = msgs[msg.id]['page']
            await self.bot.edit_message(reaction.message,new_content='Embed: ', embed=getMatches(msgs[msg.id]['ign'], msgs[msg.id]['m'][page-1], msgs[msg.id]['region'],page,msgs[msg.id]['num']))

    @commands.command(pass_context=True)
    async def stats(self, raw, player_name="", server="na", game_mode="any", days="31", auto="False"):
        """Gets a players performance in the past days.
                >stats (player_name) (server) (game_mode) (days)
            player_name   ~   name of player to search for
            server        ~   the server to which the player belongs to    ~   default: na, options: na, eu, sea or sg, ea, sa
            game_mode     ~   game mode you would like performance check   ~   default: any, options: any, casual, ranked, royale, blitz
            days          ~   day range to search from                     ~   default: 31, requirements: maximum: 93, minimum: 1
            example:
                >stats player1 na casual 7
        """

        # AUTO IS A SECRET VARIABLE THAT MAKES COMPUTER CHECK EVERY SERVER FOR PLAYER !!!WASTE OF API KEY!!!
        # FALSE = WILL ONLY CHECK GIVEN SERVER, TRUE = WILL CHECK ALL SERVERS UNTIL FINDING PLAYER

        # Checks if NOTHING was GIVEN
        if player_name == "" and server == "na" and game_mode == "any" and days == "31" and auto == "False":

            discordID = raw.message.author.id

            # If author in VGQ then GET DATA
            data = config.playersVGQ.get(discordID, False)  # Get the PREFIX for SERVER

            if data == False:
                await self.bot.say("You need to add yourself to the **VGQ** first! :face_palm:\nEnter the help command followed by saveVG to see more... :stuck_out_tongue:")
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
        print("INPUT - PLAYER_NAME: " + str(player_name) + "   | GAME_MODE: " + str(game_mode) + "   | SERVER: " + str(server) + "   | DAYS: " + str(days) + "   | AUTO: " + str(auto))

        if checkName(player_name) == False:
            await self.bot.say("No valid player name was given... :sweat_smile:")
            return

        game_mode = giveGameMode(game_mode)

        server = giveServer(server)

        days = giveDays(days)

        auto = giveAuto(auto)

        # FOR DEBUGGING
        print("NAME: " + player_name + "   | GAMEMODE: " + game_mode + "   | SERVER: " + server + "   | DAYS: " + str(days) + "   | AUTO: " + str(auto))

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
        """Checks if player exist in vainglory.
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

            discordID = raw.message.author.id

            # If author in VGQ then GET DATA
            discordID = raw.message.author.id

            data = config.playersVGQ.get(discordID, False)  # Get the PREFIX for SERVER

            if data == False:
                await self.bot.say("You need to add yourself to the **VGQ** first! :face_palm:\nEnter the help command followed by saveVG to see more... :stuck_out_tongue:")
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
        #print("INPUT - PLAYER_NAME: " + str(player_name) + "   | SERVER: " + str(server) + "   | AUTO: " + str(auto))

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
        """Fetched the latest Vainglory match.
                >player (player_name) (server) (game_mode)
            player_name   ~   name of player to check for
            server        ~   the server to which the player belongs to    ~   default: na, options: na, eu, sea or sg, ea, sa
            game_mode     ~   game mode you would like performance check   ~   default: any, options: any, casual, ranked, royale, blitz
            Example:
                >match player1 na casual
        """
        game_mode = game_mode.lower()

        # AUTO IS A SECRET VARIABLE THAT MAKES COMPUTER CHECK EVERY SERVER FOR PLAYER !!!WAIST OF API KEY!!!
        # FALSE = WILL ONLY CHECK GIVEN SERVER, TRUE = WILL CHECK ALL SERVERS UNTIL FINDING PLAYER

        # Checks if NOTHING was GIVEN
        if player_name == "" and server == "na" and game_mode == "any" and auto == "False":

            discordID = raw.message.author.id

            # If author in VGQ then GET DATA
            data = config.playersVGQ.get(discordID, False)  # Get the PREFIX for SERVER

            if data == False:
                await self.bot.say("You need to add yourself to the **VGQ** first! :face_palm:\nEnter the help command followed by saveVG to see more... :stuck_out_tongue:")
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
        print("INPUT - PLAYER_NAME: " + str(player_name) + "   | GAME_MODE: " + str(game_mode) + "   | SERVER: " + str(server) + "   | AUTO: " + str(auto))

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

        discordID = raw.message.author.id

        data = config.playersVGQ.get(discordID, False)  # Get the PREFIX for SERVER

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

    @commands.command(pass_context=True)
    async def matches(self,ctx, ign="", region = 'na',page=1 ,gamemode=''):
        """
        Reaction menu for all your matches! Works with VGQ.
        $matches <ign> <region> <page> <gamemode>
        E.X: $matches SpiesWithin na
        """
        if ign == "" and region == "na" and page == 1 and gamemode == "":
            discordID = ctx.message.author.id
            # If author in VGQ then GET DATA
            data = config.playersVGQ.get(discordID, False)  # Get the PREFIX for SERVER
            if data == False:
                await self.bot.say("You need to add yourself to the **VGQ** first! :face_palm:\nEnter the help command followed by saveVG to see more... :stuck_out_tongue:")
                return
            else:
                ign = data["IGN"]
                region = data['Region']
        gamemode = gamemode.lower()
        gamemode = VG_module.reverse_match.get(gamemode, '')
        region = region.lower()
        msg = await self.bot.say("Fetching data for {}.".format(ign))
        try:
            m = apiVG.matches({"page[limit]": 50, "filter[playerNames]": ign, "filter[createdAt-start]": "2017-01-01T08:25:30Z", "sort": "-createdAt", "filter[gameMode]": gamemode}, region = region)
        except:
            await self.bot.say("Error! Please check everything and use $help matches for more info. Remember it **is** caps sensitive.")
            return
        m = sorted(m, key=lambda d: d.createdAt, reverse=True)
        num = len(m)
        try:
            msg = await self.bot.edit_message(msg, new_content= 'Embed:', embed = getMatches(ign, m[page-1], region,page,num))
        except:
            await self.bot.edit_message(msg, new_content="Sorry, couldn't find data for {} in {}. Check your region and or spelling. It **IS** caps sensitive.".format(ign, region))
        await self.bot.add_reaction(msg, '\U00002b05')
        await self.bot.add_reaction(msg, '\U000027a1')
        #Get emojis from http://www.fileformat.info/info/unicode/char/27a1/browsertest.htm
        #or by messaging R. Danny in discordpy server
        msgs[msg.id] = {"ign": ign, 'm': m, 'page': page-1,'region':region,'num':num}
        await asyncio.sleep(300)
        try:
            del msgs[msg.id]
            pass
        except:
            pass

    @commands.command(pass_context=True aliases=['taunt','charm'])
    async def charms(hero):
        """
        Unleash Your Inner Troll
        $taunt list
        """
        url = VG_toolbox.giveTaunt(hero)
        if url == False:
            await self.bot.say("Sorry. Hero taunt not found.")
        elif 'http' not in url:
            await self.bot.say(url)
        else:
            em = discord.Embed()  
            em.set_image(url=url)
            await self.bot.say(embed = em)
    
    @commands.command(pass_context=True)
    async def claim(name="", server="na"):
        """
        Update your trophy case!
        """
        if player_name == "" and server == "na" and auto == "False":

            discordID = raw.message.author.id

            # If author in VGQ then GET DATA
            discordID = raw.message.author.id

            data = config.playersVGQ.get(discordID, False)  # Get the PREFIX for SERVER

            if data == False:
                await self.bot.say("You need to add yourself to the **VGQ** first! :face_palm:\nEnter the help command followed by saveVG to see more... :stuck_out_tongue:")
                return
    
            else:
                name = data["IGN"]
                server = data['Region']
        

        else:
                if checkName(name) == False:
                    await self.bot.say("No valid player name was given... :sweat_smile:")
                    return
                notice = "Looking for **" + str(name) + "** in the past **31** days in the **" + str(server) + "** region... :eyes:"  # MESSAGE being SENT BEFOREHAND        
                server = giveServer(server)

        msg = await self.bot.say(notice)
            
        """
        Change output here!!!!!!!!!!!!
        """
        config.playersTrophies.setdefault(name), default=[])
        earned = config.playersTrophies[name]
        
        earned, new = VG_module.getTrophies(name, server, earned)
        
        storeTrophies()
        
        if new == {"Hero" :{}, "Item":{}, "Match Goals":{}}:
            output = "No new trophies earned..."
        else:
            output = discord.Embed(title = "New Trophies Earned!")
            for cat in new:
                if new[cat] != {}:
                    for trophy in new[cat]:
                        em.add_field(name = new[cat][trophy]["name"], value = new[cat][trophy]["description"])
        
        if type(output) == str:
            await self.bot.edit_message(msg, output)
            return
    
        else:
            await self.bot.edit_message(msg, embed=output)
            return
            
    @commands.command(pass_context=True)
    async def trophies(name="", server="na"):
        """
       Show off your trophy case!
        """
        if player_name == "" and server == "na" and auto == "False":

            discordID = raw.message.author.id

            # If author in VGQ then GET DATA
            discordID = raw.message.author.id

            data = config.playersVGQ.get(discordID, False)  # Get the PREFIX for SERVER

            if data == False:
                await self.bot.say("You need to add yourself to the **VGQ** first! :face_palm:\nEnter the help command followed by saveVG to see more... :stuck_out_tongue:")
                return
    
            else:
                name = data["IGN"]
                server = data['Region']
        

        else:
                if checkName(name) == False:
                    await self.bot.say("No valid player name was given... :sweat_smile:")
                    return
                notice = "Looking for **" + str(name) + "**'s trophies :eyes:"  
                server = giveServer(server)

        msg = await self.bot.say(notice)
            
        trophy_case = config.playersTrophies[name]
        for cat in trophy_case:
            output = discord.Embed(title = cat + " Trophies:")
            for trophy in cat:
                em.add_field(name = trophy_case[cat][trophy]["name"], value = trophy_case[cat][trophy]["description"])
            await self.bot.say(output)
        
def setup(bot):
    bot.add_cog(Vg(bot))
