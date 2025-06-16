from keep_alive import keep_alive
keep_alive()
import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True  # Required for message-based commands
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is now online as {bot.user}")

# ========================
# ✅ ROLE MANAGEMENT
# ========================

@bot.command()
@commands.has_permissions(administrator=True)
async def grant(ctx, member: discord.Member, *, role_name: str):
    role_obj = discord.utils.find(lambda r: r.name.lower() == role_name.lower(), ctx.guild.roles)
    if role_obj:
        await member.add_roles(role_obj)
        await ctx.send(f"✅ `{role_obj.name}` role granted to {member.display_name}.")
    else:
        roles = [r.name for r in ctx.guild.roles]
        await ctx.send(f"❌ Role `{role_name}` not found. Available roles:\n```\n{chr(10).join(roles)}\n```")

@bot.command(name="ungrant")
@commands.has_permissions(administrator=True)
async def ungrant(ctx, member: discord.Member, *, role_name: str):
    role_obj = discord.utils.find(lambda r: r.name.lower() == role_name.lower(), ctx.guild.roles)
    if role_obj:
        await member.remove_roles(role_obj)
        await ctx.send(f"❌ `{role_obj.name}` role revoked from {member.display_name}.")
    else:
        roles = [r.name for r in ctx.guild.roles]
        await ctx.send(f"❌ Role `{role_name}` not found. Available roles:\n```\n{chr(10).join(roles)}\n```")

@bot.command()
@commands.has_permissions(administrator=True)
async def list_roles(ctx):
    roles = [role.name for role in ctx.guild.roles]
    role_list = "\n".join(roles)
    await ctx.send(f"🎭 Available roles:\n```\n{role_list}\n```")

# ========================
# 🏗️ SERVER SETUP
# ========================

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    guild = ctx.guild
    await ctx.send("🔧 Setting up server infrastructure...")

    roles = {
        "Admin": discord.Permissions(administrator=True),
        "Operator": discord.Permissions(send_messages=True, read_messages=True),
        "Recruit": discord.Permissions(read_messages=True),
        "Vault Access": discord.Permissions(read_messages=True)
    }

    for role_name, perms in roles.items():
        existing_role = discord.utils.get(guild.roles, name=role_name)
        if not existing_role:
            await guild.create_role(name=role_name, permissions=perms)

    infra = {
        "💠 HQ": ["🔔announcements", "📋rules", "📣broadcasts"],
        "🧠 Intel": ["🧬intel-drops", "📎resources", "🔍investigations"],
        "🎯 Operations": ["📓mission-logs", "📝requests", "🚨alerts"],
        "📦 Archives": ["📂uploads", "📑blueprints"],
    }

    for cat_name, channels in infra.items():
        cat = await guild.create_category(cat_name)
        for chan in channels:
            await cat.create_text_channel(chan)

    await ctx.send("✅ Server structure deployed. Assigning roles now...")

    admin_role = discord.utils.get(guild.roles, name="Admin")
    if admin_role:
        await ctx.author.add_roles(admin_role)

    await ctx.send("🎯 Setup complete. Welcome to the APEX Discord Core.")

# ========================
# 🔁 PING TEST
# ========================

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

# ========================
# 🔐 BOT TOKEN
# ========================

bot.run(os.getenv("DISCORD_TOKEN"))
