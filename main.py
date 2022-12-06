#!/bin/python3
#
#   GIVE/REMOVE role from users
#
#
import discord
import asyncio

from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

intents = discord.Intents.all()
intents.members = True

load_dotenv()

PREFIX = '!r'
helptxt = "Help: "+PREFIX+"?"
#
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
#
@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name=helptxt))
#
#
#	GIVE/ADD role to users
#
#
@bot.command(name='+')
async def giverole(ctx, role: discord.Role, *users: discord.Member):
	i=0
	if users:
		u=[]
		for user in users:
			if not role in user.roles:
				await user.add_roles(role)
				u.append(user.name)
				await asyncio.sleep(0)
				i+=1

		if i > 0:
			await ctx.send("...\n" + ", ".join(u) + "\nAdded **" + str(i) + "** users to role **" + str(role) + "**!")
		else:
			await ctx.send("Role **" + str(role) + "** already given!")
	else:
		await ctx.send("Provide users for role **" + str(role) + "** to give!")
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
	u=[]
	for user in users:
		if role in user.roles:
			await user.remove_roles(role)
			u.append(user.name)
			await asyncio.sleep(0)
			i+=1
	
	if i > 0:
		await ctx.send("...\n" + ", ".join(u) + "\nRemoved role **" + str(role) + "** from **" + str(i) + "** users!")
	else:
		await ctx.send("Role **" + str(role) + "** already empty!")
#
#
#	SHOW useres assigned to role
#
#
@bot.command(name='s')
async def showrole(ctx, role: discord.Role):
	users = bot.get_all_members()
	i=0
	u=[]
	for user in users:
		if role in user.roles:
			u.append(user.name)
			i+=1

	if i > 0:
		u.sort(key=str.lower)
		await ctx.send("...\n" + "\n".join(u) + "\nAssigned **" + str(i) + "** users to role **" + str(role) + "**!")
	else:
		await ctx.send("Role **" + str(role) + "** is empty!"+info)
#
#	HELP
#
@bot.command(name='?')
async def help(ctx):
	h = ("\n** **\n\n**Simple bot to give or remove ROLE** for selected users.\n\n" \
	+ PREFIX +"+ @ROLE @user1 @user2 ... @user11 -> will give role to users \n" \
	+ PREFIX +"- @ROLE [@user1 @user2 ... @user11] -> will remove it\n" \
	+ PREFIX +"s @ROLE -> show users assigned also current counter\n" \
	+ "\nEnjoy!\n"
	)
	await ctx.send(h)
	await asyncio.sleep(0)
#
#	RUN it
#
bot.run(getenv('TOKEN'))