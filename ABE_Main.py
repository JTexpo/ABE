import discord
from discord.ext import commands
import asyncio

import Utils

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="?",case_insensitive=True,intents=intents)

@bot.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    for server in bot.guilds:
        print(server.name)
        print(server.id)
        print('------')
    await bot.change_presence(activity=discord.CustomActivity(name = "?help"))

if __name__ == '__main__':
    #bot.remove_command("help")
    extensions = ['Monitor']
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print('Loaded {}'.format(extension))
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension,error))

@commands.command(name = "load")
@Utils.is_JTexpo()
async def load(ctx, extension = ''):
    if extension == '':
        await ctx.send("Please Give A Valid Cog")
    try:
        bot.load_extension(extension)
        await ctx.send('Loaded {}'.format(extension))
    except Exception as error:
        await ctx.send('{} cannot be loaded. [{}]'.format(extension,error))
bot.add_command(load)

@commands.command(name = "unload")
@Utils.is_JTexpo()
async def unload(ctx, extension = ''):
    if extension == '':
        await ctx.send("Please Give A Valid Cog")
    try:
        bot.unload_extension(extension)
        await ctx.send('Unloaded {}'.format(extension))
    except Exception as error:
        await ctx.send('{} cannot be unloaded. [{}]'.format(extension,error))
bot.add_command(unload)

@commands.command(name = "reload")
@Utils.is_JTexpo()
async def reload(ctx, extension = ''):
    if extension == '':
        await ctx.send("Please Give A Valid Cog")
    try:
        bot.unload_extension(extension)
        bot.load_extension(extension)
        await ctx.send('Reloaded {}'.format(extension))
    except Exception as error:
        await ctx.send('{} cannot be reloaded. [{}]'.format(extension,error))
bot.add_command(reload)

@commands.command(name = 'logout')
@Utils.is_JTexpo()
async def logout (ctx):
    await ctx.message.channel.send("Offline...")
    await bot.logout()
bot.add_command(logout)

bot.run(Utils.TOKEN)