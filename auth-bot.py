from discord.ext import commands
import verify
import asyncio

class Verification():
    def __init__(self, bot):
        self.bot = bot
    @commands.command(pass_context=True)
    async def verify(self,ctx,ign='',region=''):
        """
        Used to verify your account.
        $verify SpiesWithin na
        """
        if ign =='' or region =='':
            await self.bot.say("Please type in a ign and region.")
            return
        if not ctx.message.channel.is_private: #Makes sure channel is private
            await self.bot.say('Sorry. But this process must be done in a private message, to continue please dm the bot ```{}```'.format(ctx.message.content))
            return
        try:
            pattern = verify.start(ctx.message.author.id, ign,region)
        except Exception as e:
            await self.bot.say('Error: ' + str(e)+'\n\nJoin http://discord.me for more info.')
            return
        pattern_ = '{} Halcyon Potions, {} Weapon Infusions, and {} Crystal Infusions'.format(str(pattern.count(0)), str(pattern.count(1)), str(pattern.count(2)))
        await self.bot.say("Awesome. To complete the authorization process.\n• Enter a **blitz** match\n• Buy **{}** for your first {} items.\n• You can sell them immediately.\n• This must be your next match.\n• **Once you are done please type {}check to complete authorization process.** Once this is done, your account will be linked and authenticated permanantly.".format(pattern_,len(pattern), self.bot.command_prefix[0]))
        asyncio.sleep(345)
        await self.bot.send_message(ctx.message.author, verify.check(ctx.message.author.id))
    @commands.command(pass_context=True)
    async def check(self,ctx):
        """
        Check for your latest match to verify
        $check
        """
        try:
            check = verify.check(ctx.message.author.id)
        except Exception as e:
            await self.bot.say('Error: ' +str(e)+'\n\nIf your match hasn\'t registered yet, wait 5-10 minutes or check http://discord.me/EZLBot for updates. Else, signup again with {}verify <ign> <region>'.format(self.bot.command_prefix[0]))
            return
        await self.bot.say("OK. {}. You can now enter the matchmaker with {}vgtinder to find people to party with.".format(check,self.bot.command_prefix[0]))


def setup(bot):
    bot.add_cog(Verification(bot))
