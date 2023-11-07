from os import environ


def config(app):
    '''
    Discord guild id (server id)
    '''
    app.config["DISCORD_AUTH_GUILD_ID"] = environ.get("DISCORD_AUTH_GUILD_ID")

    '''
    Discord webhook for admin channel where auth is logged.
    Auth is not saved anywhere, it's just posted to the webhook.
    '''
    app.config["DISCORD_AUTH_WEBHOOK"] = environ.get("DISCORD_AUTH_WEBHOOK")

    '''
    Discord oauth client ID
    '''
    app.config["DISCORD_AUTH_CLIENT_ID"] = environ.get("DISCORD_AUTH_CLIENT_ID")

    '''
    Discord oauth secret (also used for state hmac secret)
    '''
    app.config["DISCORD_AUTH_SECRET"] = environ.get("DISCORD_AUTH_SECRET")

    '''
    Discord bot token. Bot must belong to the auth application,
    have access to the guild, and have "Create Instant Invite" rights
    '''
    app.config["DISCORD_AUTH_BOT_TOKEN"] = environ.get("DISCORD_AUTH_BOT_TOKEN")
