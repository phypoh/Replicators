import gamelocker, pickle, datetime, random, requests
from datetime import timedelta
from VG_module import keyVG
"""
Verify users through unique item patterns.
"""

api = gamelocker.Gamelocker(keyVG).Vainglory()

try:
    with open('auth.pickle', 'rb') as handle:
        auth = pickle.load(handle)
except:
    auth = dict() #Initializes auth
    auth['confirmed'] = list() #For 100% confirmed igns.


def storeAuth():
    with open("auth.pickle", "wb") as handle:
        pickle.dump(auth, handle, protocol=pickle.HIGHEST_PROTOCOL)

def start(discordid,ign, region):
    # 0 = Halcyon Potion
    # 1 = Weapon Infusion
    # 2 = Crystal Infusion
    try:
        if auth[discordid]['ign'] == ign and auth[discordid]['confirmed']:
            if auth[discordid]['confirmed']:
                raise  ValueError("You've already confirmed your ign.")
    except:
        pass
    if ign in auth['confirmed']:
        raise ValueError('IGN already confirmed.')
    region = region.lower()
    if region == 'sea':
        region = 'sg'
    if region not in ['na', 'sg', 'eu', 'ea', 'sa']:
        raise ValueError("Invalid Region.")

    try: #SO they can verfy again without crowding up auth['confirmed']
        auth['confirmed'].remove(auth[discordid]['ign'])
    except:
        pass
    auth[discordid] = dict()
    auth[discordid]['region'] = region
    auth[discordid]['ign'] = ign
    auth[discordid]['confirmed'] = False
    auth[discordid]['startdate'] = (datetime.datetime.utcnow() - timedelta(minutes=5)).isoformat().split('.')[0] + 'Z' #date in iso 8601  so we can check for new matches.
    pattern = []
    for i in range(0,5):
        pattern.append(random.choice(range(0,3))) #random from 0,1,2
    auth[discordid]['pattern'] = pattern
    storeAuth()
    return pattern

def check(discordid):
    if auth[discordid]['confirmed']:
        raise ValueError("Already confirmed!")
    ign  = auth[discordid]['ign']
    region  = auth[discordid]['region']
    try:
        m = api.matches({"page[limit]": 1, "filter[playerNames]": ign, "filter[createdAt-start]": auth[discordid]['startdate'], "sort": "-createdAt", 'filter[gameMode]': 'blitz_pvp_ranked'}, region = region)
        m = m[0]
    except:
        raise ValueError("No new matches.")
    r = requests.get(m.assets[0].url) #telemetry.json
    for i in m.rosters:
        for k in i.participants:
            if k.player.name == ign:
                actor = k.actor
                if i.stats['side'] == 'left/blue':
                    side = 'Left'
                else:
                    side = 'Right'
                break
    data = r.json()
    items = []
    for i in data:
        if len(items) == 5:
            break
        if i['type'] == 'BuyItem' and i['payload']['Team'] == side and i['payload']['Actor'] == actor:
            items.append(i['payload']['Item'])
    for i in items:
        if i == 'Halcyon Potion':
            items[items.index(i)] = 0 #Converts Halcyon Potion to 0
        elif i == 'Weapon Infusion':
            items[items.index(i)] = 1
        elif i == 'Crystal Infusion':
            items[items.index(i)] = 2
        else:
            items[items.index(i)] = "Other"
    if sorted(items, key=int) == sorted(auth[discordid]['pattern'], key=int): #So order doesn't matter
        auth[discordid]['confirmed']=True
        auth['confirmed'].append(ign) #adds to list of confirmed igns
        storeAuth()
        return("Authorized Account")
    else:
        items = [x if x != 0 else 'Halcyon Potion' for x in items]
        items = [x if x != 1 else 'Weapon Infusion' for x in items] #Checks for all 1's and replaces it with Weapon Infusion
        items  = [x if x != 2 else 'Crystal Infusion' for x in items] #Checks for all 2's and replaces it with Crystal Infusion
        raise ValueError('Invalid Pattern:\nYours: '+ str(sorted(items, key=int)) + "\nPattern: "+ str(sorted(auth[discordid]['pattern'], key=int)) + '\nRemember patterns are meant to be bought in order.')


def isauth(discordid, ign): #checks if discordid is confirmed on the ign given
    try:
        if auth[discordid]['ign']== ign and auth[discordid]['confirmed']:
            return True
        else:
            return False
    except:
        return False

def ign(ign): #Checks if ign is confirmed
    if ign in auth['confirmed']:
        return True
    return False

def id(discordid): #checks if discordid is confirmed
    return auth[discordid]['confirmed']

def id_to_ign(discordid):
    return auth[discordid]['ign']

def to_dict(discordid):
    return auth[discordid]
