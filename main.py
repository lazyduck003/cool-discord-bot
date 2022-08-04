import os
import discord 
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from itertools import cycle

	
client = commands.Bot(command_prefix='>')
#intents = discord.Intents.all()

status = cycle(['Status1', 'Status2'])


######################################################
#events 



@client.event    #when bot is online
async def on_ready():
	change_status.start()
	print("Logged in as {0.user}".format(client))


@client.event   #when someone joins
async def on_member_join(member):
	print(f"{member} has joined.")

@client.event  #when a member gets kicked or banned or leaves server
async def on_member_remove(member):
	print(f"print {member} is no longer in the sever.")

@client.event #when there is error with a command
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Please pass in all required arguments.")



#events
############################################################
#commands

		

@client.command(aliases=['latency'])    #check ping command
async def ping(ctx): #name the function the name of the command, ctx (context) is a parameter already passed in by default
	await ctx.send(f"{client.latency * 1000}ms")

@client.command()  #clear messages command
@has_permissions(administrator=True)
async def clear(ctx, amount : int): #amount is amount of messages to delete
		await ctx.channel.purge(limit=amount+1)


@client.command()    #kick command
@has_permissions(administrator=True)
async def kick(ctx, member : commands.MemberConverter, *, reason=None):
		await member.kick(reason=reason)

@client.command()   #ban command
@has_permissions(administrator=True)
async def ban(ctx, member : commands.MemberConverter, *, reason=None):
		await member.ban(reason=reason)
		await ctx.send(f"**Banned {member.mention}**")

@client.command()
@has_permissions(administrator=True)
async def unban(ctx, *, member):
	banned_users = ctx.guild.bans()
	member_name, member_discriminator = member.split('#')
	for ban_entry in banned_users:
		user = ban_entry.user
		if (user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
			await ctx.send(f"**Unbanned {user.mention}**")
			return


@client.command()
async def helpp(ctx):
    embed = discord.Embed(
			title="Help",
			description="description",
			color=0xFF5733)
    await ctx.send(embed=embed)

@client.command()
async def online(ctx):
	await ctx.send("im online")

@client.command()
async def join(ctx):
	channel = ctx.author.voice.channel
	await channel.connect()


@client.command()
async def leave(ctx):
	print("leave command")
	await ctx.guild.voice_client.disconnect()

	
#commands
####################################################################




@tasks.loop(seconds=10) #loop task to change status every 10 seconds
async def change_status():
	await client.change_presence(activity=discord.Game(next(status)))
	#await client.change_presence(activity=discord.Game(name="Watching You"))
	

@clear.error  #error with clear command
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		ctx.send("Specify how many messages to delete.")







#others
#################################################################

token = os.environ['token']  #create an env file with ur token
client.run(token)
