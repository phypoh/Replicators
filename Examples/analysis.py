#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 17:22:12 2017

@author: physiX
"""

from datetime import datetime
import dateutil.parser
import discord
from discord.ext import commands
import gamelocker
from gamelocker.strings import pretty


APIKEY = input("API Key:")
date = "2017-01-01T08:25:30Z"

bot = commands.Bot(command_prefix='!')

api = gamelocker.Gamelocker(APIKEY).Vainglory()

        
#************************************************************************************************************
#WORKING FUNCTIONS
#************************************************************************************************************ 

def tourneypull_a(IGN):
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
        return(output) 
    except:
        return("Not Found.")
        
        
def profile_a(IGN):
    try:
        matches = api.matches({"page[limit]": 50, "filter[createdAt-start]": date, "filter[playerNames]": IGN})
        matches.sort(key=lambda x: x.createdAt, reverse=True)
        pool = {}
        games = 0
        wins = 0
        kills = 0
        assists = 0
        deaths = 0

        for match in matches:
            for team in range(len(match.rosters)):
                for player in range(len(match.rosters[team].participants)):
                    if IGN == match.rosters[team].participants[player].player.name:    
                        hero = pretty(match.rosters[team].participants[player].actor)
                        kills += match.rosters[team].participants[player].stats["kills"]
                        assists += match.rosters[team].participants[player].stats["assists"]
                        deaths += match.rosters[team].participants[player].stats["deaths"]
                        if hero not in pool:            
                            pool.setdefault(hero,[0,0])
                        pool[hero][0] += 1
                        if match.rosters[team].participants[player].stats['winner']:
                            pool[hero][1] += 1
        
        for hero in pool:
            games += pool[hero][0]
            wins += pool[hero][1]

        winrate = str(round(wins/games*100, 1)) + "%"            
        
        output = ''
        hero_freq = sorted(pool, key=pool.get, reverse=True)[:3]
        for hero in hero_freq:
            output += hero + ": " + str(pool[hero][0]) + " ("+ str(round(pool[hero][1]/pool[hero][0]*100, 1)) + "%)\n"
            
        fav_hero = "http://www.vaingloryfire.com/images/wikibase/icon/heroes/" + hero_freq[0] + ".png"
    
        lastseen = dateutil.parser.parse(matches[0].createdAt)

        #EMBEDS
        embed = discord.Embed(title=IGN, colour=discord.Colour(0x40e0d0)) # http://www.colorhexa.com/
    
        try:
            embed.set_thumbnail(url=fav_hero)
        except:
            embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
    
        embed.add_field(name= '**Last game played**: ', value = lastseen.strftime('%d/%m/%Y %H:%M:%S') + " GMT")
        embed.add_field(name= '**Favourite Heroes: (Win rates)**', value = output)
        embed.add_field(name= '**Win Rate:**', value = winrate)
        embed.add_field(name= '**Kills per game:**', value = round(kills/games, 1))
        embed.add_field(name= '**Assists per game:**', value = round(assists/games, 1))
        embed.add_field(name= '**Deaths per game:**', value = round(deaths/games, 1))
        embed.add_field(name= '**Average KDA:**', value = round((kills+assists)/deaths, 1))
        return(embed)  
    except:
        return("Not Found.")
        
def matchpull_a(IGN):
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
        return(output) 
    except:
        return("Not Found.")
        
        
#************************************************************************************************************
#UNUSED FUNCTIONS
#************************************************************************************************************ 
        
def performance_a(IGN):
    try:    
        matches = api.matches({"page[limit]": 50, "filter[createdAt-start]": date, "filter[playerNames]": IGN})
        matches.sort(key=lambda x: x.createdAt, reverse=True)
        pool = {}
        i = 0
        for match in matches:
            i += 1
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
        return(output)    
    except:
        return("Invalid Name")
