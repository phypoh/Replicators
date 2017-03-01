#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 17:22:12 2017

@author: physiX
"""

from datetime import datetime
import discord
from discord.ext import commands
import gamelocker
from gamelocker.strings import pretty

APIKEY = ENTER_TOKEN_HERE
date = "2017-01-01T08:25:30Z"

bot = commands.Bot(command_prefix='!')

api = gamelocker.Gamelocker(APIKEY).Vainglory()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')
    print(bot.user.id)

@bot.command()
async def hello():
    await bot.say("Hello! I'm Cherubim, a bot made by physiX and Angel's child. For a list of commands, please type !commands")

@bot.command()
async def commands():
    output = ""
    output += "!hello: I just say hi and how awesome physiX is.\n"
    output += "!tourneypull <IGN>: For tournament matches"
    await bot.say(output)
 
@bot.command()
async def skillz():
    await bot.say("Skillz! Look at what mama physiX made!")
    
@bot.command()
async def performance(IGN):
    try:    
        matches = api.matches({"page[limit]": 50, "filter[createdAt-start]": date, "filter[playerNames]": IGN})
        matches.sort(key=lambda x: x.createdAt, reverse=True)
        pool = {}
        for match in matches:
            for team in range(len(match.rosters)):
                for player in range(len(match.rosters[team].participants)):
                    if IGN == match.rosters[team].participants[player].player.name:    
                        hero = pretty(match.rosters[team].participants[player].actor)
                        if hero not in pool:            
                            pool.setdefault(hero,[0,0])
                        pool[hero][0] += 1
                        if match.rosters[team].participants[player].stats['winner']:
                            pool[hero][1] += 1
        output = '**Last game played**: ' + matches[0].createdAt + "\n**Win Rates:**\n"
        for hero in pool:
            output += hero + ": " + str(pool[hero][0]) + " ("+ str(round(pool[hero][1]/pool[hero][0]*100, 1)) + "% win rate)\n"    
        output += "**Total games**: " + str(i)
        await bot.say(output)    
    except:
        await bot.say("Invalid Name")                              


@bot.command()
async def tourneypull(IGN):
    try:
        match_list = api.matches({"page[limit]": 3, "filter[createdAt-start]": date, "filter[playerNames]": IGN})
        output = ""    
        i = 0
        for match in match_list:
            if (match.gameMode == "private_party_draft_match"):
                i += 1
                output += "\nGame " + str(i)
                for team in range(len(match.rosters)):
                    output += "\nTeam " + str(team+1) 
                    if match.rosters[team].participants[0].stats['winner'] == 1: 
                        output += " (Won)\n"
                    else: 
                        output += " (Lost)\n"
                    for player in range(len(match.rosters[team].participants)):
                        name = match.rosters[team].participants[player].player.name
                        hero = pretty(match.rosters[team].participants[player].actor)
                        kills = match.rosters[team].participants[player].stats["kills"]
                        deaths = match.rosters[team].participants[player].stats["deaths"]
                        assists = match.rosters[team].participants[player].stats["assists"]            
                        output += name + " " + hero + " " + str(kills) + ' / ' + str(deaths) +  ' / ' + str(assists) + "\n"
                output += "\n"
        await bot.say(output) 
    except:
        await bot.say("Not Found.")

@bot.command()
async def matchpull(IGN):
    try:
        match_list = api.matches({"page[limit]": 3, "filter[createdAt-start]": date, "filter[playerNames]": IGN})
        output = ""    
        i = 0
        for match in match_list:
            i += 1
            output += "\nGame " + str(i)
            for team in range(len(match.rosters)):
                output += "\nTeam " + str(team+1) 
                if match.rosters[team].participants[0].stats['winner'] == 1: 
                    output += " (Won)\n"
                else: 
                    output += " (Lost)\n"
                for player in range(len(match.rosters[team].participants)):
                    name = match.rosters[team].participants[player].player.name
                    hero = pretty(match.rosters[team].participants[player].actor)
                    kills = match.rosters[team].participants[player].stats["kills"]
                    deaths = match.rosters[team].participants[player].stats["deaths"]
                    assists = match.rosters[team].participants[player].stats["assists"]            
                    output += name + " " + hero + " " + str(kills) + ' / ' + str(deaths) +  ' / ' + str(assists) + "\n"
            output += "\n"
        await bot.say(output) 
    except:
        await bot.say("Not Found.")
        
"""    
@bot.command()
async def common(IGN1, IGN2): 
    match_list = api.matches({"page[limit]": 3, "filter[createdAt-start]": date, "filter[playerNames]": (IGN1, IGN2)}) 
    output = ""    
    i = 0
    for match in match_list:
        i += 1
        output += "\nGame " + str(i)
        for team in range(2):
            output += "\nTeam " + str(team+1) 
            if match.rosters[team].participants[0].stats['winner'] == 1: 
                output += " (Won)\n"
            else: 
                output += " (Lost)\n"
            for player in range(3):
                name = match.rosters[team].participants[player].player.name
                hero = pretty(match.rosters[team].participants[player].actor)
                kills = match.rosters[team].participants[player].stats["kills"]
                deaths = match.rosters[team].participants[player].stats["deaths"]
                assists = match.rosters[team].participants[player].stats["assists"]            
                output += name + " " + hero + " " + str(kills) + ' / ' + str(deaths) +  ' / ' + str(assists) + "\n"
        output += "\n"
    await bot.say(output) 
"""
    
@bot.command()
async def test(input1, input2): 
    output = ""
    output += input1 + "\n"
    output += input2 + "\n"
    await bot.say(output)
    
@bot.command()
async def angel():
    await bot.say("Hush, no one has seen Angel. Legend tells that she lives among the Clouds.")
    
  
bot.run(ENTER_TOKEN_HERE)
