import os
import discord
from dotenv import load_dotenv

from discord.ext import commands
import requests

# helpers
from helpers.dataProcessing import saveDataToJson

load_dotenv()
TOKEN_BOT = os.getenv("TOKEN_BOT")

bot = commands.Bot(command_prefix="!", description="A bot for the Discord server.")


@bot.command()
async def q(ctx, *, question):
    """
    Ask a question to the bot and get the answer.
    """
    pass


@bot.command()
async def exams(ctx):
    """
    Get the exams of the day.
    """
    exam_list = []

    # ver todos los archivos de la carpeta exams y extraer los nombres
    try:
        exams = os.listdir("src/exam")

        if len(exams) > 0:
            exams = [exam.split(".")[0] for exam in exams]

            for exam in exams:
                exam_list.append(f"{exam}\n")

            embed = discord.Embed(
                title=f"{ctx.guild.name}",
                description="Etos son los nombres de los examenes que estan disponibles, recuerda usar !aw nombreExamen pregunta, para poder ver las respuestas registradas",
                timestamp=ctx.message.created_at,
                color=discord.Color.gold(),
            )
            embed.add_field(
                name="Examenes disponibles",
                value="\n".join(exam_list),
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("No hay examenes para mostrar")
    except FileNotFoundError:
        await ctx.send("No se han añadido examenes")


# comandos
@bot.command()
async def addExam(ctx):
    if ctx.author.guild_permissions.administrator:
        try:
            files = ctx.message.attachments

            file = files[0]

            if (
                len(files) == 1
                and file.filename.endswith(".json")
                and file.size <= 1000000
            ):
                req = requests.get(file.url)

                saveDataToJson(file.filename, req.json())

                await ctx.send(f"{file.filename} Guardado!")
            elif len(ctx.message.attachments) > 1:
                await ctx.send("Solo se puede subir un archivo por mensaje")
                await ctx.message.delete()

            else:
                await ctx.send("El archivo tiene que ser un JSON valido :)")
                await ctx.message.delete()

        except IndexError:
            await ctx.send("No se ha adjuntado ningun archivo")
            await ctx.message.delete()

    else:
        await ctx.send("No tienes permisos para usar este comando")
        await ctx.message.delete()


if __name__ == "__main__":

    # eventos
    @bot.event
    async def on_ready():
        print(f"{bot.user} has connected to Discord!")

    @bot.command()
    async def info(ctx):
        embed = discord.Embed(
            title=f"{ctx.guild.name}",
            description="Hola, soy el bot para tus respuestas de examenes. Empieza a agregar un JSON con la información",
            timestamp=ctx.message.created_at,
            color=discord.Color.red(),
        )
        embed.add_field(
            name="Comandos",
            value="!addExam \n!delete \n!lis\n!help\n!exams",
        )
        await ctx.send(embed=embed)

    """@bot.listen()
    async def on_message(message):
        if "prueba" in message.content.lower():
            await message.channel.send(
                "Hola, soy el bot para tus respuesas de examenes"
            )
            await bot.process_commands(message)"""

    bot.run(TOKEN_BOT)
