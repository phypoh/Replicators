from discord.ext import commands

"""
For general commands which don't fit into other categories. i.e. Set Default IGN.
"""
class Misc():
    def __init__(self, bot):
        self.bot = bot

    @commands.command() #Example
    async def roll(self, dice : str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await self.bot.say('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.bot.say(result)

    @commands.command(description='For when you wanna settle the score some other way') #Example
    async def choose(self, *choices : str):
        """Chooses between multiple choices."""
        await self.bot.say(random.choice(choices))


def setup(bot):
    bot.add_cog(Misc(bot))
