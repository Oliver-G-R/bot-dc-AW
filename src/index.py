import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import requests

# helpers
from helpers.dataProcessing import getJson, saveDataToJson

load_dotenv()
TOKEN_BOT = os.getenv("TOKEN_BOT")

bot = commands.Bot(command_prefix="!", description="A bot for the Discord server.")
bot.remove_command("help")

def getPermissions(roles, permissionAdmin):
    for role in roles:
        if role.name == "pb🤖" or permissionAdmin:
            return True
    return False

'''
Comando que capture el comando exam y que capture la pregunta completa 
y la guarde en un archivo json.
'''
@bot.command(name="aw")
async def answerExam(ctx, ex, question): 
    """
    ​    Responde las preguntas que esten en el examen.
    ​    Uso: !aw <examen> <pregunta> (public)
    """
    roles = ctx.author.roles
    permissionsAdmin = ctx.author.guild_permissions.administrator

    if getPermissions(roles, permissionsAdmin):
        if ex is not None or question is not None:
            questionsJSON = getJson(ex.lower())
            if len(questionsJSON) > 0:
                for qu in questionsJSON:
                    if question.lower() in qu["question"] and len(question) >= 4:
                        await ctx.send(f"**{qu['question'].upper()}**")
                        for answer in qu["answers"]:
                            await ctx.send(answer)
            else:
                await ctx.send(f"No se encontro el nombre del examen **{ex}** seleccionado, usa !aw nombreExamen pregunta")
        elif question is None:
            await ctx.send("Falto la pregunta")
        else:
            await ctx.send("Escribe los parametros disponibles")
    else:
        await ctx.send("No tienes permisos para usar este comando")


# Lista todos los archivos json de los examnes disponibles
@bot.command()
async def exams(ctx):
    """
    Obtiene el listado de examenes disponibles (public)
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
                description="Estos son los nombres de los examenes que estan disponibles, recuerda usar !aw nombreExamen pregunta, para poder ver las respuestas registradas",
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


# Añade los examenes en formato json
@bot.command()
async def addExam(ctx):
    """
    Añade el examen (root)
    """
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


# Lista los comandos disponibles
@bot.command()
async def info(ctx):
    """
    Información de los comandos disponibles (public)
    """
    commands = bot.commands

    embed = discord.Embed(
        title=f"{ctx.guild.name}",
        description="Estos son los comandos disponibles",
        timestamp=ctx.message.created_at,
        color=discord.Color.gold(),
    )

    for command in commands:
        embed.add_field(
            name=f"{command.name}",
            value=f"{command.help}",
        )

    await ctx.send(embed=embed)


@bot.command()
async def delete(ctx):
    """
    Elimina todos los mensajes del chat de la sala (root)
    """
    if ctx.author.guild_permissions.administrator:
        await ctx.channel.purge()
    else:
        await ctx.send("No tienes permisos para usar este comando")
        await ctx.message.delete()


@bot.command()
async def deleteExam(ctx, exam):
    """
    Elimina el examen (root)
    """
    if ctx.author.guild_permissions.administrator:
        try:
            os.remove(f"src/exam/{exam}.json")
            await ctx.send(f"{exam} Eliminado")
        except FileNotFoundError:
            await ctx.send("No se encontro el examen")
    else:
        await ctx.send("No tienes permisos para usar este comando")
        await ctx.message.delete()


if __name__ == "__main__":

    @bot.event
    async def on_ready():
        print(f"{bot.user} has connected to Discord!")

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(
                "El comando no existe, intenta con !info para ver los comandos disponibles"
            )

    bot.run(TOKEN_BOT)
