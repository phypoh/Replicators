"""

Telemetry Wrapper

Input: Match object from Shutterfly's wrapper, team (0 or 1) and player (0, 1, 2)
Output: Kills, Deaths, Item Buys and Neutral Kills


"""
import gamelocker
import urllib
import requests
import sys
from datetime import datetime
import dateutil.parser
from strings import pretty


class telemetry(object):
    def __init__(self, match, team, player_no):        
        self.IGN = match.rosters[team].participants[player_no].player.name
        self.hero = pretty(match.rosters[team].participants[player_no].actor)
        if team == 0:
            self.team = "Blue"
        elif team == 1:
            self.team = "Red"
        if match.rosters[team].participants[player_no].stats['winner'] == 0:
            self.result = "Lost"
        elif match.rosters[team].participants[player_no].stats['winner'] == 1:
            self.result = "Won"
        self.tel = requests.get(match.assets[0].url).json()
        
        """
        Initializing Varialbes
        """
        self.rawDealt = 0
        self.rawReceived = 0
        self.dealt = 0
        self.received = 0
        self.dealtData = []
        self.receivedData = []
        self.gold = 0
        self.goldData = []
        self.start = dateutil.parser.parse(self.tel[0]["time"])
        self.end = dateutil.parser.parse(self.tel[-1]["time"])
        self.items = []
        self.kills = {}
        self.deaths = {}
        self.nonheroes = {}
        self.killTot = 0
        self.deathTot = 0
     

        """
        Damage and Level Up Data
        """
        
        for datum in self.tel:
            if datum["type"] == "DealDamage":
                if datum["payload"]["IsHero"] == 1 and datum["payload"]["TargetIsHero"] == 1:
                    time = (dateutil.parser.parse(datum["time"])-self.start).seconds
                    raw = datum["payload"]["Damage"]
                    num = datum["payload"]["Delt"]
                    if pretty(datum["payload"]["Target"]) == self.hero:
                        self.received += num
                        self.rawReceived += raw
                        self.receivedData.append([time, num, raw])    
                    elif pretty(datum["payload"]["Actor"]) == self.hero:
                        self.dealt += num
                        self.rawDealt += raw
                        self.dealtData.append([time, num, raw])
                        
            elif datum["type"] == "LevelUp":
                time = (dateutil.parser.parse(datum["time"])-self.start).seconds
                gold = datum["payload"]["LifetimeGold"]
                if pretty(datum["payload"]["Actor"]) == self.hero:
                    self.goldData.append([time,gold])
                    
            elif datum["type"] == "BuyItem":
                if pretty(datum["payload"]["Actor"]) == self.hero:
                    time = (dateutil.parser.parse(datum["time"])-self.start).seconds
                    item = pretty(datum["payload"]["Item"])
                    self.items.append([time, item])
                    
            elif datum["type"] == "KillActor":
                if datum["payload"]["IsHero"] == 1 and datum["payload"]["TargetIsHero"] == 1:
                    #Kills
                    if pretty(datum["payload"]["Actor"]) == self.hero:
                        target = pretty(datum["payload"]["Killed"])
                        self.kills.setdefault(target,0)
                        self.kills[target] += 1
                        self.killTot += 1
                    #Deaths
                    elif pretty(datum["payload"]["Killed"]) == self.hero:
                        target = pretty(datum["payload"]["Actor"])
                        self.deaths.setdefault(target,0)
                        self.deaths[target] += 1 
                        self.deathTot += 1      
        if self.received != 0:
            self.ratio = round(self.dealt/self.received,3)
        else: 
            self.ratio = 0
        
    def __repr__(self):
        return self.IGN + " " + self.hero
        
        
if __name__ == "__main__":  
    """
    Sample Program
    """
    
    APIKEY = ''
    api = gamelocker.Gamelocker(APIKEY).Vainglory()
    IGN = "physiX"
    date = "2017-03-16T00:00:00Z"
    """
    matches = api.matches({
        "sort": "-createdAt",
        "filter[playerNames]": IGN,
        "filter[createdAt-start]": date,
        "page[limit]": "1"
    }, "eu") 
    """
    match = matches[0]
    tel = telemetry(match, 0, 2)
    print(tel.IGN, tel.hero)
    print(tel.kills)
    print(tel.deaths)
    print(tel.itemBuys)
    print(tel.neutrals)