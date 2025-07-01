import discord
from discord.ext import commands
import json
import os

TOKEN = os.getenv("DISCORD_TOKEN")  # Token depuis les variables d'environnement
TEMPLATE_FILE = "template.json"

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Bot connecté : {bot.user.name}")

@bot.slash_command(name="deploy-template", description="Réinitialise le serveur")
@commands.has_permissions(administrator=True)
async def deploy_template(ctx):
    if ctx.author.id != ctx.guild.owner_id:
        await ctx.respond("❌ Seul le propriétaire peut utiliser cette commande.", ephemeral=True)
        return

    # Supprime tous les salons
    for channel in ctx.guild.channels:
        await channel.delete()

    # Crée les nouveaux salons depuis template.json
    with open(TEMPLATE_FILE) as f:
        template = json.load(f)
    
    last_channel = None
    for category in template["categories"]:
        new_category = await ctx.guild.create_category(category["name"])
        for channel in category["channels"]:
            if channel["type"] == "text":
                new_channel = await ctx.guild.create_text_channel(channel["name"], category=new_category)
            else:
                new_channel = await ctx.guild.create_voice_channel(channel["name"], category=new_category)
            last_channel = new_channel

    await last_channel.send("✅ Template déployée !", delete_after=60)

bot.run(TOKEN)
