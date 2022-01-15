#House mods(Bot), Bot de moderação & etc da hm!

import asyncio
import os
from asyncio import tasks
import discord
from discord.ext import commands

#Bot começando daqui

#Prefixo

client = commands.Bot(command_prefix=";")

bot = commands.Bot(command_prefix=";")

#Mostra isso no terminal caso o bot esteja funcionando

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

#Output de erro caso o usuario não tenha permissões o suficiente, ou o comando falta argumentos

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Erro de "MissingRequiredArgument" Algo ai não está certo!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Erro de MissingPermissions Você não tem as permissoẽs nescessarias")

#Comando especial pro jefersu

@bot.command("jeferson")
async def hello(ctx):
    await ctx.send("é gay")

#Comando de estado, normalmente usado para verificar se o bot está funcionando como deveria

@bot.command("estado")
async def hello(ctx):
    await ctx.send("Funcionando")

#Alternativa a o comando de estado

@bot.command("e1")
async def hello(ctx):
    await ctx.send("Funcionando")

#Comando de ping

@bot.command("ping")
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))

#Comando de help

@bot.command("ajuda")
async def hello(ctx):
    await ctx.send(f'Ola! Meus comandos São: Geral: e1, ajuda(este), ping, estado. Moderação: Clean, Kick, Ban, Unban')

#Comando de ban
@bot.command(name="ban", aliases=["banir","deumole","vaipracasadokrl"])
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("Falta argumentos! Usuario a ser banido = autor & etc")
        print("Ban self")
        return
    if reason == None:
        reason = "Descumprimento de regras ou TOS"

    await member.ban(reason = reason)
    print("ban realizado")
    await ctx.send("Banido!")

#Comando de unban

@bot.command(name="unban", aliases=["desbanir","pardon","taperdoadomeuparceiro"])
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Desbanido')
            print("Unban realizado")
            return

#Comando de kick

@bot.command(name="kick", aliases=["expulsar","deumenosmole","kickar"])
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason = None):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("Falta argumentos! Usuario a ser expulso = autor & etc")
        print("Kick self")
        return
    if reason == None:
        reason = "Descumprimento de regras ou TOS"

    await member.kick(reason = reason)
    print("kick realizado")
    await ctx.send("Expulso!")

#Comando de clear

@bot.command("clear")
@commands.has_permissions(manage_messages = True)
async def clear(ctx , amount=5):
  await ctx.channel.purge(limit=amount + 1)

#Comando de lock & unlock

@bot.command("lock")
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role,send_messages=False)
    await ctx.send( ctx.channel.mention + " Canal fechado")

@bot.command("unlock")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + " Canal aberto!")

#Comando de timeout por enquanto instavel

#-----------------------------------------

#Comando de avatar

@bot.command(name="avatar", aliases=["foto","perfil","roubarfoto"])
async def dp(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    userAvatar = member.avatar_url
    await ctx.send(userAvatar)

#Comando de about

@bot.command("about")
async def server(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=name + " Info",
        description="Info do server!!!",
        color=discord.Color.blurple()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="ID do server", value=id, inline=True)
    embed.add_field(name="Membros", value=memberCount, inline=True)

    await ctx.send(embed=embed)

#RPC

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Dsc.gg/housemods"))

#Comando de mute

@bot.command("mute")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, mute_time : int, *, reason=None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    await ctx.send(f'Mutado, duração: {mute_time}segundos')

    await asyncio.sleep(mute_time)
    await member.remove_roles(role)
    await ctx.send(f"Desmutado {member.mention}")


#Token

bot.run("seu token aqui!")
print("bot.run realizado")