import discord
from discord import app_commands
from discord.ext import commands
import re
import shared_state

class add(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="add", description="Adds user(s) to the list. Allows for multiple entries separated by spaces.")
    async def add(self, interaction: discord.Interaction, usernames: str):
        if shared_state.customs_started:
            added_users = []
            errors = []
            for username in usernames.split():
                username = username.strip()

                if re.match(r'<@!?[0-9]+>', username):
                    await interaction.response.send_message("Invalid input.", ephemeral=True)
                    continue

                if username not in shared_state.players_list:
                    shared_state.players_list.append(username)
                    added_users.append(username)
                else:
                    errors.append(f"{username} is already in the list.")

            if added_users:
                added_users_str = ', '.join(added_users)
                await interaction.response.send_message(f"{added_users_str} {'have' if len(added_users) > 1 else 'has'} been added to the list.")
            if errors:
                errors_str = ' '.join(errors)
                await interaction.response.send_message(errors_str, ephemeral=True)
        else:
            await interaction.response.send_message("Customs haven't started yet!", ephemeral=True)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(add(client))
