# CTFd Discord Auth

Adds a `/discordauth` Discord OAuth2 endpoint for CTFd users to authenticate through.
Upon successful authentication, the user is added to the Discord server and an info message is sent to a specified webhook, linking the Discord user to the corresponding CTFd user.

## Setup

1. Clone to CTFd plugins folder
2. Register new Discord application: https://discord.com/developers/applications
3. Go to `OAuth2` -> `General`:
   - Note down client id and client secret
   - Add redirect URI: `$ctf_url/discordauth` e.g. `https://nc3ctf.dk/discordauth`.
4. Create a Discord bot under the created application and invite to Discord server (must have `Create Instant Invite` permission)
   - Invite URL: https://discord.com/api/oauth2/authorize?scope=bot&permissions=1&client_id=<client_id>
5. Create webhook in discord (`Server Settings` -> `Integrations` -> `Webhooks`) and note down Webhook URL
6. Note down Discord guild ID (`Server Settings` -> `Widget` -> `Server ID`)
7. Set appropriate env vars for CTFd (preferrably under `services` -> `ctfd` -> `environment` in `docker-compose.yml` of the CTFd root):
   - `DISCORD_AUTH_GUILD_ID`
   - `DISCORD_AUTH_WEBHOOK`
   - `DISCORD_AUTH_CLIENT_ID`
   - `DISCORD_AUTH_SECRET`
   - `DISCORD_AUTH_BOT_TOKEN`
