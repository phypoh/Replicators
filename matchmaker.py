from discord.ext import commands
import pickle, asyncio
from discord import Embed
import gamelocker, datetime, dateutil.parser
from VG_module import keyVG
api = gamelocker.Gamelocker(keyVG).Vainglory()
msgs = dict()
import random, verify
from discord.ext.commands.cooldowns import BucketType
"""
Author: @SpiesWithin
Created At 3/18/2017
Matchmaker for EZLBot.
~~Ignore my crappy code.~~
"""
queue_ = dict() #dict used during signup. So queue doesn't get mad when it finds an incomplete dict
queue = dict()  #dict to queue from || only completed values
heroes = ["Adagio","Alpha","Ardan","Baron","Blackfeather","Catherine","Celeste","Fortress","Glaive","Grumpjaw","Gwen","Idris","Joule","Kestrel","Koshka","Krul","Lance","Lyra","Ozo","Petal","Phinn","Reim","Ringo","Rona","Samuel","Saw","Skaarf","Skye","Taka","Vox"] #Taken from some guys npm package
skill_dict = {
     -1: ['Un-Ranked', 'http://i64.tinypic.com/30veur5.jpg'],
     0:  ['Just Beginning - B', 'http://i66.tinypic.com/spj77t.jpg'],
     1:  ['Just Beginning - S', 'http://i67.tinypic.com/24ct7qu.jpg'],
     2:  ['Just Beginning - G', 'http://i63.tinypic.com/14kytzl.jpg'],
     3:  ['Getting There - B', 'http://i66.tinypic.com/w8x5ci.jpg'],
     4:  ['Getting There - S', 'http://i65.tinypic.com/2rc3f39.jpg'],
     5:  ['Getting There - G', 'http://i66.tinypic.com/15guo43.jpg'],
     6:  ['Rock Solid - B', 'http://i63.tinypic.com/10zbkuw.jpg'],
     7:  ['Rock Solid - S', 'http://i64.tinypic.com/2igmao7.jpg'],
     8:  ['Rock Solid - G', 'http://i64.tinypic.com/m9ngpc.jpg'],
     9:  ['Worthy Foe - B', 'http://i63.tinypic.com/99jgg4.jpg'],
     10:  ['Worthy Foe - S', 'http://i64.tinypic.com/nnksv9.jpg'],
     11:  ['Worthy Foe - G', 'http://i68.tinypic.com/120kpk9.jpg'],
     12:  ['Got Swagger - B', 'http://i64.tinypic.com/4rxoid.jpg'],
     13:  ['Got Swagger - S', 'http://i68.tinypic.com/2lnib61.jpg'],
     14:  ['Got Swagger - G', 'http://i63.tinypic.com/oqjgau.jpg'],
     15:  ['Credible Threat - B', 'http://i65.tinypic.com/dphenn.jpg'],
     16:  ['Credible Threat - S', 'http://i66.tinypic.com/2dr9law.jpg'],
     17:  ['Credible Threat - G', 'http://i65.tinypic.com/20h6cti.jpg'],
     18:  ['The Hotness - B', 'http://i65.tinypic.com/288vxuc.jpg'],
     19:  ['The Hotness - S', 'http://i68.tinypic.com/2e3rby8.jpg'],
     20:  ['The Hotness - G', 'http://i68.tinypic.com/dq3meg.jpg'],
     21:  ['Simply Amazing - B', 'http://i65.tinypic.com/2hpm0d3.jpg'],
     22:  ['Simply Amazing - S', 'http://i66.tinypic.com/2b19ap.jpg'],
     23:  ['Simply Amazing - G', 'http://i65.tinypic.com/im5f13.jpg'],
     24:  ['Pinnacle of Awesome - B', 'http://i65.tinypic.com/vp8f8l.jpg'],
     25:  ['Pinnacle of Awesome - S', 'http://i68.tinypic.com/5wjhvs.jpg'],
     26:  ['Pinnacle of Awesome- G', 'http://i65.tinypic.com/10r7rrs.jpg'],
     27:  ['Vainglorious - B', 'http://i68.tinypic.com/27y8mdw.jpg'],
     28:  ['Vainglorious - S', 'http://i64.tinypic.com/1znqsds.jpg'],
     29:  ['Vainglorious - G', 'http://i65.tinypic.com/e6x74n.jpg']
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
} #real name ==> pretty name

reverse_match = {
"casual": "casual",
"blitz": "blitz_pvp_ranked",
"royale": "casual_aral",
"rank": "ranked",
"rank": "ranked",
"ranked": "ranked",
"br": "casual_aral",
"battle": "casual_aral"
}#pretty name ==> real name

quotes = ['To commend a player for their performance do $upvote @discordname', 'EZLKarma is our special karma built just for you!', 'Match Pts is how compatible you are!','To accept your match, press the check mark below.','Come talk to us at http://discord.me/EZLBot', 'You can block spammers with $block discordname'] #Quotes used at the footer

def getPlayer(match, ign):
    """
    Get's players stats from the match -specified by ign
    """
    for i in match.rosters[0].participants:
        if i.player.name == ign:
            return i
    for i in match.rosters[1].participants:
        if i.player.name == ign:
            return i

def getplayerEmbed(id): #Returns **one** embed. Used for the dm to the acceptee
            expand=True
            i = id
            try:
                q = queue[id]
            except:
                return Embed(title="ERROR 404: Player Not Found")
            try:
                diff = abs(q['tier'] - queue[i]['tier'])
            except:
                print(q, queue[i])
                diff = 0
            chance = 0
            if q['role'] != 'any' and queue[i]['role'] == q['role']:
                if expand:
                    chance -=3
                else:
                    chance -=2
            else:
                chance +=5
            if q['voice'] != queue[i]['voice'] and q['voice'] != 'Whatever Works':
                if expand:
                    chance-=2
                else:
                    chance -=1
            if q['gamemode'] != 'any' and q['gamemode'] != queue[i]['gamemode']:
                if expand:
                    chance-=3
                else:
                    chance -=1
            if diff > q['diff']*3 and diff > queue[i]['diff']*3: #Absolute value of tier diff
                if expand:
                    chance-=4
                else:
                    chance -=2
            if q['time'] != queue[i]['time'] and q['time'] != 'Whenever' and queue[i]['time']:
                if q['time_'] == 0 or queue[i]['time_'] ==0:
                    pass
                else:
                    chance -= abs(q['time_'] - q['time_'])
            else:
                chance +=2

            chance -= diff
            chance -= round(abs(q['level']-queue[i]['level'])*.8)
            chance -= abs(q['karma']-queue[i]['karma'])*3
            chance -= abs(q['afk']- queue[i]['afk'])
            chance -= abs(q['popularity'] - queue[i]['popularity'])
            try:
                blocked1 = queue[i]['blocked']
                del queue[i]['blocked']
            except:
                pass
            try:
                blocked2 = q['blocked']
                del q['blocked']
            except:
                pass
            chance += round(len(set(queue[i].values()) & set(q.values()))*2.2) #Similarity. Returns an int which can be used to compare their match %
            try:
                queue[i]['blocked'] = blocked1
            except:
                pass
            try:
                q['blocked'] = blocked2
            except:
                pass
            return(playerListEmbed([{'id':i, 'chance': chance}] , 1, 1))


def playerListEmbed(playerlist,page,num): #Generates an embed from the list of players
    if page ==0:
        return(Embed(title="Loading..."))
    playerlist = sorted(playerlist, key=lambda k: k['chance'], reverse=True)
    q = queue[playerlist[page-1]['id']] #returns list of keys
    player = playerlist[page-1]

    avatar = "http://www.vaingloryfire.com/images/wikibase/icon/heroes/"+random.choice(heroes)+".png"
    if player['chance'] in range(10,100):
        match_heat = 0xe22f2f
    elif player['chance'] in range(5,11):
        match_heat= 0xfc8523
    else:
        match_heat = 0xf7f431
    em = Embed(title= "Match #{}".format(str(page)), description='MatchPts: **{}**\nGameMode: **{}**\n{}\nLevel: **{}**\nEZLKarma: **{}**'.format(str(player['chance']), match_dict.get(q['gamemode'], 'Any'), skill_dict[q['tier']][0], q['level'],  (q['karma']*5) + q['popularity'], ), colour=match_heat)
    em.add_field(name = 'Playing Time:', value = q['time'])
    em.add_field(name = 'Favorite Role:', value = q['role'])
    em.add_field(name = 'Voice:', value = q['voice'])
    em.set_author(name=q['ign'], icon_url= avatar)
    em.set_footer(text=random.choice(quotes), icon_url= 'http://www.vaingloryfire.com/images/wikibase/icon/items/oakheart.png')
    return em


def storeQueue(): #Stores the queue
    with open("queue.pickle", "wb") as handle:
        pickle.dump(queue, handle, protocol=pickle.HIGHEST_PROTOCOL)

try: # loads the queue
    with open('queue.pickle', 'rb') as handle:
        queue = pickle.load(handle)
except:
    print("No queue Yet")

class Matchmaker():
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, error, ctx): #To explain the cooldown
        if isinstance(error, commands.errors.CommandOnCooldown):
            print(dir(error))
            await self.bot.send_message(ctx.message.channel, "Sorry, you can't do that for the next {} seconds.".format(int(error.retry_after)))

    async def on_reaction_add(self, reaction,user): #used for the menu
        if reaction.message.id in msgs.keys() and reaction.emoji == '➡' and msgs[reaction.message.id]['page'] < msgs[reaction.message.id]['num']:
            msg = reaction.message
            msgs[msg.id]['page'] += 1 #Dict used to store all messages that need to be checked for reaction changes
            page = msgs[msg.id]['page'] #Page the user is on
            await self.bot.edit_message(reaction.message, embed=playerListEmbed(msgs[msg.id]['list'],page,len(msgs[msg.id]['list'])))
        elif reaction.message.id in msgs.keys() and reaction.emoji == '⬅' and msgs[reaction.message.id]['page'] >1:
            msg = reaction.message
            msgs[msg.id]['page'] -= 1
            page = msgs[msg.id]['page']
            await self.bot.edit_message(reaction.message, embed=playerListEmbed(msgs[msg.id]['list'],page,len(msgs[msg.id]['list'])))
        elif reaction.message.id in msgs.keys() and reaction.emoji == '✅':
            msg = reaction.message
            page = msgs[msg.id]['page']
            playerlist = msgs[msg.id]['list']
            name = msg.embeds[0]['author']['name'] #Gets the name from the message embed
            page = next(index for (index, d) in enumerate(playerlist) if d["ign"] == name)+1
            match = await self.bot.get_user_info(msgs[msg.id]['list'][page-1]['id'])
            q = queue[playerlist[page-1]['id']]
            _user = queue[user.id]
            if q.get('blocked') is None: #Checks if user is blocked
                pass
            else:
                for i in q['blocked']:
                    if i == str(user):
                        await self.bot.send_message(user,"Sorry, you were blocked from contacting {}.".format(q['ign']))
                        return
            await self.bot.send_message(user, ":ok_hand:, I have notified {}. Please join https://discord.me/EZLBot to contact them. Or you can dm them at ".format(q['ign'] ) )
            await self.bot.send_message(user, str(match))
            await self.bot.send_message(match,content="Hey, you've been matched by {}. Here are the details. You can contact them at http://discord.me/EZLBot or dm them at {}. To remove yourself from the queue, type $dequeue".format(_user['ign'], str(user)) )
            await self.bot.send_message(match, embed=getplayerEmbed(user.id))
            del msgs[msg.id] #deletes the msg from the dict so it can't be controlled by reactions anymore

    async def on_reaction_remove(self, reaction,user):
        if reaction.message.id in msgs.keys() and reaction.emoji == '➡' and msgs[reaction.message.id]['page'] < msgs[reaction.message.id]['num']:
            msg = reaction.message
            msgs[msg.id]['page'] += 1
            page = msgs[msg.id]['page']
            await self.bot.edit_message(reaction.message, embed=playerListEmbed(msgs[msg.id]['list'],page,len(msgs[msg.id]['list'])))
        elif reaction.message.id in msgs.keys() and reaction.emoji == '⬅' and msgs[reaction.message.id]['page'] >1:
            msg = reaction.message
            msgs[msg.id]['page'] -= 1
            page = msgs[msg.id]['page']
            await self.bot.edit_message(reaction.message, embed=playerListEmbed(msgs[msg.id]['list'],page,len(msgs[msg.id]['list'])))

    @commands.cooldown(1, 5, BucketType.user)
    @commands.command(description='Signup for a matchmaker that puts Match.com to shame!', pass_context=True)
    async def vgtinder(self,ctx):
        """
        Used to signup for the queue:
        $vgtinder <ign> <region> ==> Reaction Menu
        Only in Private Messages
        """
        try:
            verifyd = verify.to_dict(ctx.message.author.id)
            ign = verifyd['ign']
            region = verifyd['region']
        except:
            await self.bot.say("Sorry, you must authorize your account with {}verify".format(self.bot.command_prefix[0]))
            return
        if not ctx.message.channel.is_private: #Makes sure channel is private
            await self.bot.say('Sorry. But this process must be done in a private message.')
            return
        if not verify.isauth(ctx.message.author.id, ign):
            try:
                check = verify.check(ctx.message.author.id)
                await self.bot.say('I verified your account.')
            except:
                await self.bot.say("Sorry, you must authorize your account with {}verify {} {}".format(self.bot.command_prefix[0], ign,region))
                return
        print(1)
        region = region.lower()
        print(2)
        if region == 'sea':
            region = 'sg'
        if region not in ['sg', 'na', 'eu', 'sa', 'ea'] or ign == '':
            return
        print(3)
        try:
            m = api.matches({"page[limit]": 50, "filter[playerNames]": ign, "filter[createdAt-start]": "2017-01-01T08:25:30Z", "sort": "-createdAt"}, region = region)
            m = sorted(m, key=lambda d: d.createdAt, reverse=True)#sorts  match
        except:
            if region == 'sg':
                region='sea'
            await self.bot.say('Couldn\'t find data for {} in {}.'.format(ign, region))
            return
        queue_[ctx.message.author.id]=dict() #queue_ so queue doesn't pull from in progress signups
        queue_[ctx.message.author.id]['ign'] = ign
        queue_[ctx.message.author.id]['region'] = region
        q = queue_[ctx.message.author.id]
        msg = await self.bot.say('Alright, do you want to voice with your teammates? Answer: \n:one: Yes\n\n:two: No\n\n:three: Doesn\'t Matter')
        await self.bot.add_reaction(msg, '\U00000031\U000020e3')
        await self.bot.add_reaction(msg, '\U00000032\U000020e3')
        await self.bot.add_reaction(msg, '\U00000033\U000020e3')
        res = await self.bot.wait_for_reaction(['1⃣', '2⃣', '3⃣'], message = msg, user = ctx.message.author, timeout=  600)
        if res.reaction.emoji == '1⃣':
            q['voice'] = 'Yes'
        elif res.reaction.emoji == '2⃣':
            q['voice'] = "No"
        else:
            q['voice'] = 'Whatever Works'

        msg = await self.bot.say('Ok :ok_hand:, what gamemode do you want to play? Answer:\n:one: Ranked\n\n:two: Casual\n\n:three: Blitz\n\n:four: Battle Royale\n\n:five: Any')
        await self.bot.add_reaction(msg, '\U00000031\U000020e3')
        await self.bot.add_reaction(msg, '\U00000032\U000020e3')
        await self.bot.add_reaction(msg, '\U00000033\U000020e3')
        await self.bot.add_reaction(msg, '\U00000034\U000020e3')
        await self.bot.add_reaction(msg, '\U00000035\U000020e3')
        res = await self.bot.wait_for_reaction(['1⃣', '2⃣', '3⃣', '4⃣', '5⃣'], message = msg, user = ctx.message.author, timeout=  600)
        if res.reaction.emoji == '1⃣':
            q['gamemode'] = 'ranked'
        elif res.reaction.emoji == '2⃣':
            q['gamemode'] = 'casual'
        elif res.reaction.emoji == '3⃣':
            q['gamemode'] = 'blitz_pvp_ranked'
        elif res.reaction.emoji == '4⃣':
            q['gamemode'] = 'casual_aral'
        else:
            q['gamemode'] = 'any'

        msg = await self.bot.say('Ok :ok_hand:, how flexible are you in terms of teammates? How wide do you want to look for teammates?  Answer:\n:one: 1 Tier\n\n:two: 2 Tiers\n\n:three: 3 Tiers\n\n:four: All')
        await self.bot.add_reaction(msg, '\U00000031\U000020e3')
        await self.bot.add_reaction(msg, '\U00000032\U000020e3')
        await self.bot.add_reaction(msg, '\U00000033\U000020e3')
        await self.bot.add_reaction(msg, '\U00000034\U000020e3')
        res = await self.bot.wait_for_reaction(['1⃣', '2⃣', '3⃣', '4⃣'], message = msg, user = ctx.message.author, timeout=  600)
        if res.reaction.emoji == '1⃣':
            q['diff'] = 1
        elif res.reaction.emoji == '2⃣':
            q['diff'] = 2
        elif res.reaction.emoji == '3⃣':
            q['diff'] = 3
        else:
            q['diff']= 10

        msg = await self.bot.say('Ok :ok_hand:, when do you like to play? Answer:\n:one: Morning\n\n:two: Afternoon\n\n:three: Evening\n\n:four: Night\n\n:five: Whenever')
        await self.bot.add_reaction(msg, '\U00000031\U000020e3')
        await self.bot.add_reaction(msg, '\U00000032\U000020e3')
        await self.bot.add_reaction(msg, '\U00000033\U000020e3')
        await self.bot.add_reaction(msg, '\U00000034\U000020e3')
        await self.bot.add_reaction(msg, '\U00000035\U000020e3')
        res = await self.bot.wait_for_reaction(['1⃣', '2⃣', '3⃣', '4⃣', '5⃣'], message = msg, user = ctx.message.author, timeout=  600)
        if res.reaction.emoji == '1⃣':
            q['time'] = 'Morning'
            q['time_'] = 1
        elif res.reaction.emoji == '2⃣':
            q['time'] = 'Afternoon'
            q['time_'] =  2
        elif res.reaction.emoji == '3⃣':
            q['time'] = 'Evening'
            q['time_'] = 3
        elif res.reaction.emoji == '4⃣':
            q['time'] = 'Night'
            q['time_'] = 4
        else:
            q['time'] = 'Whenever'
            q['time_'] = 0

        msg = await self.bot.say('Ok :ok_hand:, one last thing. What position are you looking to play?  Answer:\n:one: Captain\n\n:two: Jungler\n\n:three: Carry\n\n:four: Any')
        await self.bot.add_reaction(msg, '\U00000031\U000020e3')
        await self.bot.add_reaction(msg, '\U00000032\U000020e3')
        await self.bot.add_reaction(msg, '\U00000033\U000020e3')
        await self.bot.add_reaction(msg, '\U00000034\U000020e3')
        res = await self.bot.wait_for_reaction(['1⃣', '2⃣', '3⃣', '4⃣'], message = msg, user = ctx.message.author, timeout=  600)
        if res.reaction.emoji == '1⃣':
            q['role'] = 'Captain'
        elif res.reaction.emoji == '2⃣':
            q['role'] = 'Jungler'
        elif res.reaction.emoji == '3⃣':
            q['role'] = 'Carry'
        else:
            q['role'] = 'any'
        await self.bot.say('Awesome, you\'re ready now to start finding players, do {0}queue. To update your stats when your tier changes, or you change your mind. Just do {0}vgtinder again.'.format(self.bot.command_prefix[0]))
        p = getPlayer(m[0], ign)
        q['tier'] = p.stats['skillTier']
        q['karma'] = p.stats['karmaLevel']
        q['level'] = p.stats['level']
        q['afk'] = 0
        q['dead'] = False
        try:
            q['blocked'] = queue[ctx.message.author.id]['blocked'] #prevents people from resetting their account
        except:
            q['blocked'] = []
        try:
            q['popularity'] = queue[ctx.message.author.id]['popularity'] #prevents people from resetting their account
        except:
            q['popularity'] = 0
        for i in m:
            if getPlayer(i, ign).stats['wentAfk']:
                q['afk'] +=1
        queue[ctx.message.author.id] = q
        storeQueue()
        del q
    @commands.cooldown(1, 10, BucketType.user) #10 second cooldown.
    @commands.command(description="Shows you a list of players you might like to match with.", pass_context=True)
    async def queue(self,ctx,gamemode = '', expand=''):
        """
        Used to search for players:
        $queue <OPTIONAL gamemode> <OPTIONAL expand>
        expand: Expand the search queue. | True/Yes
        """
        if not ctx.message.channel.is_private:
            await self.bot.say('Sorry. But this process must be done in a private message.')
            return
        if expand != '':
            expand = False
        else:
            expand = True
        gamemode = reverse_match.get(gamemode.lower(),'')
        playerlist = []
        try:
            q = queue[ctx.message.author.id]
        except:
            await self.bot.say("Umm, this is awkward, but you're not in the queue.")
            return
        for i in queue.keys():
            if queue[i].get('dead', False): #Checks if user is in queue and has not used $dequeue
                continue
            if queue[i] == q:#Checks if user found themselves
                continue
            try:
                diff = abs(q['tier'] - queue[i]['tier'])
            except:
                print(q, queue[i])
                diff = 0
            chance = 0
            if queue[i]['region'] != q['region']:
                if expand:
                    continue
                else:
                    continue
            if q['role'] != 'any' and queue[i]['role'] == q['role']:
                if expand:
                    chance -=3
                else:
                    chance -=2
            else:
                chance +=5
            if q['voice'] != queue[i]['voice'] and q['voice'] != 'Whatever Works':
                if expand:
                    chance-=2
                else:
                    chance -=1
            if gamemode != queue[i]['gamemode'] and gamemode != '':
                continue
            elif q['gamemode'] != 'any' and q['gamemode'] != queue[i]['gamemode']:
                if expand:
                    chance-=3
                else:
                    chance -=1
            if diff > q['diff']*3 and diff > queue[i]['diff']*3: #Absolute value of tier diff
                if expand:
                    chance-=4
                else:
                    chance -=1
            if q['time'] != queue[i]['time'] and q['time'] != 'Whenever' and queue[i]['time']:
                if q['time_'] == 0 or queue[i]['time_'] ==0:
                    pass
                else:
                    chance -= abs(q['time_'] - q['time_'])
            else:
                chance +=2
            chance -= diff
            chance -= round(abs(q['level']-queue[i]['level'])*.8)
            chance -= abs(q['karma']-queue[i]['karma'])*3
            chance -= abs(q['afk']- queue[i]['afk'])
            chance -= abs(q['popularity'] - queue[i]['popularity'])
            try:
                blocked1 = queue[i]['blocked'] #Removes these lists so chance can add up the Similarity
                del queue[i]['blocked']
            except:
                pass
            try:
                blocked2 = q['blocked']#Removes these lists in the list so chance can add up the Similarity
                del q['blocked']
            except:
                pass
            chance += round(len(set(queue[i].values()) & set(q.values()))*2.8) #Similarity. Returns an int which can be used to compare their match %
            try:
                queue[i]['blocked'] = blocked1 #Adds the lists back
            except:
                pass
            try:
                q['blocked'] = blocked2 #adds the list back
            except:
                pass
            playerlist.append({'id':i, 'chance': chance, 'ign': queue[i]['ign']})
        try:
            playerlist[0] #Checks for even one match.
        except Exception as e:
            await self.bot.say('No matches found :(')
            return
        msg = await self.bot.say(embed = playerListEmbed(playerlist, page=1, num=len(playerlist)) )
        await self.bot.add_reaction(msg, '\U00002b05')
        await self.bot.add_reaction(msg, '\U00002705')
        await self.bot.add_reaction(msg, '\U000027a1')
        await asyncio.sleep(1)
        msgs[msg.id] = {'list': playerlist, 'page': 1, 'num': len(playerlist), 'author': ctx.message.author.id}
        await asyncio.sleep(300) #Used as a timeout
        try:
            del msgs[msg.id]
        except:
            pass


    @commands.command(pass_context=True, description='Removes you from the queue.')
    async def dequeue(self,ctx):
        """
        Used to remove yourself from the queue:
        $dequeue
        """

        try:
            queue[ctx.message.author.id]['dead'] = True #Instead of deleting, which resets popularity.
        except:
            await self.bot.say("You aren't in the queue :face_palm: Join it with {}vgtinder".format(self.bot.command_prefix[0]))
            return
        await self.bot.say("Ok, you've been removed from the queue.")

    @commands.cooldown(1, 10, BucketType.user)
    @commands.command(pass_context=True)
    async def block(self,ctx,tag): #Adds user to the blocked dict
        """
        Block other users by discordname:
        $block SpiesWithin#7398
        """
        try:
            blocked = queue[ctx.message.author.id]['blocked']
        except:
            queue[ctx.message.author.id]['blocked'] = []
            blocked = queue[ctx.message.author.id]['blocked']
        blocked.append(tag)
        await self.bot.say('Blocked {} :ok_hand:'.format(tag))
        storeQueue()

    @commands.command(pass_context=True)
    async def changemode(self,ctx): #Quick use to change the gamemode
        """
        Quickly change the gamemode:
        $changemode ==> Reaction Menu
        """
        try:
            q = queue[ctx.message.author.id]
        except:
            await self.bot.say("Sorry. I don't think you're in the queue.")
            return
        msg = await self.bot.say('What gamemode do you want to play? Answer:\n:one: Ranked\n\n:two: Casual\n\n:three: Blitz\n\n:four: Battle Royale\n\n:five: Any')
        await self.bot.add_reaction(msg, '\U00000031\U000020e3')
        await self.bot.add_reaction(msg, '\U00000032\U000020e3')
        await self.bot.add_reaction(msg, '\U00000033\U000020e3')
        await self.bot.add_reaction(msg, '\U00000034\U000020e3')
        await self.bot.add_reaction(msg, '\U00000035\U000020e3')
        asyncio.sleep(2)
        res = await self.bot.wait_for_reaction(['1⃣', '2⃣', '3⃣', '4⃣', '5⃣'], message = msg, user = ctx.message.author, timeout=  100)
        if res.reaction.emoji == '1⃣':
            q['gamemode'] = 'ranked'
        elif res.reaction.emoji == '2⃣':
            q['gamemode'] = 'casual'
        elif res.reaction.emoji == '3⃣':
            q['gamemode'] = 'blitz_pvp_ranked'
        elif res.reaction.emoji == '4⃣':
            q['gamemode'] = 'casual_aral'
        else:
            q['gamemode'] = 'any'
        storeQueue()



    @commands.cooldown(1, 10, BucketType.user)
    @commands.command(pass_context=True)#removes user from the blocked dict
    async def unblock(self,ctx,tag):
        """
        Used to unblock a user:
        $unblock SpiesWithin#7398
        """
        try:
            queue[ctx.message.author.id]['blocked'].remove(tag)
            await self.bot.say(":ok_hand: Done.")
        except:
            await self.bot.say("I couldn't find {} in your blocked list.".format(tag))
            storeQueue()

    @commands.command(pass_context=True)#Tells who is blocked
    async def blocked(self,ctx):
        """
        See who you have blocked:
        $blocked
        """
        notice = '**Blocked:**\n'
        for i in queue[ctx.message.author.id]['blocked']:
            notice+= '{},\n'.format(i)
        await self.bot.say(notice)


    @commands.cooldown(1,1800, BucketType.user)
    @commands.command(pass_context=True)
    async def upvote(self,ctx, ign):
        """
        Used to upvote a player:
        $upvote <ign>
        Can only be used once per 30 minutes on your latest match.
        """
        if ctx.message.author.id not in queue.keys():
            await self.bot.say("Ummm, you have to be in the queue for that.")
            return
        else:
            try:
                m = api.matches({"page[limit]": 1, "filter[playerNames]": queue[ctx.message.author.id]['ign'], "filter[createdAt-start]": "2017-01-01T08:25:30Z", "sort": "-createdAt"}, region = queue[ctx.message.author.id]['region'])
            except:
                await self.bot.say("Sorry couldn't find your most recent match:(.")
                return
            m= m[0]
            seconds_diff = (datetime.datetime.now() - dateutil.parser.parse(m.createdAt).replace(tzinfo=None)).seconds #difference from now till match time in seconds
            if seconds_diff > 2700: #Check if match is older than 45 minutes
                await self.bot.say('Sorry, but you have to upvote or downvote a player within 45 minutes of the match.')
                return
            for i in m.rosters:
                for k in i.participants:
                    if k.player.name == queue[ctx.message.author.id]['ign']:
                        team = i
                        break
        for i in team.participants:
            if i.player.name == ign:
                await self.bot.say("Sorry, couldn't find {} on your team in your **latest** match.".format(ign))
                return
        check = True
        for i in queue.keys():
            if queue[i]['ign'] == ign:
                player = queue[i]
                user = await self.bot.get_user_info(i)
                check = False
                break
        if check:
            await self.bot.say("ERROR 404: {} not found in queue.".format(ign))
            return
        player['popularity'] +=1
        await self.bot.send_message(user, "You've been upvoted by {}.".format(queue[ctx.message.author.id]['ign']))
        await self.bot.say("Done :ok_hand:! You can't upvote anyone else for the next 30 minutes.")
        storeQueue()

    @commands.cooldown(1,3600, BucketType.user)
    @commands.command(pass_context=True)
    async def downvote(self,ctx, ign):
        """
        Used to downvote players:
        $downvote <ign>
        Can only be used once per hour on your latest match.
        """
        if ctx.message.author.id not in queue.keys():
            await self.bot.say("Ummm, you have to be in the queue for that.")
            return
        else:
            try:
                m = api.matches({"page[limit]": 1, "filter[playerNames]": queue[ctx.message.author.id]['ign'], "filter[createdAt-start]": "2017-01-01T08:25:30Z", "sort": "-createdAt"}, region = queue[ctx.message.author.id]['region'])
            except:
                await self.bot.say("Sorry couldn't find your most recent match:(.")
                return
            m= m[0]
            seconds_diff = (datetime.datetime.now() - dateutil.parser.parse(m.createdAt).replace(tzinfo=None)).seconds
            if seconds_diff > 2700:
                await self.bot.say('Sorry, but you have to upvote or downvote a player within 45 minutes of the match.')
                return
            for i in m.rosters:
                for k in i.participants:
                    if k.player.name == queue[ctx.message.author.id]['ign']:
                        team = i
                        break
        for i in team.participants:
            if i.player.name == ign:
                await self.bot.say("Sorry, couldn't find {} in your **latest** match.".format(ign))
        check = True
        for i in queue.keys():
            if queue[i]['ign'] == ign:
                player = queue[i]
                check = False
                break
        if check:
            await self.bot.say("ERROR 404: {} not found.".format(ign))
            return
        player['popularity'] -=1
        await self.bot.say("Done :ok_hand:! You can't downvote anyone else for the next 30 minutes.")
        storeQueue()


def setup(bot):
    bot.add_cog(Matchmaker(bot))
