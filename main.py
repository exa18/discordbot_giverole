#!/bin/python3
#
#   GIVE/REMOVE role to users OR SHOW
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
#
# >

#	>> CLASS
#	Identify arguments given as mention
#
class getArgs:
	def __init__(self, ctx, args):
		self.users=[]
		self.roles=[]
		self.channels=[]
		self.guild=ctx.guild

		for a in args:
			# mention format <@12345678901234> cuts to @12345678901234
			s=str( a[1:-1] )
			p=s[0:1]
			# IF channel
			if p == "#":
				s=s[1:]
				e=self.guild.get_channel(int(s))
				self.channels.append(e)
			# IF role or user
			elif p == "@":
				s=s[1:]
				p=s[0:1]
				# Check second symbol IF true this is ROLE
				if p == "&":
					s=s[1:]
					e=self.guild.get_role(int(s))
					self.roles.append(e)
				else:
					e=self.guild.get_member(int(s))
					self.users.append(e)

# <
#
#	>> READY
#
@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name=helptxt))
#	>>
#
#	GIVE/ADD role/s to user/s
#
@bot.command(name='+')
async def giverole(ctx, *args):

	ga = getArgs(ctx, args)
	users = ga.users
	roles = ga.roles

	if roles:
		if users:
			for role in roles:
				i=0
				u=[]
				for user in users:
					if not role in user.roles:
						await user.add_roles(role)
						u.append(user.display_name)
						await asyncio.sleep(0)
						i+=1
			
				if i > 0:
					s=""
					if i>1:
						s="s"
					await ctx.send("...\n" + ", ".join(u) + "\nAdded **" + str(i) + "** user" + s + " to role **" + str(role.name) + "**!")
				else:
					await ctx.send("Role **" + str(role.name) + "** already given!")
		else:
			u=[]
			for role in roles:
				u.append(role.name)
			s=""
			if len(u)>1:
				s="s"
			await ctx.send("Provide user/s for role" + s + " **" + ", ".join(u) + "** to give!")
	else:
		await ctx.send("Provide role/s to give users !!!")
#	>>
#
#	REMOVE role from users
#	if arg USERS is empty search in all
#
@bot.command(name='-')
async def removerole(ctx, *args):

	ga = getArgs(ctx, args)
	users = ga.users
	roles = ga.roles
	
	if not users:
		users = ctx.guild.members

	if roles:
		for role in roles:
			i=0
			u=[]
			for user in users:
				if role in user.roles:
					await user.remove_roles(role)
					u.append(user.display_name)
					await asyncio.sleep(0)
					i+=1

			if i > 0:
				s=""
				if i>1:
					s="s"
				await ctx.send("...\n" + ", ".join(u) + "\nRemoved role **" + str(role.name) + "** from **" + str(i) + "** user" + s + "!")
			else:
				await ctx.send("Role **" + str(role.name) + "** already empty!")
	else:
		await ctx.send("Provide role/s to remove from user/s !!!")
#	>>
#
#	SHOW useres assigned to role
#
@bot.command(name='s')
async def showrole(ctx, *roles: discord.Role):
	users = ctx.guild.members

	if roles:
		for role in roles:
			i=0
			u=[]
			for user in users:
				if role in user.roles:
					u.append(user.display_name)
					i+=1
		
			if i > 0:
				u.sort(key=str.lower)
				await ctx.send("...\n" + "\n".join(u) + "\nAssigned **" + str(i) + "** users to role **" + str(role.name) + "**!")
			else:
				await ctx.send("Role **" + str(role.name) + "** is empty!"+info)
	else:
		await ctx.send("Provide role/s to list !")
#	>>
#
#	HELP
#
@bot.command(name='?')
async def help(ctx):
	h = ("\n** **\n\n**Simple bot to give/remove ROLE** for selected users." \
	+ " Argumets could be given in any order.\n\n--- ADD\n"
	+ PREFIX +"+ @role (or more)... @user (or more) -> give role to users \n\n--- REMOVE\n" \
	+ PREFIX +"- @role (or more)... [@user (or more)] -> remove role from all or selected users\n\n--- SHOW\n" \
	+ PREFIX +"s @role (or more)... -> show users assigned to role\n\n" \
	+ "\nEnjoy!\n"
	)
	await ctx.send(h)
	await asyncio.sleep(0)
#
#	>> RUN it
#
bot.run(getenv('TOKEN'))