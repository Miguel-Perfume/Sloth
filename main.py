import discord, os, re
from discord.ext import commands
from dotenv import load_dotenv
from random import randint


customStatus = discord.Game("and sleeping")


load_dotenv(os.path.join(os.path.dirname(__file__), 'token.env'))

TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix = "?", case_insensitive = True)


@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.online, activity = customStatus)
    print("Connection Successful\n")
    print(f"Bot: {bot.user}")
    print(f"Discord Version: {discord.__version__}")


@bot.command()
async def ping(ctx):
    await ctx.send("WIP\nPong! :ping_pong:")


@bot.command(aliases = ["r", "rolls"])
async def roll(ctx, *, d):
    diceRegex = re.compile(r"^(\d*)d(\d+)((-|\+)\d+)?$", re.IGNORECASE)
    dado = diceRegex.search(d)

    colorRange = {0: 0xee0000, 1: 0xee2800, 2: 0xee5900, 3: 0xee8b00, 4: 0xeebc00, 5: 0xeeee00, 6: 0xcaf300, 7: 0xa2f800, 8: 0x77fc00, 9: 0x49ff00, 10: 0x18ff00} 
    
    numDados = int(dado[1]) if dado[1] else 1
    numLados = int(dado[2])
    numRodadas = [randint(1, numLados) for i in range(numDados)]

    valor = (sum(numRodadas) * 10) / (numDados * numLados)

    name = f"[{numDados}d{numLados} {sorted(numRodadas)} "
    total = f"{sum(numRodadas)}"
   
    if dado[3]:
        modificador = [i if i not in "+-" else f"{i} " for i in dado[3]]
        name += "".join(modificador)
        total += str(dado[3])

    cor = colorRange[round(valor)]

    embedVar = discord.Embed(title=":game_die: Rolando Dados :game_die: ", color=cor)
    embedVar.add_field(name = name, value = f"O resultado final foi: {eval(total)}", inline=False)
    
    await ctx.send(embed = embedVar)


@bot.command()
async def prefix(ctx, prefix):
    bot.command_prefix = prefix
    await ctx.send(f"WIP\nPrefix changed to: **{bot.command_prefix}**")


@bot.command()
async def svinfo(ctx):
    await ctx.send(f"""WIP
{ctx.guild.id}""")


@bot.command()
async def clear(ctx, ammount):
    if ammount == "all":
        await ctx.send("Apagar todas as mensagens pode demorar um pouco e deixar o chat inutilizavel durante esse período.\nDeseja mesmo continuar?")

        def check(m):
            return bool(m)

        resp = await bot.wait_for("message", check = check)

        if resp.content.lower() in "simyes":
            ammount = 100000

    else:
        ammount = int(ammount)

    deleted = await ctx.channel.purge(limit = ammount)
    await ctx.send(f"**Foram apagadas {len(deleted)} mensagens.**")


bot.run(TOKEN)