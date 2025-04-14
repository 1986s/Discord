import json
import os
from pathlib import Path

# Default configuration
DEFAULT_CONFIG = {
    "prefix": "@",
    "footer": "Made with ❤️ by 30ax",
    "moderation": {
        "warn_threshold": 3,
        "warn_action": "mute",
        "mute_duration": 3600,  # in seconds (1 hour)
        "log_channel_id": None
    },
    "automod": {
        "enabled": True,
        "filter_profanity": True,
        "filter_spam": True,
        "filter_links": False,
        "filter_invites": True,
        "max_mentions": 5,
        "spam_threshold": 5,  # messages
        "spam_timeframe": 5,  # seconds
        "ignored_channels": [],
        "ignored_roles": []
    },
    "autorole": {
        "enabled": False,
        "default_role_id": None
    }
}

# Create data directory if it doesn't exist
Path("./data").mkdir(exist_ok=True)

# Load or create configuration
def load_config():
    try:
        with open('./data/config.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Create default config file if it doesn't exist
        with open('./data/config.json', 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG

# Save configuration
def save_config(config_data):
    with open('./data/config.json', 'w') as f:
        json.dump(config_data, f, indent=4)

# Load configuration
config = load_config()

# Bot prefix
PREFIX = config.get("prefix", "@")

# Bot footer (for welcome and help commands only)
FOOTER = config.get("footer", "Made with ❤️ by 30ax")
# Minimal footer for other commands
MINIMAL_FOOTER = ""

# Moderation settings
WARN_THRESHOLD = config["moderation"].get("warn_threshold", 3)
WARN_ACTION = config["moderation"].get("warn_action", "mute")
MUTE_DURATION = config["moderation"].get("mute_duration", 3600)
LOG_CHANNEL_ID = config["moderation"].get("log_channel_id", None)

# Automod settings
AUTOMOD_ENABLED = config["automod"].get("enabled", True)
FILTER_PROFANITY = config["automod"].get("filter_profanity", True)
FILTER_SPAM = config["automod"].get("filter_spam", True)
FILTER_LINKS = config["automod"].get("filter_links", False)
FILTER_INVITES = config["automod"].get("filter_invites", True)
MAX_MENTIONS = config["automod"].get("max_mentions", 5)
SPAM_THRESHOLD = config["automod"].get("spam_threshold", 5)
SPAM_TIMEFRAME = config["automod"].get("spam_timeframe", 5)
IGNORED_CHANNELS = config["automod"].get("ignored_channels", [])
IGNORED_ROLES = config["automod"].get("ignored_roles", [])

# Autorole settings
AUTOROLE_ENABLED = config["autorole"].get("enabled", False)
DEFAULT_ROLE_ID = config["autorole"].get("default_role_id", None)
