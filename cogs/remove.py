import discord
from discord import app_commands
from discord.ext import commands

customs_started = False
players_list = []

class remove(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client    
    
    @app_commands.command(name="remove", description="Removes a username if they are in the list.")
    async def remove(self, interaction: discord.Interaction, targets: str):
        global customs_started, players_list

        if customs_started:
            removed_users = []
            errors = []

            indices_to_remove = []
            usernames_to_remove = []

            for target in targets.split():
                try:
                    index = int(target)
                    if 1 <= index <= len(players_list):
                        indices_to_remove.append(index - 1)
                    else:
                        errors.append(f"Invalid index {index}.")
                except ValueError:
                    usernames_to_remove.append(target)

            indices_to_remove.sort(reverse=True)
            for index in indices_to_remove:
                removed_users.append(players_list.pop(index))

            for username in usernames_to_remove:
                if username in players_list:
                    players_list.remove(username)
                    removed_users.append(username)
                else:
                    errors.append(f"{username} not found in the list.")

            if removed_users:
                removed_users_str = ', '.join(removed_users)
                await interaction.response.send_message(f"Removed: {removed_users_str}")
            if errors:
                errors_str = ' '.join(errors)
                await interaction.response.send_message(errors_str, ephemeral=True)
        else:
            await interaction.response.send_message("Customs haven't started yet!", ephemeral=True)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(remove(client))

