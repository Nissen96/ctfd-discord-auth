from .config import config

from flask import request, redirect
import requests
from requests.utils import quote
from CTFd.utils.decorators import authed_only
from CTFd.utils.user import get_current_user
import hmac


API_URL = "https://discord.com/api/v10"


def get_state_secret(client_secret, user):
    return hmac.new(
        client_secret.encode(),
        user.id.to_bytes(8, "big"),
        "sha256"
    ).hexdigest()


def load(app):
    config(app)

    @app.route("/discordauth", methods=["GET"])
    @authed_only
    def discordauth():
        error = request.values.get("error")
        if error:
            return "Error occurred"

        user = get_current_user()

        client_id = app.config["DISCORD_AUTH_CLIENT_ID"]
        client_secret = app.config["DISCORD_AUTH_SECRET"]

        # Authenticate with Discord OAuth2
        code = request.args.get("code")
        if code is None:
            url  = "https://discord.com/oauth2/authorize?response_type=code"
            url += f"&client_id={quote(client_id)}"
            url += f"&redirect_uri={quote(request.base_url)}"
            url += "&scope=guilds.join%20identify"
            url += f"&state={quote(get_state_secret(client_secret, user))}"
            return redirect(url, code=302)

        if not hmac.compare_digest(get_state_secret(client_secret, user), request.args.get("state")):
            return "No csrf pls"

        # Get access token for user
        r = requests.post(
            f"{API_URL}/oauth2/token",
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": request.base_url
            }
        )
        r.raise_for_status()
        access_token = r.json()["access_token"]
        access_details = r.text

        # Get user info
        r = requests.get(f"{API_URL}/users/@me", headers={"Authorization": f"Bearer {access_token}"})
        r.raise_for_status()
        user_id = r.json()["id"]

        # Post user info to webhook
        info  = f"User profile: {request.url_root}users/{user.id}\n"
        info += f"User admin: {request.url_root}admin/users/{user.id}\n"
        info += f"<@{user_id}>\n"
        info += f"```\n{access_details}\n```"
        info += f"```\n{r.text}\n```"
        requests.post(app.config["DISCORD_AUTH_WEBHOOK"], json={"content": info})

        # Add user to guild
        guild_id = app.config["DISCORD_AUTH_GUILD_ID"]
        r = requests.put(
            f"{API_URL}/guilds/{guild_id}/members/{user_id}",
            json={"access_token": access_token},
            headers={"Authorization": f"Bot {app.config['DISCORD_AUTH_BOT_TOKEN']}"}
        )

        # Redirect user to guild
        return redirect(f"https://discord.com/channels/{guild_id}")
