import discord
from discord.ext import commands
import asyncio

import Utils

import sklearn

class Monitor(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    async def check_for_bullying(self,ctx):
        if not Utils.in_server(ctx): return
        if Utils.ignor_users(ctx): return

        text = Utils.tokenize_text(ctx.content)
        x_data = [0]*5
        total_score = 0

        flagged = []

        if len(text) == 1: return 

        for i in range(len(text)):
            pred = Utils.ABE_BRAIN.predict_proba([x_data])[0]
            if i == 0: pred = [0,0]
            x_data[3] = pred[0]
            x_data[4] = pred[1]

            if text[i] in Utils.FLAGGED_WORDS:
                total_score += Utils.BAD_WEIGHT
                x_data[0] = Utils.BAD_WEIGHT
                x_data[1] += 1

                flagged.append(text[i])
            else : 
                total_score -= Utils.GOOD_WEIGHT
                x_data[0] = -1 * Utils.GOOD_WEIGHT
            x_data[2] = total_score

        if not Utils.ABE_BRAIN.predict([x_data]): return

        possible_false_positives = ['you','youre','your','yourself','u','ur','urself','ya','yeah','gonna','go','yo']
        advance_list = [word for word in flagged if word not in possible_false_positives ]
        if len(advance_list) == 0: return

        conf = Utils.ABE_BRAIN.predict_proba([x_data])[0]

        report_message = f"""**__Message :__** {ctx.content}

[click here]({ctx.jump_url})
        """
        embd = discord.Embed(title = "Please React 🚨 If There Is Harassement",
                description = report_message,
                colour = (0xFD6A02))
        embd.add_field(name = "Confidence of Bullying :", value = f"{int(100 * conf[1])}%", inline = True)
        embd.add_field(name = "Channel :", value = f"{ctx.channel.mention}", inline = True)
        embd.add_field(name = "Author :", value = f"{ctx.author.mention}", inline = True)
        embd.add_field(name = "Flagged Words :", value = f"{' , '.join(flagged)}", inline = False)
        mychn = self.bot.get_channel(826442249276882964)
        if conf[1] >= .75:
            await mychn.send('<@&826442502474956831>')
        msg = await mychn.send(embed = embd)
        await msg.add_reaction("🚨")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        await self.check_for_bullying(ctx)
    
    @commands.Cog.listener()
    async def on_message_edit(self, ctx2, ctx):
        await self.check_for_bullying(ctx)

    @commands.Cog.listener()
    async def on_reaction_add(self, ctx, user):
        mychn = self.bot.get_channel(826442249276882964)
        if ctx.message.channel.id != mychn.id : return
        if ctx.emoji == "🚨" and ctx.count == 3:
            users = ''
            async for user in ctx.message.reactions[0].users():
                users += f'{user.mention} '
            embd = discord.Embed(
                    title = "A Message Was Voted As Harassement",
                    description = f"**__Reported By__** :\n{users}\n\nClick Here To Read For Yourself : [Link]({ctx.message.jump_url})",
                    colour = (0x10A5F5)
                    )
            await mychn.send('<@&566343161929007124>')
            await mychn.send(embed = embd)


def setup(bot):
    bot.add_cog(Monitor(bot))