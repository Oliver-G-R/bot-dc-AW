import os
import discord
from dotenv import load_dotenv

from discord.ext import commands
import requests

# helpers
from helpers.dataProcessing import save_to_json

load_dotenv()
TOKEN_BOT = os.getenv("TOKEN_BOT")

bot = commands.Bot(command_prefix="!", description="A bot for the Discord server.")


# eventos
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


# comandos
@bot.command()
async def addExam(ctx):
    """
    Get file attached to a message
    """

    try:
        files = ctx.message.attachments

        file = files[0]

        if len(files) == 1 and file.filename.endswith(".json") and file.size <= 1000000:
            req = requests.get(file.url)

            save_to_json(file.filename, req.json())

            await ctx.send(f"{file.filename} Guardado!")
        elif len(ctx.message.attachments) > 1:
            await ctx.send("Solo se puede subir un archivo por mensaje")
        else:
            await ctx.send("El archivo tiene que ser un JSON valido :)")
    except IndexError:
        await ctx.send("No se ha adjuntado ningun archivo")


if __name__ == "__main__":

    @bot.command()
    async def info(ctx):
        embed = discord.Embed(
            title=f"{ctx.guild.name}",
            description="Hola, soy el bot para tus respuestas de examenes. Empieza a agregar un JSON con la información",
            timestamp=ctx.message.created_at,
            color=discord.Color.dark_blue(),
        )
        embed.add_field(
            name="Comandos",
            value="!addExam \n!delete \n!lis\n!help",
        )
        embed.set_footer(text="Bot creado por @OliverGR")
        await ctx.send(embed=embed)

    """@bot.listen()
    async def on_message(message):
        if "prueba" in message.content.lower():
            await message.channel.send(
                "Hola, soy el bot para tus respuesas de examenes"
            )
            await bot.process_commands(message)"""

    bot.run(TOKEN_BOT)
