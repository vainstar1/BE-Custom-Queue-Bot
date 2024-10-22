import discord
from discord import app_commands
from discord.ext import commands, tasks

class SyncCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name='sync', description='Syncs the bot commands with Discord.')
    async def sync_commands(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)  # Optional: Show loading message
        try:
            # Syncing the commands using the client instance
            synced = await self.client.tree.sync()
            await interaction.followup.send(f"Successfully synced {len(synced)} commands!")
        except Exception as e:
            await interaction.followup.send(f"Failed to sync commands: {str(e)}")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(SyncCog(client))
