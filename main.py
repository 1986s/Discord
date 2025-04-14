import os
import discord
from discord.ext import commands
import asyncio
import logging
import config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("discord.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize bot with intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config.PREFIX, intents=intents, help_command=None)

# Load cogs when the bot starts
@bot.event
async def on_ready():
    logger.info(f'Bot is ready! Logged in as {bot.user} (ID: {bot.user.id})')
    logger.info(f'Connected to {len(bot.guilds)} guilds')
    
    # Update bot status - explicitly set to online with a watching activity
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.watching, 
            name=f"{config.PREFIX}help | Watching for attackers"
        )
    )
    
    # Load all cogs
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f'Loaded extension: {filename[:-3]}')
            except Exception as e:
                logger.error(f'Failed to load extension {filename[:-3]}: {e}')
    
    # Slash commands are synced in the slash_commands cog
    logger.info("Command syncing will be handled by the slash_commands cog")
    
    # Wait a moment to ensure cogs are loaded, then check if commands are synced
    import asyncio
    async def ensure_commands_synced():
        await asyncio.sleep(5)  # Give the cog a chance to sync first
        
        # Check if we have any global commands registered
        commands = await bot.tree.fetch_commands()
        
        if not commands:
            logger.warning("No slash commands detected after 5 seconds - performing fallback sync")
            try:
                # Try syncing directly if the cog didn't do it
                await bot.tree.sync()
                logger.info(f"Fallback sync complete - registered {len(await bot.tree.fetch_commands())} commands")
            except Exception as e:
                logger.error(f"Failed to perform fallback command sync: {e}")
    
    # Schedule the sync check
    bot.loop.create_task(ensure_commands_synced())

# Error handling for commands
@bot.event
async def on_command_error(ctx, error):
    from utils.helpers import create_embed
    
    # Ignore command not found errors
    if isinstance(error, commands.CommandNotFound):
        return
    
    # Get command name for better error context
    command_name = ctx.command.name if ctx.command else "Unknown"
    
    if isinstance(error, commands.MissingRequiredArgument):
        # Missing argument error
        embed = create_embed(
            title="Missing Argument",
            description=f"You're missing the `{error.param.name}` argument for this command.",
            color="error",
            fields=[
                {"name": "Usage", "value": f"`{config.PREFIX}{command_name} {ctx.command.signature}`", "inline": False},
                {"name": "Help", "value": f"Type `{config.PREFIX}help {command_name}` for more information.", "inline": False}
            ],
            footer=f"Attempted by {ctx.author.name}",
            timestamp=True
        )
    elif isinstance(error, commands.MissingPermissions):
        # Missing permissions error
        missing_perms = ", ".join([f"`{p.replace('_', ' ').title()}`" for p in error.missing_permissions])
        embed = create_embed(
            title="Permission Denied",
            description=f"You don't have the required permissions to use this command.",
            color="error",
            fields=[
                {"name": "Missing Permissions", "value": missing_perms, "inline": False}
            ],
            footer="This command is restricted for your security and the server's safety.",
            timestamp=True
        )
    elif isinstance(error, commands.BotMissingPermissions):
        # Bot missing permissions error
        missing_perms = ", ".join([f"`{p.replace('_', ' ').title()}`" for p in error.missing_permissions])
        embed = create_embed(
            title="Bot Permission Error",
            description=f"I don't have the necessary permissions to execute this command.",
            color="error",
            fields=[
                {"name": "Missing Permissions", "value": missing_perms, "inline": False},
                {"name": "Solution", "value": "Please ask a server administrator to grant me these permissions.", "inline": False}
            ],
            footer="I need these permissions to function correctly.",
            timestamp=True
        )
    elif isinstance(error, commands.CommandOnCooldown):
        # Command on cooldown error
        embed = create_embed(
            title="Command on Cooldown",
            description=f"This command is on cooldown to prevent spam.",
            color="warning",
            fields=[
                {"name": "Try Again In", "value": f"`{error.retry_after:.1f}` seconds", "inline": False}
            ],
            footer=f"Cooldown: {error.cooldown.rate} uses every {error.cooldown.per} seconds",
            timestamp=True
        )
    elif isinstance(error, commands.BadArgument):
        # Bad argument error
        embed = create_embed(
            title="Invalid Argument",
            description=f"You provided an invalid argument for this command.",
            color="error",
            fields=[
                {"name": "Usage", "value": f"`{config.PREFIX}{command_name} {ctx.command.signature}`", "inline": False},
                {"name": "Help", "value": f"Type `{config.PREFIX}help {command_name}` for more information.", "inline": False}
            ],
            footer=f"Attempted by {ctx.author.name}",
            timestamp=True
        )
    elif isinstance(error, commands.DisabledCommand):
        # Disabled command error
        embed = create_embed(
            title="Command Disabled",
            description=f"The command `{command_name}` is currently disabled.",
            color="warning",
            footer="This command may be temporarily disabled for maintenance.",
            timestamp=True
        )
    elif isinstance(error, commands.NotOwner):
        # Not owner error
        embed = create_embed(
            title="Owner Command",
            description=f"The command `{command_name}` can only be used by the bot owner.",
            color="error",
            footer="This command is restricted for security purposes.",
            timestamp=True
        )
    else:
        # Unknown error
        logger.error(f"Command error in {command_name}: {error}")
        embed = create_embed(
            title="An Error Occurred",
            description="An unexpected error occurred while executing the command.",
            color="error",
            fields=[
                {"name": "Error Details", "value": f"```{str(error)}```", "inline": False}
            ],
            footer="The error has been logged for review.",
            timestamp=True
        )
    
    # Send the error embed
    try:
        await ctx.send(embed=embed)
    except discord.HTTPException:
        # Fallback if embed fails to send (e.g., missing permissions)
        await ctx.send(f"Error: {error}")
        logger.error(f"Failed to send error embed for {error}")

# Event when bot joins a new server
@bot.event
async def on_guild_join(guild):
    """Send a welcome message when the bot joins a new server and set up logging"""
    from utils.helpers import create_embed
    import json
    
    # Create a logs category and channel if bot has permission
    log_category = None
    log_channel = None
    
    # Check if bot has necessary permissions
    if guild.me.guild_permissions.manage_channels:
        try:
            # Check if "Bot Logs" category already exists
            for category in guild.categories:
                if category.name.lower() == "bot logs":
                    log_category = category
                    break
            
            # Create category if it doesn't exist
            if not log_category:
                log_category = await guild.create_category("Bot Logs")
                
            # Check if "mod-logs" channel already exists in this category
            for channel in log_category.channels:
                if channel.name.lower() == "mod-logs":
                    log_channel = channel
                    break
            
            # Create channel if it doesn't exist
            if not log_channel:
                log_channel = await log_category.create_text_channel("mod-logs")
                
                # Set permissions to limit who can see logs
                everyone_role = guild.default_role
                await log_channel.set_permissions(everyone_role, read_messages=False)
                await log_channel.set_permissions(guild.me, read_messages=True, send_messages=True)
                
                # Try to grant access to admin and mod roles
                for role in guild.roles:
                    role_name = role.name.lower()
                    if "admin" in role_name or "mod" in role_name:
                        await log_channel.set_permissions(role, read_messages=True)
            
            # Set log channel in config
            with open('./data/config.json', 'r') as f:
                config_data = json.load(f)
            
            config_data["moderation"]["log_channel_id"] = log_channel.id
            
            with open('./data/config.json', 'w') as f:
                json.dump(config_data, f, indent=4)
            
            # Reload config
            import importlib
            import config
            importlib.reload(config)
            
            logger.info(f"Created log channel in {guild.name} (ID: {guild.id})")
        except Exception as e:
            logger.error(f"Error creating log channel: {e}")
    
    # Find the best channel to send the welcome message
    welcome_channel = None
    
    # First try to find a system channel
    if guild.system_channel and guild.system_channel.permissions_for(guild.me).send_messages:
        welcome_channel = guild.system_channel
    
    # If no system channel, look for a general channel
    if not welcome_channel:
        for channel in guild.text_channels:
            # Check if bot has permission to send messages in this channel
            if (channel.permissions_for(guild.me).send_messages and
                channel.name.lower() in ["general", "chat", "main", "lobby", "welcome"]):
                welcome_channel = channel
                break
    
    # If still no channel found, use the first text channel where the bot can send messages
    if not welcome_channel:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                welcome_channel = channel
                break
    
    # If a suitable channel was found, send the welcome message
    if welcome_channel:
        embed = create_embed(
            title=f"Thanks for adding {bot.user.name} to your server!",
            description=f"Hello {guild.name}! I'm a comprehensive moderation bot designed to help keep your server safe and organized.",
            color="info",
            thumbnail=bot.user.avatar.url if bot.user.avatar else None,
            fields=[
                {
                    "name": "📋 Moderation Features",
                    "value": "• User warnings, mutes, kicks, bans\n• Channel lockdown\n• Message purging\n• Slowmode management",
                    "inline": True
                },
                {
                    "name": "🤖 Auto-Moderation",
                    "value": "• Profanity filter\n• Anti-spam protection\n• Discord invite blocking\n• Mass mention prevention",
                    "inline": True
                },
                {
                    "name": "🔍 Logging",
                    "value": "• Message edits/deletions\n• User joins/leaves\n• Moderation actions\n• Role & channel changes",
                    "inline": False
                },
                {
                    "name": "👥 Role Management",
                    "value": "• Auto-role for new members\n• Mass role assignments",
                    "inline": False
                },
                {
                    "name": "🔧 Getting Started",
                    "value": f"• Use `{config.PREFIX}help` to see all commands\n• A logs channel has been created in the 'Bot Logs' category\n• Configure auto-role with `{config.PREFIX}autorole enable @role`",
                    "inline": False
                }
            ],
            footer=f"{config.FOOTER} | Prefix: {config.PREFIX}",
            timestamp=True
        )
        
        try:
            await welcome_channel.send(embed=embed)
            
            # Also send a DM to server owner with setup instructions
            try:
                owner_embed = create_embed(
                    title=f"Thanks for adding {bot.user.name}!",
                    description=f"Your bot has been successfully added to **{guild.name}**. Here's how to get started with setup:",
                    color="info",
                    thumbnail=bot.user.avatar.url if bot.user.avatar else None,
                    fields=[
                        {
                            "name": "1️⃣ Set a Logging Channel",
                            "value": f"Use `{config.PREFIX}setlogchannel #channel` to set up logging",
                            "inline": False
                        },
                        {
                            "name": "2️⃣ Configure Auto-Moderation",
                            "value": f"Use `{config.PREFIX}automod config` to enable/disable features",
                            "inline": False
                        },
                        {
                            "name": "3️⃣ Set Up Auto-Role (Optional)",
                            "value": f"Use `{config.PREFIX}autorole enable @role` to automatically assign roles to new members",
                            "inline": False
                        },
                        {
                            "name": "📚 Help and Commands",
                            "value": f"Type `{config.PREFIX}help` to see all available commands",
                            "inline": False
                        }
                    ],
                    footer="For support or questions, please check the documentation",
                    timestamp=True
                )
                await guild.owner.send(embed=owner_embed)
            except discord.Forbidden:
                # Couldn't DM the owner, that's fine
                pass
            
        except Exception as e:
            logger.error(f"Failed to send welcome message in {guild.name}: {e}")
            
    # Log the new server join
    logger.info(f"Bot has been added to a new server: {guild.name} (ID: {guild.id}) - Owner: {guild.owner}")
    logger.info(f"The guild has {guild.member_count} members")

# Custom help command
@bot.command(name="help")
async def help_command(ctx, command_name=None):
    from utils.helpers import create_embed
    
    if command_name:
        command = bot.get_command(command_name)
        if command:
            # Create detailed help for specific command
            embed = create_embed(
                title=f"Command: {config.PREFIX}{command.name}",
                description=command.help or "No description available",
                color="info",
                timestamp=True,
                author={
                    "name": bot.user.name,
                    "icon_url": bot.user.avatar.url if bot.user.avatar else None
                },
                fields=[
                    {"name": "Usage", "value": f"`{config.PREFIX}{command.name} {command.signature}`", "inline": False}
                ],
                footer=f"{config.FOOTER} | Requested by {ctx.author.name}"
            )
            
            # Add aliases if any
            if command.aliases:
                aliases = ", ".join([f"`{config.PREFIX}{alias}`" for alias in command.aliases])
                embed.add_field(name="Aliases", value=aliases, inline=False)
                
            # Add cooldown if any
            if command._buckets._cooldown:
                cooldown = command._buckets._cooldown
                embed.add_field(
                    name="Cooldown",
                    value=f"{cooldown.rate} use(s) every {cooldown.per} seconds",
                    inline=False
                )
                
            # Add required permissions if any
            required_permissions = []
            for check in command.checks:
                if hasattr(check, "__qualname__") and "has_permissions" in check.__qualname__:
                    # This is a bit of a hack to extract permissions from the check
                    # It assumes the check is created by commands.has_permissions decorator
                    import inspect
                    check_source = inspect.getsource(check)
                    import re
                    matches = re.findall(r'(\w+)=True', check_source)
                    if matches:
                        required_permissions.extend(matches)
            
            if required_permissions:
                formatted_perms = ", ".join([f"`{perm.replace('_', ' ').title()}`" for perm in required_permissions])
                embed.add_field(name="Required Permissions", value=formatted_perms, inline=False)
                
        else:
            # Command not found
            embed = create_embed(
                title="Command Not Found",
                description=f"The command `{config.PREFIX}{command_name}` was not found.",
                color="error",
                footer=f"{config.FOOTER} | Type {config.PREFIX}help to see all available commands."
            )
    else:
        # Create general help with categories
        embed = create_embed(
            title=f"{bot.user.name} Help",
            description=f"Here are all the available commands. Use `{config.PREFIX}help <command>` for detailed information.",
            color="info",
            timestamp=True,
            thumbnail=bot.user.avatar.url if bot.user.avatar else None,
            footer=f"{config.FOOTER} | Requested by {ctx.author.name}"
        )
        
        # Group commands by category (cog)
        for cog_name in bot.cogs:
            cog = bot.get_cog(cog_name)
            commands_list = cog.get_commands()
            
            if commands_list:
                # Format commands with emojis based on category
                category_emojis = {
                    "Moderation": "🛡️",
                    "AutoMod": "🤖",
                    "Logging": "📋",
                    "AutoRole": "👥"
                }
                
                emoji = category_emojis.get(cog_name, "🔹")
                
                # Build command list with short descriptions
                commands_desc = "\n".join([
                    f"{emoji} `{config.PREFIX}{cmd.name}` - {cmd.help.split('.')[0] if cmd.help else 'No description'}" 
                    for cmd in sorted(commands_list, key=lambda x: x.name)
                ])
                
                embed.add_field(name=f"__{cog_name}__", value=commands_desc, inline=False)
    
    await ctx.send(embed=embed)

# Import Flask app for web interface
from web_app import app

# Run the bot or web app based on environment
if __name__ == "__main__":
    # Check if we're being run from gunicorn (for web app)
    if 'gunicorn' in os.environ.get('SERVER_SOFTWARE', ''):
        # We're being run as a web app, app variable will be used by gunicorn
        logger.info("Running as web application via gunicorn")
    else:
        # We're being run directly, start the Discord bot
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            logger.error("No DISCORD_TOKEN found in environment variables!")
            exit(1)
        
        try:
            logger.info("Starting Discord bot...")
            asyncio.run(bot.start(token))
        except KeyboardInterrupt:
            logger.info("Bot shutdown initiated by keyboard interrupt")
        except Exception as e:
            logger.error(f"Error running bot: {e}")
