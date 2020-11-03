from discord.ext import commands


class User:
    def __init__(self, ctx):
        self.name = ctx.author.name
        self.idp = ctx.author.id
        self.last_message = ctx.created_at
        self.rate = 0
        self.falls = 0
        self.banned = False

    def message_rate(self, ctx):
        mentions = ctx.mentions
        mention = 0
        if len(mentions) > 0:
            mention = 3

        score = 0
        if ctx.content[0] == '!':
            score = 0.5

        self.rate += 1+mention-score
        return 1.5+mention-score

    def set_rate(self, score, delta):
        self.rate += score/(int(delta.seconds)+int(delta.microseconds)/1000) - delta.seconds

        if self.rate < 0:
            self.rate = 0

        return self.rate


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.users = {}

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.bot.user:
            return

        if ctx.author.id in self.users:
            delta = ctx.created_at - self.users[ctx.author.id].last_message
            rate = self.users[ctx.author.id].message_rate(ctx)
            self.users[ctx.author.id].last_message = ctx.created_at
            score = self.users[ctx.author.id].set_rate(rate, delta)

            if self.users[ctx.author.id].falls == 3:
                await self.bot.kick(ctx.author.name)

            if int(delta.seconds) > 10:
                self.users[ctx.author.id].banned = False
                self.users[ctx.author.id].rate = 0
                return

            if self.users[ctx.author.id].banned:
                await ctx.delete()
                return

            if score > 10:
                self.users[ctx.author.id].banned = True
                self.users[ctx.author.id].falls += 1
                await ctx.delete()
                if self.users[ctx.author.id].falls == 1:
                    await ctx.channel.send('{}, can you stop spamming? You have 1 fall'.format(ctx.author))
                elif self.users[ctx.author.id].falls == 2:
                    await ctx.channel.send('{}, can you stop spamming? You have 2 falls, if you write something, you will be kicked.'.format(ctx.author))
        else:
            self.users[ctx.author.id] = User(ctx)


def setup(bot):
    bot.add_cog(Admin(bot))
