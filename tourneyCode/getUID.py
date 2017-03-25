#Modified from Github: python-gamelocker/examples/getID.py
import gamelocker, config, datetime


api = gamelocker.Gamelocker(config.vgKey).Vainglory()

def getID(name):
    try:
        m = api.matches({"page[limit]": 2, "filter[playerNames]": name, "filter[createdAt-start]": str(datetime.date.today() - datetime.timedelta(days=31)) + "T00:00:00Z"})
        for i in m[0].rosters:
            for j in i.participants:
                if j.player.name == name:
                    return(j.player.id)
    except:
        return("Invalid Name")