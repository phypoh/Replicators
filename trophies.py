"""

List of trophies

"""
import telemetry_wrapper
import gamelocker

trophy_list = {}

trophy_list["Hero"] = {
"Let the Skye Fall":{"image":"http://i.imgur.com/aukoXll.png", 
            "description": "Let the Skye Fall\nKill Skye 10 times in a match"},

"Throwzo": {"image":"http://i.imgur.com/aukoXll.png",
        "description": "Throwzo\nWin a match with 10 deaths on Ozo or more"},

"Double Down": {"image":"http://i.imgur.com/aukoXll.png",
        "description":"Double Down\nWin a game with exactly 2 deaths on Ringo"},

"Killed Someone":{"image":"http://i.imgur.com/aukoXll.png",
        "description":"Killed Someone\nTestTrophy"}
                
        
}

trophy_list["Match Goals"] = {
"Here to Impress": {"image":"http://i.imgur.com/aukoXll.png",
        "description":"Here to Impress\nWin a match with 0 deaths"},
"Da Damage Dealer": {"image":"http://i.imgur.com/aukoXll.png",
        "description":"Da Damage Dealer\nDeal >50,000 accumulated damage to heroes in a single match"}
}
        

def trophy_giver(player):
    trophies = {"Hero" :{}, "Item":{}, "Match Goals":{}}
    
    #HERO TROPHIES
    """
    Let the Skye Fall
    Kill Skye 10 times in a match
    """
    if "Skye" in player.kills:
        if player.kills["Skye"] >= 10:
            trophies["Hero"].append("Let the Skye Fall":trophy_list["Hero"]["Let the Skye Fall"])

    """
    Throwzo
    Win a match with >=10 deaths on Ozo
    """

    if player.hero == "Ozo" and player.deathTot >= 10:
        trophies["Hero"].append("Throwzo":trophy_list["Hero"]["Throwzo"])


    """
    Double Down
    Win a game with exactly 2 deaths on Ringo
    """

    if player.hero == "Ringo" and player.deathTot == 2:
        trophies["Hero"].append("Double Down":trophy_list["Hero"]["Double Down"])
        
            
    #MATCH TROPHIES        

    """
    Here to Impress
    Win a match with 0 deaths
    """
    if player.deathTot == 0 and player.result == 1:
        trophies["Match Goals"].append("Here to Impress":trophy_list["Match Goals"]["Here to Impress"])


    """
    Da Damage Dealer

    Deal >50,000 accumulated damage to heroes in a single match

    """
    if player.dealt > 50000:
        trophies["Match Goals"].append("Da Damage Dealer":trophy_list["Match Goals"]["Da Damage Dealer"])


    """
    Crazy Drunk (Use Hellfire Brew 7 times in a match)
    """



    #test code to see if it works    
    if player.killTot >= 0:
        trophies["Match Goals"].append("Killed Someone":trophy_list["Hero"]["Killed Someone"])

    return trophies

if __name__ == "__main__":
    APIKEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI4OGY2YjA0MC1kY2I1LTAxMzQtNWRjOC0wMjQyYWMxMTAwMDQiLCJpc3MiOiJnYW1lbG9ja2VyIiwib3JnIjoicGh5cG9oLWdtYWlsLWNvbSIsImFwcCI6Ijg4ZjRlZjEwLWRjYjUtMDEzNC01ZGM3LTAyNDJhYzExMDAwNCIsInB1YiI6InNlbWMiLCJ0aXRsZSI6InZhaW5nbG9yeSIsInNjb3BlIjoiY29tbXVuaXR5IiwibGltaXQiOjEwfQ.W2kh0cyVTEtaphP9V0E4C-vTL-UVq5gziAfoat0Jlc4"
    api = gamelocker.Gamelocker(APIKEY).Vainglory()
    IGN = "gabevizzle"
    date = "2017-03-10T00:00:00Z"
    

    matches = api.matches({
        "sort": "-createdAt",
        "filter[playerNames]": IGN,
        "filter[createdAt-start]": date,
        "page[limit]": "1"
    })

    match = matches[0]
    player = telemetry_wrapper.telemetry(match, 0,1)
    print(trophy_giver(player))
