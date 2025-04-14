# Advanced Discord Moderation Bot

An advanced Discord moderation bot with auto-moderation, message filtering, and mod commands built in Python using discord.py.

## Features

### Auto-Moderation
- Profanity filter
- Spam detection
- Discord invite blocking
- Link filtering
- Mass mention protection

### Moderation Commands
- `!warn` - Warn a user
- `!mute` - Mute a user
- `!unmute` - Unmute a user
- `!kick` - Kick a user
- `!ban` - Ban a user
- `!unban` - Unban a user
- `!purge` - Delete multiple messages
- `!lock` - Lock a channel
- `!unlock` - Unlock a channel
- `!slowmode` - Set channel slowmode

### Warning System
- Tracks warnings per user
- Configurable actions when warning threshold is reached
- `!warnings` - View a user's warnings
- `!clearwarnings` - Clear warnings for a user

### Logging System
- Logs moderation actions
- Member join/leave events
- Message edits and deletions
- Role and channel changes

### Auto-Role
- Assign roles automatically to new members
- `!autorole` - Configure auto-role assignment
- `!massrole` - Add a role to all members at once

## Configuration

The bot uses a JSON configuration file located at `data/config.json`. You can edit this file directly or use commands to change settings.

### Configuration Options:

- `prefix`: The command prefix (default: `!`)
- Moderation settings:
  - `warn_threshold`: Number of warnings before action is taken
  - `warn_action`: Action to take when threshold is reached (`mute`, `kick`, or `ban`)
  - `mute_duration`: Duration of mutes in seconds
  - `log_channel_id`: Channel ID for logging actions
- Auto-moderation settings:
  - `enabled`: Enable/disable auto-moderation
  - `filter_profanity`: Filter bad words
  - `filter_spam`: Detect and punish spam
  - `filter_links`: Block links
  - `filter_invites`: Block Discord invites
  - `max_mentions`: Maximum allowed mentions per message
  - `spam_threshold`: Number of messages considered spam
  - `spam_timeframe`: Timeframe for spam detection in seconds
  - `ignored_channels`: List of channel IDs to ignore
  - `ignored_roles`: List of role IDs to ignore
- Auto-role settings:
  - `enabled`: Enable/disable auto-role
  - `default_role_id`: Role ID to assign to new members

## Setup

1. Install required dependencies:
   ```
   pip install discord.py
   ```

2. Set up your environment variable:
   ```
   export DISCORD_TOKEN=your_bot_token
   ```

3. Run the bot:
   ```
   python main.py
   ```

## Permission Requirements

The bot requires the following permissions:
- Manage Roles
- Kick Members
- Ban Members
- Manage Messages
- Manage Channels
- View Channels
- Send Messages
- Read Message History

## Customization

You can customize the bot by editing the configuration files:
- `data/config.json`: General bot settings
- `data/badwords.txt`: List of words to filter, one per line
