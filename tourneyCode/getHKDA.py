#Modified from Github python-gamelocker/examples/kda.py
import gamelocker, config, Player
from gamelocker.strings import pretty

api = gamelocker.Gamelocker(config.vgKey).Vainglory()

def getMatchStats(IGN):
    finalStats = []

    #
    # FinalStats = [<win/lose> for team Left, {Dict for T1_Player1}, {Dict for T1_Player2}, {Dict for T1_Player3},
    #               <win/lose> for team right, {Dict for T2_Player1}, {Dict for T2_Player2}, {Dict for T2_Player3}
    # Dict {IGN, HERO, KILLS, DEATHS, ASSISTS, BUILD}
    #
    matches = api.matches({"sort": "-createdAt",
                           "filter[playerNames]": IGN,
                           "filter[createdAt-start]": "2017-03-10T00:00:00Z",
                           "page[limit]": "5"})

    if (matches == False):
        print ("No Matches found")


    # For now using Ranked Games, but
    # have to include check for match.gameMode == 'private_party_draft_match'
    #
    #
    # elif (matches[0].gameMode == 'private_party_draft_match'):
    else:
        matches = sorted(matches, key=lambda d: d.createdAt, reverse=True)
        match = matches[0]
        print('Time Played: ', match.createdAt)
        print('GameMode: ', match.gameMode)
        print('Telemetry: ', match.assets[0].url)
        finalStats.append(match.gameMode)
        for team in range(len(match.rosters)):

            #print("\nTeam", match.rosters[team].stats["side"])
            finalStats.append(match.rosters[team].participants[0].stats["winner"])

            for player in range(len(match.rosters[team].participants)):

                name = match.rosters[team].participants[player].player.name
                #name = Player.Player(name)

                hero = pretty(match.rosters[team].participants[player].actor)
                #name.hero = pretty(match.rosters[team].participants[player].actor)

                k = match.rosters[team].participants[player].stats["kills"]
                #name.k = match.rosters[team].participants[player].stats["kills"]

                d = match.rosters[team].participants[player].stats["deaths"]
                #name.d = match.rosters[team].participants[player].stats["deaths"]

                a = match.rosters[team].participants[player].stats["assists"]
                #name.a = match.rosters[team].participants[player].stats["assists"]

                builds = match.rosters[team].participants[player].stats["items"]
                #name.builds = match.rosters[team].participants[player].stats["items"]

                win = match.rosters[team].participants[player].stats["winner"]
                #name.win = match.rosters[team].participants[player].stats["winner"]

                finalStats.append({'ign': name, 'hero': hero, 'kills': k, 'deaths': d, 'assists': a, 'build': builds})
                #
                # Take a look at Players.py to get more information about the member varaible for a player object.
                #
                #print (name, win, hero, k, '/', d, '/', a, '/', builds)
    return(finalStats)