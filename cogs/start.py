import discord
from discord import app_commands
from discord.ext import commands

customs_started = False
players_list = []
current_code = None
GENERAL_CHANNEL_ID = 1099419224914542693
ROLE_ID = 1198429813103403148

class start(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client    

    @app_commands.command(name="start", description="Starts a customs list with the given code.")
    async def start(self, interaction: discord.Interaction, code: str): 
        global customs_started, current_code

        if customs_started:
            return await interaction.response.send_message("A custom queue is already active.")

        rolePing = f"<@&{ROLE_ID}>"
        customs_started = True
        players_list.clear()
        current_code = code
        startMessage = (f"{rolePing} {interaction.user.mention} Started a custom queue with code: {code}. Type /join to be put on the list.")

        channel = interaction.guild.get_channel(GENERAL_CHANNEL_ID)
        if channel is not None:
            await interaction.response.send_message(f"You have initiated customs. Sending ping in general.", ephemeral=True)
            await channel.send(startMessage)
        else:
            await interaction.response.send_message("Failed to find the specified channel.")

async def setup(client:commands.Bot) -> None:
    await client.add_cog(start(client))

