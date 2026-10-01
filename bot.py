import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import datetime

# =====================================================
# CONFIGURATION
# =====================================================

SERVER_NAME = "Asgard Minecraft SMP"

RULES_URL = "https://discord.com/channels/1146846387623968869/1554867787934208030"     # Discord rules channel/message URL
DISCORD_URL = "https://discord.gg/x8MRMB64Bd"   # Discord invite URL

# =====================================================
# BOT SETUP
# =====================================================

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =====================================================
# READY EVENT
# =====================================================

@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online!")
    print(f"⚔️ Server: {SERVER_NAME}")

# =====================================================
# WELCOME MESSAGE EVENT
# =====================================================

@bot.event
async def on_member_join(member):
    try:
        guild = member.guild
        welcome_channel_id = os.getenv("WELCOME_CHANNEL_ID")

        # Check welcome channel ID
        if not welcome_channel_id:
            print("❌ WELCOME_CHANNEL_ID not set in Bot.env")
            return

        try:
            welcome_channel = bot.get_channel(int(welcome_channel_id))
        except ValueError:
            print("❌ WELCOME_CHANNEL_ID must be a valid number")
            return

        if not welcome_channel:
            print(f"❌ Welcome channel {welcome_channel_id} not found")
            return

        # Current time
        now = datetime.now()
        time_string = now.strftime("%H:%M")

        # =================================================
        # WELCOME EMBED
        # =================================================

        embed = discord.Embed(
            title=f"⚔️ Welcome to {SERVER_NAME}",
            description=(
                f"**Your adventure begins here, {member.mention}!**\n\n"
                "Welcome to **Asgard Minecraft SMP**, a community built "
                "around friendship, survival, teamwork, and unforgettable adventures.\n\n"
                "🌲 **Explore** the world\n"
                "⛏️ **Build** your kingdom\n"
                "⚔️ **Fight** alongside your allies\n"
                "🏰 **Create** your own legacy\n\n"
                "Before starting your adventure, make sure to read the "
                "server rules below."
            ),
            color=discord.Color.from_str("#8B0000")
        )

        # Member avatar
        embed.set_thumbnail(
            url=member.display_avatar.url
        )

        # Footer
        embed.set_footer(
            text=f"⚔️ Members: {guild.member_count} • Today at {time_string}"
        )

        # =================================================
        # BUTTONS
        # =================================================

        view = discord.ui.View()

        # Server Rules
        view.add_item(
            discord.ui.Button(
                label="Server Rules",
                style=discord.ButtonStyle.link,
                emoji="📜",
                url=RULES_URL if RULES_URL else "https://discord.com"
            )
        )

        # Discord
        view.add_item(
            discord.ui.Button(
                label="Discord",
                style=discord.ButtonStyle.link,
                emoji="💬",
                url=DISCORD_URL if DISCORD_URL else "https://discord.com"
            )
        )

        # =================================================
        # SEND WELCOME MESSAGE
        # =================================================

        await welcome_channel.send(
            content=f"⚔️ Welcome to **{SERVER_NAME}**, {member.mention}!",
            embed=embed,
            view=view
        )

        print(f"✅ Welcome message sent for {member}")

    except Exception as error:
        print(f"❌ Error sending welcome message: {error}")

# =====================================================
# LOGIN
# =====================================================

bot_token = os.getenv("BOT_TOKEN")

if not bot_token:
    print("❌ BOT_TOKEN not found in Bot.env")
else:
    bot.run(bot_token)