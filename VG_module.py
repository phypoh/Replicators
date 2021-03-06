# VG Module:
# Functions using the Vainglory API
"""
List of Functions:
    getPlayerInfoVG
    getPlayerPerformanceVG
    getLatestMatchVG
"""

import gamelocker
from gamelocker.strings import pretty
import datetime
import discord
import TOOL_module as tools
import dateutil.parser
import VG_toolbox
from VG_toolbox import giveMatchVG
import telemetry_wrapper


# VG Variables--
keyVG = ""
apiVG = gamelocker.Gamelocker(keyVG).Vainglory()  # API OBJECT

# DISCORD EMBED VARIABLES--
botImageDISCORD = "http://i63.tinypic.com/9k6xcj.jpg"  # URL of BOTS IMAGE
signatureDISCORD = "Thanks to SEMC and MadGlory made with love ~ xoxo"  # String used in FOOTER as MESSAGE


heroes = {
        "*Adagio*": "Adagio",
        "*Alpha*": "Alpha",
        "*Ardan*": "Ardan",
        "*Baron*": "Baron",
        "*Blackfeather*": "Blackfeather",
        "*Catherine*": "Catherine",
        "*Celeste*": "Celeste",
        "*Flicker*": "Flicker",
        "*Fortress*": "Fortress",
        "*Glaive*": "Glaive",
        "*Gwen*": "Gwen",
        "*Hero009*": "Krul",
        "*Hero010*": "Skaarf",
        "*Hero016*": "Rona",
        "*Idris*": "Idris",
        "*Joule*": "Joule",
        "*Kestrel*": "Kestrel",
        "*Koshka*": "Koshka",
        "*Lance*": "Lance",
        "*Lyra*": "Lyra",
        "*Ozo*": "Ozo",
        "*Petal*": "Petal",
        "*Phinn*": "Phinn",
        "*Reim*": "Reim",
        "*Ringo*": "Ringo",
        "*Samuel*": "Samuel",
        "*SAW*": "SAW",
        "*Sayoc*": "Taka",
        "*Skye*": "Skye",
        "*Vox*": "Vox"
    }
    
match_dict = {
"blitz_pvp_ranked": "Blitz",
"casual_aral": "Battle Royale",
"private": "Private Casual",
"private_party_draft_match": "Private Draft",
"private_party_blitz_match": "Private Blitz",
"private_party_aral_match":"Private Battle Royale",
"casual": "Casual Match",
"ranked": "Rank Match"
}

reverse_match = {
"casual": "casual",
"blitz": "blitz_pvp_ranked",
"royale": "casual_aral",
"rank": "ranked",
"rank": "ranked",
"ranked": "ranked",
"br": "casual_aral",
"battle": "casual_aral"
}

# GETS MATCH OBJECTS and RETURNS INFO
def getMatchesVG(amount=50, name="", server="na", game_mode="any", days=31, auto=False):
    amount = int(amount)         # Convert AMOUNT to a STRING to prevent ERRORS
    name = str(name)             # Convert ID to a STRING to prevent ERRORS
    server = str(server)         # Convert SERVER to STRING to prevent ERRORS
    game_mode = str(game_mode)   # Convert MODE to STRING to prevent ERRORS
    days = int(days)             # Convert DAYS to STRING to prevent ERRORS
    auto = bool(auto)            # Convert AUTO to BOOLEAN to prevent errors

    # FOR DEBUGGING
    # print("Amount: " + str(amount) + "  |Name: " + name + "  |Server: " + server + "  |Game Mode: " + game_mode + "  |Days: " + str(days) + "  |Auto: " + str(auto))

    # DATE RANGE when FETCHING from MATCHES!!! example: {"filter[createdAt-start]": daterange, "filter[createdAt-end]": datenow, etc...}
    datenow = datetime.date.today()
    daterange = str(datenow - datetime.timedelta(days=days)) + "T00:00:00Z"  # Get the DATE RANGE to SEARCH from
    # datenow = str(datetime.date.today()) + "T00:00:00Z"  # CURRENT DATE

    # BUILD FILTER used to GET MATCHES
    filterVG = {'filter[createdAt-start]': daterange, 'page[limit]': amount, 'filter[playerNames]': name, "sort": "-createdAt"}

    if game_mode == "any" or game_mode == "":
        pass

    else:
        filterVG["filter[gameMode]"] = giveMatchVG(game_mode, 1)

    # FOR DEBUGGING
    # print(str(filterVG) + "   |   FILTER USED")

    # If AUTO is TRUE then SEARCH in every SERVER until you FIND
    if auto == True:

        # SERVERS to SEARCH THROUGH
        servers = [
            "na",
            "eu",
            "sg",
            "ea",
            "sa",
            "tournament-na",
            "tournament-eu"
            ]

        for serverName in servers:
            try:
                matches = apiVG.matches(filterVG, serverName)
                break  # BREAK loop once a MATCH was FOUND

            except:
                matches = False

        if matches == False:
            return False

    elif auto == False:
        try:  # GIVEN the SERVER try to FIND MATCHES for PLAYER
            matches = apiVG.matches(filterVG, server)

        except:
            return False

    else:
        print("!!!HUGE ERROR WHILE TRYING TO GET MATCHES!!!")
        return "!!!HUGE ERROR WHILE TRYING TO GET MATCHES!!!"
    matches = sorted(matches, key=lambda d: d.createdAt, reverse =True)
    return matches


# GETS a PLAYERS life time INFORMATION
def getPlayerInfoVG(name, server="", auto=False):
    name = str(name)             # Convert ID to a STRING to prevent ERRORS
    server = str(server)         # Convert SERVER to STRING to prevent ERRORS
    auto = bool(auto)            # Convert AUTO to BOOLEAN to prevent errors

    matches = getMatchesVG(1, name, server, auto=auto)

    # If NO MATCHES were RETURNED
    if matches == False:
        return "Couldn't find anything on **" + str(name) + "** in the past **31** days in **" + str(server) + "** server!"

    # MATCH VARIABLES USED
    # IGN, level, lifetimeGold, lossStreak, played, winStreak, wins, xp,
    # skillTier, thumbnail, karmaLevel, latestmatch, gamemode, skillTier, KarmaLevel

    for match in matches:  # From that MATCH get the VAINGLORY PLAYER ID
        latestmatchraw = dateutil.parser.parse(match.createdAt)
        latestmatch = latestmatchraw.strftime('%d/%m/%Y %H:%M:%S') + " GMT"
        gameMode = str(match.gameMode)

        for roaster in match.rosters:
            for participant in roaster.participants:
                if participant.player.name == name:
                    matchstats = participant.stats
                    playerstats = participant.player.stats

                    IGN = str(participant.player.id)
                    level = str(matchstats["level"])
                    lifetimeGold = str(playerstats["lifetimeGold"])
                    lossStreak = str(playerstats["lossStreak"])
                    played = str(playerstats["played"])
                    winStreak = str(playerstats["winStreak"])
                    wins = str(playerstats["wins"])
                    xp = str(playerstats["xp"])

                    skillTier = str(matchstats["skillTier"])
                    thumbnail = VG_toolbox.giveSkillTierVG(skillTier, 1)
                    karmaLevel = str(matchstats["karmaLevel"])

    # CREATES the STRING for ID
    idString = "\n**ID:** *" + str(IGN) + "*"

    # CREATES the STRING for LIFETIMEGOLD
    lifetimeGoldString = "\n**Life Time Gold:** *" + str(lifetimeGold) + "*"

    # CREATES the STRING for LOSSSTREAK
    lossStreakString = "\n**Loss Streak:** *" + str(lossStreak) + "*"

    # CREATES the STRING for PLAYED
    playedString = "\n**Played:** *" + str(played) + "*"

    # CREATES the STRING for WINSTREAK
    winStreakString = "\n**Wins Streak:** *" + str(winStreak) + "*"

    # CREATES the STRING for WINS
    winsString = "\n**Wins:** *" + str(wins) + "*"

    # CREATES the STRING for XP
    xpString = "\n**Xp:** *" + str(xp) + "*"

    # CREATES the STRING for LOSE
    loseString = "\n**Lost:** *" + str(int(played) - int(wins)) + "*"

    # FORMAT USED TO CREATE STRINGS ~
    # CREATES the STRING for
    # String = "\n**:** *" +  + "*"

    # EMBED CREATION****************************************************************************************************
    # Create the TITLE for EMBED
    title = "Vainglory Career for " + str(name)

    # Create the DESCRIPTION for the EMBED
    description = "**Player:** *" + str(name) + "* **| Lv:** *" + str(level) + "* **| ST:** *" + str(VG_toolbox.giveSkillTierVG(skillTier)) + "* **| K:** *" + str(VG_toolbox.giveKarmaVG(karmaLevel)) + "*\n**Last Game Registered:** *" + str(latestmatch) + "* **| Game Type:** *" + str(VG_toolbox.giveMatchVG(gameMode)) + "*"

    # ASSEMBLE the STATS TOGETHER for EMBED
    staticsOne = str(lifetimeGoldString) + str(winStreakString) + str(lossStreakString) + str(playedString) + str(winsString) + str(loseString) + str(xpString)

    # CREATE the EMBED
    embed = discord.Embed(title=title, colour=discord.Colour(0x4e9ff9), description=description,
                          timestamp=datetime.datetime.now())

    # Set the HEADER
    embed.set_author(name="Halcyon Hackers", url="https://github.com/ClarkThyLord/Computer-BOT", icon_url="http://i67.tinypic.com/25738l1.jpg")

    # Set the THUMBNAIL to MOST USED HERO
    try:
        embed.set_thumbnail(url=thumbnail)
    except:  # If THUMBNAIL couldn't be REACHED then MAKE THUMBNAIL the Vainglory logo
        embed.set_thumbnail(url="http://i63.tinypic.com/9k6xcj.jpg")

    # ADD PART ONE of STATICS to EMBED
    embed.add_field(name="Career:", value=staticsOne)

    # ADD FOOTER of STATICS to EMBED
    embed.set_footer(text=signatureDISCORD, icon_url=botImageDISCORD)

    # SEND the EMBED
    return embed

    # if mode == "" or mode == "user":  # If MODE is DEFAULT or USER SEND regular MESSAGE
    #     return "The player **" + name + "** was found in the Vainglory servers in the past 31 days!"
    # if mode == "dev":  # If MODE is DEV send ID with MESSAGE
    #     return "The player **" + name + "** was found in the Vainglory servers in the past 31 days! ID: " + id



# Get a PLAYERS performance from RANGE of DAYS with the players NAME
def getPlayerPerformanceVG(name, server="", game_mode="", days=7, auto=False):
    name = str(name)             # Convert ID to a STRING to prevent ERRORS
    server = str(server)         # Convert SERVER to STRING to prevent ERRORS
    game_mode = str(game_mode)   # Convert MODE to STRING to prevent ERRORS
    days = int(days)             # Convert DAYS to STRING to prevent ERRORS
    auto = bool(auto)            # Convert AUTO to BOOLEAN to prevent errors

    matches = getMatchesVG(50, name, server, game_mode, days, auto)

    # If NO MATCHES were RETURNED
    if matches == False:
        msg = "Couldn't find"

        if game_mode != "":
            msg += " any **" + str(game_mode) + "** matches"

        else:
            msg += " anything"

        msg += " of **" + str(name) + "** in the past **" + str(days) + "** days in **" + str(
            server) + "** server!"

        return msg

    # MATCH VARIABLES
    latestmatch = ""
    gameMode = []
    duration = []

    # Get DATA out of the MATCH OBJECTS
    playerdata = []
    matchNum = 0
    size = len(matches) - 1
    number  = 0
    for match in matches:
        if number == 0:  # If MATCH is the FIRST MATCH then GET DATA
            latestmatchraw = dateutil.parser.parse(match.createdAt)
            latestmatch = latestmatchraw.strftime('%d/%m/%Y %H:%M:%S') + " GMT"

        gameMode.append(str(match.gameMode))
        duration.append(match.duration)
        number += 1

        for roaster in match.rosters:
            for participant in roaster.participants:
                if participant.player.name == name:
                    playerdata.append(participant.to_dict())  # If DATA belongs to PLAYER then KEEP
        number += 1
    # FOR DEBUGGING
    # print(str(latestmatch) + " | latestmatch")
    # print(str(gameMode) + " | gameMode")

    # DATA VARIABLES
    size = str(len(playerdata))  # Get the SIZE of the PLAYERSDATA

    # PROFILE VARIABLES ~ most of this will be USED for MEAN and MODE
    actor = []
    assists = []
    crystalMineCaptures = []
    deaths = []
    farm = []
    goldMineCaptures = []
    itemslist = []
    karmaLevel = ""
    kills = []
    krakenCaptures = []
    level = ""
    minionKills = []
    skillTier = ""
    skinKey = []
    turretCaptures = []
    wentAfk = []
    winner = []
    number = 0
    # Go though PLAYERDATA getting DATA needed for building a PROFILE
    for data in playerdata:
        attributes = data["attributes"]
        stats = attributes["stats"]

        actor.append(pretty(attributes["actor"]).replace("*", ""))
        assists.append(stats["assists"])
        crystalMineCaptures.append(stats["crystalMineCaptures"])
        deaths.append(stats["deaths"])
        farm.append(stats["farm"])
        goldMineCaptures.append(stats["goldMineCaptures"])

        for item in stats["items"]:  # LOOPS the ITEMS for EACH MATCH ADDING it to the ITEMSLIST
            itemslist.append(pretty(item))

        kills.append(stats["kills"])
        krakenCaptures.append(stats["krakenCaptures"])
        minionKills.append(stats["minionKills"])
        skinKey.append(pretty(stats["skinKey"]))
        turretCaptures.append(stats["turretCaptures"])
        wentAfk.append(stats["wentAfk"])
        winner.append(stats["winner"])
        if number == 0:
            level = stats["level"]
            karmaLevel = stats["karmaLevel"]
            skillTier = stats["skillTier"]
        number += 1

    # FOR DEBUGGING
    # print(str(actor) + " | actors")
    # print(str(assists) + " | assists")
    # print(str(crystalMineCaptures) + " | crystalMineCaptures")
    # print(str(deaths) + " | deaths")
    # print(str(farm) + " | farm")
    # print(str(goldMineCaptures) + " | goldMineCaptures")
    # print(str(itemslist) + " | itemslist")
    # print(str(karmaLevel) + " | karmaLevel")
    # print(str(kills) + " | kills")
    # print(str(krakenCaptures) + " | krakenCaptures")
    # print(str(level) + " | level")
    # print(str(minionKills) + " | minionKills")
    # print(str(skillTier) + " | skillTier")
    # print(str(skinKey) + " | skinKey")
    # print(str(turretCaptures) + " | turretCaptures")
    # print(str(wentAfk) + " | wentAfk")
    # print(tools.giveMeanOfList(wentAfk))
    # print(str(winner) + " | winner")
    # print(tools.giveMeanOfList(winner))

    # CREATING a list(STRING) of the TOP GAMEMODES in the past X days
    gamemodes = tools.giveListInOrderTOOL(gameMode)
    if len(gamemodes) <= 0:  # If NO GAMEMODES were FOUND then NOTICE USER about it
        gamemodelistString = "\n**We couldn't get any game modes from your matches!**"

    elif game_mode != "":
        gamemodelistString = "\n**This is performance from " + str(game_mode) + " games only...**"

    else:
        gamemodelistString = "\n**Game Modes Played Most:**"  # SET TITLE to INFO

        num = 0
        if len(gamemodes) < 3:  # If LESS then FIVE GAMEMODES were FOUND then set NUM to the GAMEMODES LIST LENGTH
            max = len(gamemodes) - 1

        elif len(gamemodes) >= 3:  # If FIVE or MORE GAMEMODES were FOUND then SET NUM to FIVE
            max = 3

        while num < max:  # NAME POSITIONS of most USED GAMEMODES
            gamemodelistString += "\n**" + str(num + 1) + "** ~ *"

            gamemodelistString += str(VG_toolbox.giveMatchVG(gamemodes[num])) + "*"

            num += 1

    # CREATING a list(STRING) of the TOP ACTORS used in the past X days
    actors = tools.giveListInOrderTOOL(actor)
    if len(actors) <= 0:  # If NO ACTORS were FOUND then NOTICE USER about it
        actorslistString = "\n**We couldn't get any heroes from your matches!**"

    else:
        actorslistString = "\n**Heroes Used Most:**"  # SET TITLE to INFO

        num = 0
        if len(actors) < 3:  # If LESS then FIVE ACTORS were FOUND then set NUM to the ACTORS LIST LENGTH
            max = len(actors) - 1

        elif len(actors) >= 3:  # If FIVE or MORE ACTORS were FOUND then SET NUM to FIVE
            max = 3

        while num < max:  # NAME POSITIONS of most USED ACTORS
            actorslistString += "\n**" + str(num + 1) + "** ~ *" + str(actors[num]) + "*"

            if num == 0:  # GETS the THUMBNAIL for MOST USED HERO
                thumbnail = "http://www.vaingloryfire.com/images/wikibase/icon/heroes/" + str(actors[num]) + ".png"

            num += 1

    # CREATING a list(STRING) of the TOP SKINS used in the past X days
    # skins = tools.giveListInOrderTOOL(skinKey)
    # if len(skins) <= 0:  # If NO SKINS were FOUND then NOTICE USER about it
    #     skinslistString = "\n**We couldn't get any skins from your matches!**"
    #
    # else:
    #     skinslistString = "\n**Skins Used Most:**"  # SET TITLE to INFO
    #
    #     num = 0
    #     if len(skins) < 3:  # If LESS then FIVE SKINS were FOUND then set NUM to the ACTORS LIST LENGTH
    #         max = len(skins) - 1
    #
    #     elif len(skins) >= 3:  # If FIVE or MORE SKINS were FOUND then SET NUM to FIVE
    #         max = 3
    #
    #     while num < max:  # NAME POSITIONS of most USED SKINS
    #         skinslistString += "\n**" + str(num + 1) + "** ~ *" + str(skins[num]) + "*"
    #         num += 1
    #
    # CREATING a list(STRING) of the TOP ITEMS used in the past X days to MSG
    # items = tools.giveListInOrderTOOL(itemslist)
    # if len(items) <= 0:  # If NO ITEMS were FOUND then NOTICE USER about it
    #     itemlistString = "\n**We couldn't get any items from your matches!**"
    #
    # else:
    #     itemlistString = "\n**Items Used Most:**"  # SET TITLE to INFO
    #
    #     num = 0
    #     if len(items) < 3:  # If LESS then FIVE ITEMS were FOUND then set NUM to the ACTORS LIST LENGTH
    #         max = len(items) - 1
    #
    #     elif len(items) >= 3:  # If FIVE or MORE ITEMS were FOUND then SET NUM to FIVE
    #         max = 3
    #
    #     while num < max:  # NAME POSITIONS of most USED ITEMS
    #         itemlistString += "\n**" + str(num + 1) + "** ~ *" + str(items[num]) + "*"
    #         num += 1

    #CREATING DURATION MEAN from the past X days
    durationString = "\n**Average Match Time:** *" + str(round(tools.giveMeanOfListTOOL(duration) / 60, 2)) + " minutes*"

    # CREATING KILLS MEAN from the past X days
    killsString = "\n**Average Kills:** *" + str(round(tools.giveMeanOfListTOOL(kills), 2)) + "*"

    # CREATING ASSISTS MEAN from the past X days
    assistsString = "\n**Average Assists:** *" + str(round(tools.giveMeanOfListTOOL(assists), 2)) + "*"

    # CREATING DEATHS MEAN from the past X days
    deathString = "\n**Average Deaths:** *" + str(round(tools.giveMeanOfListTOOL(deaths), 2)) + "*"

    # CREATING FARM MEAN from the past X days
    farmString = "\n**Average Farm:** *" + str(round(tools.giveMeanOfListTOOL(farm), 2)) + "*"

    # CREATING MINIONKILLS MEAN from the past X days
    minionkillsString = "\n**Average Minion Kills:** *" + str(round(tools.giveMeanOfListTOOL(minionKills), 2)) + "*"

    # CREATING WINNER MEAN from the past X days
    winnerString = "\n**Victory Rate:** *" + str(round(tools.giveMeanOfListTOOL(winner) * 100)) + "%*"

    # CREATING WENTAFK MEAN from the past X days
    wentafkString = "\n**AFK Rate:** *" + str(round(tools.giveMeanOfListTOOL(wentAfk) * 100)) + "%*"

    # CREATING TURRETCAPTURES MEAN from the past X days
    turrentcapturesString = "\n**Total Turrets Destroyed:** *" + str(round(sum(turretCaptures))) + "*"

    # CREATING KRAKEN MEAN from the past X days
    krakenString = "\n**Total Kraken Captures:** *" + str(round(sum(krakenCaptures))) + "*"

    # CREATING MEAN GOLDMINECAPTURES from the past X days
    goldmineString = "\n**Total Gold Mine Captures:** *" + str(round(sum(goldMineCaptures))) + "*"

    # CREATING MEAN CRYSTALMINECAPTURES from the past X days
    crystalmineString = "\n**Total Sentry Captures:** *" + str(round(sum(crystalMineCaptures))) + "*"

    # CREATING LEVEL from the past X days
    # levelString = "\n**Players Level:** *" + str(level) + "*"

    # # CREATING  MEAN from the past X days
    # msg = "\n**** *" + str(round(tools.giveMeanOfList())) + "*"

    if game_mode == "":  # If no specific GAMETYPE was given then set GAME to ANY
        game_mode = "any"

    # Create the TITLE for EMBED
    title = "Match performance from " + str(game_mode) + " matches in the past " + str(days) + " days | Sampled: " + str(size) + " games"

    # Create the DESCRIPTION for the EMBED
    description = "**Player:** *" + str(name) + "* **| Lv:** *" + str(level) + "* **| ST:** *" + str(VG_toolbox.giveSkillTierVG(skillTier)) + "* **| K:** *" + str(VG_toolbox.giveKarmaVG(karmaLevel)) + "*\n**Last Game Registered:** *" + str(latestmatch) + "*\n" + str(durationString) + str(gamemodelistString) + "\n" + str(winnerString) + str(wentafkString)

    # ASSEMBLE the TOP LIST TOGETHER for EMBED
    toplist = str(actorslistString)

    # ASSEMBLE the STATS TOGETHER for EMBED
    staticsOne = str(killsString) + str(assistsString) + str(deathString) + str(farmString) +  str(minionkillsString) + str(turrentcapturesString) +  str(crystalmineString) + str(goldmineString) + str(krakenString)

    # CREATE the EMBED
    embed = discord.Embed(title=title, colour=discord.Colour(0x4e9ff9), description=description, timestamp=datetime.datetime.now())

    # Set the HEADER
    embed.set_author(name="Halcyon Hackers", url="https://github.com/ClarkThyLord/Computer-BOT", icon_url="http://i67.tinypic.com/25738l1.jpg")

    # Set the THUMBNAIL to MOST USED HERO
    try:
        embed.set_thumbnail(url=thumbnail)
    except:  # If THUMBNAIL couldn't be REACHED then MAKE THUMBNAIL the Vainglory logo
        embed.set_thumbnail(url="http://i63.tinypic.com/9k6xcj.jpg")

    # ADD TOP LIST to the EMBED
    embed.add_field(name="Top Elements:", value=toplist)

    # ADD PART ONE of STATICS to EMBED
    embed.add_field(name="Overall Match Stats:", value=staticsOne)

    # ADD FOOTER of STATICS to EMBED
    embed.set_footer(text=signatureDISCORD, icon_url=botImageDISCORD)

    # SEND the EMBED
    return embed

def getLatestMatchVG(name, server="na", game_mode="", auto=False):
    name = str(name)             # Convert ID to a STRING to prevent ERRORS
    server = str(server)         # Convert SERVER to STRING to prevent ERRORS
    game_mode = str(game_mode)   # Convert MODE to STRING to prevent ERRORS
    auto = bool(auto)            # Convert AUTO to BOOLEAN to prevent errors

    matches = getMatchesVG(1, name, server, game_mode=game_mode, auto=auto)

    # If NO MATCHES were RETURNED
    if matches == False:
        msg = "Couldn't find"

        if game_mode != "":
            msg += " any **" + str(game_mode) + "** matches"

        else:
            msg += " anything"

        msg += " of **" + str(name) + "** in the past **31** days in **" + str(
            server) + "** server!"

        return msg

    # MATCH VARIABLES USED
    # latestmatch, gameMode, winner, heroKillsA, goldA, acesEarnedA, krakenCapturesA, turretKillsA,
    # turretsRemainingA ,heroKillsB, goldB, acesEarnedB, krakenCapturesB, turretKillsB, turretsRemainingB
    player1 = {}
    player2 = {}
    player3 = {}
    player4 = {}
    player5 = {}
    player6 = {}

    roasternum = 0
    playernum = 0
    for match in matches:  # From that MATCH get the VAINGLORY PLAYER ID
        latestmatchraw = dateutil.parser.parse(match.createdAt)
        latestmatch = latestmatchraw.strftime('%d/%m/%Y %H:%M:%S') + " GMT"
        gameMode = str(match.gameMode)

        for roaster in match.rosters:
            roasterdata = roaster.to_dict()
            roasterattributes = roasterdata["attributes"]
            roasterstats = roasterattributes["stats"]

            # FOR DEBUGGING
            # print(str(roasterdata) + " | RoasterData")
            # print(str(roasterattributes) + " | RoastersAttributes")
            # print(str(roasterstats) + " | RoasterStats")

            if roasternum == 0:
                heroKillsA = roasterstats["heroKills"]
                goldA = roasterstats["gold"]
                acesEarnedA = roasterstats["acesEarned"]
                krakenCapturesA = roasterstats["krakenCaptures"]
                turretKillsA = roasterstats["turretKills"]
                turretsRemainingA = roasterstats["turretsRemaining"]

            elif roasternum == 1:
                heroKillsB = roasterstats["heroKills"]
                goldB = roasterstats["gold"]
                acesEarnedB = roasterstats["acesEarned"]
                krakenCapturesB = roasterstats["krakenCaptures"]
                turretKillsB = roasterstats["turretKills"]
                turretsRemainingB = roasterstats["turretsRemaining"]

            roasternum += 1

            for participant in roaster.participants:
                matchstats = participant.stats  # INFORMATION belonging to the MATCH about CURRENT PLAYER
                playerstats = participant.player.stats  # INFORMATION belonging to the PLAYER about CURRENT PLAYER

                # FOR DEBUGGING
                # print(str(matchstats) + " | MatchStats")
                # print(str(playerstats) + " | PlayerStats")

                if participant.player.name == name:
                    thumbnail = str(VG_toolbox.giveKarmaVG(matchstats["karmaLevel"], 1))

                if playernum == 0:
                    if str(matchstats["winner"]) == "True":
                        winner = "Team A"

                    player1["name"] = str(participant.player.name)
                    player1["level"] = str(playerstats["level"])
                    player1["karmaLevel"] = str(matchstats["karmaLevel"])
                    player1["skillTier"] = str(matchstats["skillTier"])

                    player1["actor"] = str(pretty(participant.actor).replace("*", ""))
                    player1["kills"] = str(matchstats["kills"])
                    player1["assists"] = str(matchstats["assists"])
                    player1["deaths"] = str(matchstats["deaths"])
                    player1["farm"] = str(matchstats["farm"])

                elif playernum == 1:
                    player2["name"] = str(participant.player.name)
                    player2["level"] = str(playerstats["level"])
                    player2["karmaLevel"] = str(matchstats["karmaLevel"])
                    player2["skillTier"] = str(matchstats["skillTier"])

                    player2["actor"] = str(pretty(participant.actor).replace("*", ""))
                    player2["kills"] = str(matchstats["kills"])
                    player2["assists"] = str(matchstats["assists"])
                    player2["deaths"] = str(matchstats["deaths"])
                    player2["farm"] = str(matchstats["farm"])

                elif playernum == 2:
                    player3["name"] = str(participant.player.name)
                    player3["level"] = str(playerstats["level"])
                    player3["karmaLevel"] = str(matchstats["karmaLevel"])
                    player3["skillTier"] = str(matchstats["skillTier"])

                    player3["actor"] = str(pretty(participant.actor).replace("*", ""))
                    player3["kills"] = str(matchstats["kills"])
                    player3["assists"] = str(matchstats["assists"])
                    player3["deaths"] = str(matchstats["deaths"])
                    player3["farm"] = str(matchstats["farm"])

                elif playernum == 3:
                    if str(matchstats["winner"]) == "True":
                        winner = "Team B"

                    player4["name"] = str(participant.player.name)
                    player4["level"] = str(playerstats["level"])
                    player4["karmaLevel"] = str(matchstats["karmaLevel"])
                    player4["skillTier"] = str(matchstats["skillTier"])

                    player4["actor"] = str(pretty(participant.actor).replace("*", ""))
                    player4["kills"] = str(matchstats["kills"])
                    player4["assists"] = str(matchstats["assists"])
                    player4["deaths"] = str(matchstats["deaths"])
                    player4["farm"] = str(matchstats["farm"])

                elif playernum == 4:
                    player5["name"] = str(participant.player.name)
                    player5["level"] = str(playerstats["level"])
                    player5["karmaLevel"] = str(matchstats["karmaLevel"])
                    player5["skillTier"] = str(matchstats["skillTier"])

                    player5["actor"] = str(pretty(participant.actor).replace("*", ""))
                    player5["kills"] = str(matchstats["kills"])
                    player5["assists"] = str(matchstats["assists"])
                    player5["deaths"] = str(matchstats["deaths"])
                    player5["farm"] = str(matchstats["farm"])

                elif playernum == 5:
                    player6["name"] = str(participant.player.name)
                    player6["level"] = str(playerstats["level"])
                    player6["karmaLevel"] = str(matchstats["karmaLevel"])
                    player6["skillTier"] = str(matchstats["skillTier"])

                    player6["actor"] = str(pretty(participant.actor).replace("*", ""))
                    player6["kills"] = str(matchstats["kills"])
                    player6["assists"] = str(matchstats["assists"])
                    player6["deaths"] = str(matchstats["deaths"])
                    player6["farm"] = str(matchstats["farm"])

                playernum += 1

    # FOR DEBUGGING
    # print(str(player1) + " | player1")
    # print(str(player2) + " | player2")
    # print(str(player3) + " | player3")
    # print(str(player4) + " | player4")
    # print(str(player5) + " | player5")
    # print(str(player6) + " | player6")

    # Create STRING for TEAMA
    teamAString = "**Kills:** *" + str(heroKillsA) + "* **| Deaths:** *" + str(heroKillsB) + "* **| Aces:** *" + str(acesEarnedA) + "* **| Kraken Captures:** *" + str(krakenCapturesA) + "* **| Gold:** *" + str(goldA) + "* **| Turrets Destroyed:** *" + str(turretKillsA) + "* **| Turrets Left:** *" + str(turretsRemainingA) + "*"

    # Create STRING for PLAYER1
    player1String = "\n\n**Player:** *" + str(player1["name"]) + "* **| Lv:** *" + str(player1["level"]) + "* **| ST:** *" + str(VG_toolbox.giveSkillTierVG(player1["skillTier"])) + "* **| K:** *" + str(VG_toolbox.giveKarmaVG(player1["karmaLevel"])) + "*\n**Actor:** *" + str(player1["actor"]) + "* **| Kills:** *" + str(player1["kills"]) + "* **| Assists:** *" + player1["assists"] + "* **| Deaths:** *" + player1["deaths"] + "* **| Grind:** *" + player1["farm"] + "*"

    # Create STRING for PLAYER2
    player2String = "\n\n**Player:** *" + str(player2["name"]) + "* **| Lv:** *" + str(player2["level"]) + "* **| ST:** *" + str(VG_toolbox.giveSkillTierVG(player2["skillTier"])) + "* **| K:** *" + str(VG_toolbox.giveKarmaVG(player2["karmaLevel"])) + "*\n**Actor:** *" + str(player2["actor"]) + "* **| Kills:** *" + str(player2["kills"]) + "* **| Assists:** *" + player2["assists"] + "* **| Deaths:** *" + player2["deaths"] + "* **| Grind:** *" + player2["farm"] + "*"

    # Create STRING for PLAYER3
    player3String = "\n\n**Player:** *" + str(player3["name"]) + "* **| Lv:** *" + str(player3["level"]) + "* **| ST:** *" + str(VG_toolbox.giveSkillTierVG(player3["skillTier"])) + "* **| K:** *" + str(VG_toolbox.giveKarmaVG(player3["karmaLevel"])) + "*\n**Actor:** *" + str(player3["actor"]) + "* **| Kills:** *" + str(player3["kills"]) + "* **| Assists:** *" + player3["assists"] + "* **| Deaths:** *" + player3["deaths"] + "* **| Grind:** *" + player3["farm"] + "*"

    # Create STRING for TEAMB
    teamBString = "**Kills:** *" + str(heroKillsB) + "* **| Deaths:** *" + str(heroKillsA) + "* **| Aces:** *" + str(acesEarnedB) + "* **| Kraken Captures:** *" + str(krakenCapturesB) + "* **| Gold:** *" + str(goldB) + "* **| Turrets Destroyed:** *" + str(turretKillsB) + "* **| Turrets Left:** *" + str(turretsRemainingB) + "*"

    # Create STRING for PLAYER4
    player4String = "\n\n**Player:** *" + str(player4["name"]) + "* **| Lv:** *" + str(player4["level"]) + "* **| ST:** *" + str(VG_toolbox.giveSkillTierVG(player4["skillTier"])) + "* **| K:** *" + str(VG_toolbox.giveKarmaVG(player4["karmaLevel"])) + "*\n**Actor:** *" + str(player4["actor"]) + "* **| Kills:** *" + str(player4["kills"]) + "* **| Assists:** *" + player4["assists"] + "* **| Deaths:** *" + player4["deaths"] + "* **| Grind:** *" + player4["farm"] + "*"

    # Create STRING for PLAYER5
    player5String = "\n\n**Player:** *" + str(player5["name"]) + "* **| Lv:** *" + str(player5["level"]) + "* **| ST:** *" + str(VG_toolbox.giveSkillTierVG(player5["skillTier"])) + "* **| K:** *" + str(VG_toolbox.giveKarmaVG(player5["karmaLevel"])) + "*\n**Actor:** *" + str(player5["actor"]) + "* **| Kills:** *" + str(player5["kills"]) + "* **| Assists:** *" + player5["assists"] + "* **| Deaths:** *" + player5["deaths"] + "* **| Grind:** *" + player5["farm"] + "*"

    # Create STRING for PLAYER6
    player6String = "\n\n**Player:** *" + str(player6["name"]) + "* **| Lv:** *" + str(player6["level"]) + "* **| ST:** *" + str(VG_toolbox.giveSkillTierVG(player6["skillTier"])) + "* **| K:** *" + str(VG_toolbox.giveKarmaVG(player6["karmaLevel"])) + "*\n**Actor:** *" + str(player6["actor"]) + "* **| Kills:** *" + str(player6["kills"]) + "* **| Assists:** *" + player6["assists"] + "* **| Deaths:** *" + player6["deaths"] + "* **| Grind:** *" + player6["farm"] + "*"

    # Create the TITLE for EMBED
    title = "Latest match from " + str(name) + " in the past 31 days | Game Type: " + str(VG_toolbox.giveMatchVG(gameMode)) + " | Date: " + str(latestmatch)

    # Create the DESCRIPTION for the EMBED
    description = "**Match Winner:** *" + str(winner) + "*"

    # ASSEMBLE the TOP LIST TOGETHER for EMBED
    teamAINFO = str(teamAString) + str(player1String) + str(player2String) + str(player3String)

    # ASSEMBLE the STATS TOGETHER for EMBED
    teamBINFO = str(teamBString) + str(player4String) + str(player5String) + str(player6String)

    # CREATE the EMBED
    embed = discord.Embed(title=title, colour=discord.Colour(0x4e9ff9), description=description, timestamp=datetime.datetime.now())

    # Set the HEADER
    embed.set_author(name="Halcyon Hackers", url="https://github.com/ClarkThyLord/Computer-BOT", icon_url="http://i67.tinypic.com/25738l1.jpg")

    # Set the THUMBNAIL to MOST USED HERO
    try:
        embed.set_thumbnail(url=thumbnail)
    except:  # If THUMBNAIL couldn't be REACHED then MAKE THUMBNAIL the Vainglory logo
        embed.set_thumbnail(url="http://i63.tinypic.com/9k6xcj.jpg")

    # ADD TOP LIST to the EMBED
    embed.add_field(name="Team A:", value=teamAINFO)

    # ADD PART ONE of STATICS to EMBED
    embed.add_field(name="Team B:", value=teamBINFO)

    # ADD FOOTER of STATICS to EMBED
    embed.set_footer(text=signatureDISCORD, icon_url=botImageDISCORD)

    # SEND the EMBED
    return embed

def getMatches(ign, m, region='na',page =1, num =1):
    t1_tier = 0
    t2_tier = 0
    t1 = m.rosters[0]
    t2 = m.rosters[1]
    t1_participants = ''
    t2_participants = ''
    duration  = format((m.duration // 60) + ((m.duration % 60) /100), '.2f')
    duration = duration.replace('.', ':')
    for i in m.rosters[0].participants:
        i.actor = heroes.get(i.actor, i.actor)
        i.actor = (i.actor).replace('*','')
        if i.player.name == ign:
            player = i
        t1_tier += i.stats['skillTier']
    for i in m.rosters[1].participants:
        i.actor = heroes.get(i.actor, i.actor)
        i.actor = (i.actor).replace('*','')
        t2_tier += i.stats['skillTier']
        
    for i in m.rosters[1].participants:
        if i.player.name == ign:
            t1_tier,t2_tier = t2_tier,t1_tier
            t1,t2 = t2,t1
            player = i

    gamemode = match_dict.get(m.gameMode, m.gameMode)
    if t1.participants[0].stats['winner']:
        result = 'Victory'
        resultcolor = 0x2fe26e
        thumburl = 'https://s2.postimg.org/barjsw3e1/victory.png'
    else:
        result = 'Defeat'
        resultcolor = 0xe22f2f
        thumburl = 'https://s1.postimg.org/y4uwz4eu7/defeat.png'

    #Trophies
    for team in range(len(m.rosters)):
        for player_no in range(len(m.rosters[team].participants)):
            if  m.rosters[team].participants[player_no].name == ign:
                break
       
    tel = telemetry_wrapper.telemetry(m, team, player_no)
    trophy_dict = trophies.trophy_giver(tel)
         
        
    if t1.stats['side'] == 'left/blue':
        t1_color = "Blue:"
        t2_color = "Orange:"
    else:
        t1_color = "Orange:"
        t2_color = "Blue:"
    for i in t1.participants:
        t1_participants += '**{}** | {} | {}/{}/{}\n'.format(i.player.name, i.actor, i.stats['kills'], i.stats['deaths'], i.stats['assists'])
    for i in t2.participants:
        t2_participants += '**{}** | {} | {}/{}/{}\n'.format(i.player.name, i.actor, i.stats['kills'], i.stats['deaths'], i.stats['assists'])
    
    details = "{} Kills {} | {} Turrets {} | {} Krakens {} | {} Aces {} | {} Gold {}".format(str(t1.stats['heroKills']), str(t2.stats['heroKills']), str(t1.stats['turretsRemaining']), str(t2.stats['turretsRemaining']), str(t1.stats['krakenCaptures']),str( t2.stats['krakenCaptures']), str(t1.stats['acesEarned']), str(t2.stats['acesEarned']), str(t1.stats['gold']), str(t2.stats['gold']))
    winchance = str(int(round(100 * (t1_tier/ (t1_tier+t2_tier)), 0)))
    krakens = str(m.rosters[0].stats['krakenCaptures'] + m.rosters[1].stats['krakenCaptures'])
    em = discord.Embed(title=result +' | '+ gamemode, description= '{} Minutes Long.\n{} Krakens Taken.\nVictory Chance: {}%'.format(duration, krakens, winchance) , colour=resultcolor, url = "http://ezlgg.com", timestamp = dateutil.parser.parse(m.createdAt).replace(tzinfo=None))
    em.add_field(name = t1_color, value = t1_participants)
    em.add_field(name = t2_color, value = t2_participants)
    em.add_field(name = "Details:", value = details, inline = False)
    
    for category in trophy_dict:
        if category != []:
            for trophy in trophy_dict[category]:
                em.add_field(name = category + " Trophy Earned!", value = "*" + trophy + "*", inline = False)
    
    em.set_author(name=ign, icon_url="http://www.vaingloryfire.com/images/wikibase/icon/heroes/"+player.actor+".png", url = 'http://www.vaingloryfire.com/vainglory/wiki/heroes/'+player.actor)
    em.set_footer(text= ign+' | Page {}/{}'.format(str(page),str(num)), icon_url= "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcREVEEL3vFm3boDZD0aSwSPFtZ2EXJGwiEjsnvXXTluLqXrD0mknNohwA")
    em.set_thumbnail(url = thumburl)
    return em

    
def getTrophies(name, server, earned):
    try:
        m = apiVG.matches({"page[limit]": 50, "filter[playerNames]": name, "filter[createdAt-start]": "2017-01-01T08:25:30Z", "sort": "-createdAt"}, region=server)
    except:
       return "Error! Matches were not found."
       
    new = {"Hero" :{}, "Item":{}, "Match Goals":{}}

    for match in m:
        for team in range(len(m.rosters)):
            for player_no in range(len(m.rosters[team].participants)):
                if  m.rosters[team].participants[player_no].name == ign:
                    break
                
        tel = telemetry_wrapper.telemetry(match, team, player_no)
        t_list = trophies.trophy_giver(tel)
        for cat in trophies.trophy_giver(tel):
            for trophy in cat:
                if trophy in earned[cat]:
                    pass
                else:
                    new[cat].append(trophy)
                    earned[cat].append(trophy)
                    
    return earned, new
    
        
       
        