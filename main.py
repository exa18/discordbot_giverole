#!/bin/python3

import discord
import asyncio

from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

intents = discord.Intents.default()
intents.members = True

load_dotenv()

bot = commands.Bot(command_prefix='!r', intents=intents)
#@commands.has_permissions(manage_roles=True)
#
#
#	GIVE/ADD role to users
#
#
@bot.command(name='+')
async def giverole(ctx, role: discord.Role, *users: discord.Member):
	i=0
	for user in users:
		await user.add_roles(role)
		await ctx.send("+ " + user.name)
		await asyncio.sleep(0)
		i+=1
	await ctx.send("Added **" + str(i) + "** users to role **" + str(role) + "**!")
#
#
#	REMOVE role from users
#	if arg USERS is empty search in all
#
#
@bot.command(name='-')
async def removerole(ctx, role: discord.Role, *users: discord.Member):
	if not users:
		users = bot.get_all_members()
	
	i=0
	for user in users:
		if role in user.roles:
			await user.remove_roles(role)
			await ctx.send("- " + user.name)
			await asyncio.sleep(0)
			i+=1
	await ctx.send("Removed role **" + str(role) + "** from **" + str(i) + "** users!")
#
#	HELP
#
@bot.command(name='?')
async def help(ctx):
	h = ("\n** **\n\nSimple bot to give or remove ROLE for selected users.\n\n" \
	"!r+ @ROLE @user1 @user2 ... @user11 -> will give role to users \n" \
	"!r- @ROLE [@user1 @user2 ... @user11] -> will remove it\n\nEnjoy!\n" 
	)
	await ctx.send(h)
	await asyncio.sleep(0)
#
#	RUN it
#
bot.run(getenv('TOKEN'))