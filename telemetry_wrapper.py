"""

Telemetry Wrapper

Input: Match object from Shutterfly's wrapper, team (0 or 1) and player (0, 1, 2)
Output: Kills, Deaths, Item Buys and Neutral Kills


"""
from strings import pretty

class telemetry(object):
    def __init__(self, match, team, player):        
        self.IGN = match.rosters[team].participants[player].player.name
        self.hero = pretty(match.rosters[team].participants[player].actor)
        self.telem = requests.get(match.assets[0].url).json()
        
           
       
        kill_dict = {}
        death_dict = {}
        item_dict = {}
        neutral_dict = {}
        for datum in self.telem:
        

            #Kills and Deaths
            if datum["type"] == "KillActor":
                if datum["payload"]["IsHero"] == 1 and datum["payload"]["TargetIsHero"] == 1:
                    #Kills
                    if pretty(datum["payload"]["Actor"]) == self.hero:
                        target = pretty(datum["payload"]["Killed"])
                        kill_dict.setdefault(target,0)
                        kill_dict[target] += 1
                    #Deaths
                    elif pretty(datum["payload"]["Killed"]) == self.hero:
                        target = pretty(datum["payload"]["Actor"])
                        death_dict.setdefault(target,0)
                        death_dict[target] += 1
                    
                    
            #Item Buys
            elif datum["type"] == "BuyItem":
                if pretty(datum["payload"]["Actor"]) == self.hero:
                   item = datum["payload"]["Item"]
                   item_dict.setdefault(item,0)
                   item_dict[item] += 1
            
            #Minion Kills
            if datum["type"] == "KillActor":
                if datum["payload"]["IsHero"] == 1 and datum["payload"]["TargetIsHero"] == 0:
                    if pretty(datum["payload"]["Actor"]) == self.hero:
                        target = pretty(datum["payload"]["Killed"])
                        neutral_dict.setdefault(target,0)
                        neutral_dict[target] += 1
           
        self.kills = kill_dict
        self.deaths = death_dict
        self.itemBuys = item_dict
        self.neutrals = neutral_dict
        
        
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