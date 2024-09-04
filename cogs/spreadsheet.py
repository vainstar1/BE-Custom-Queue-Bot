import discord
from discord import app_commands
from discord.ext import commands

class spreadsheet(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client    

    @app_commands.command(name="spreadsheet", description="Pastes the link for the BE spreadsheet (created by Blob and Odd).")
    async def spreadsheet(self, interaction: discord.Interaction):
        spreadsheet_link = "https://docs.google.com/spreadsheets/d/1u3s-C-MEGvxUrOvklw0EvgmXE_r1LOhHOVoHibv_RXI/edit?pli=1#gid=0"
        embed = discord.Embed(title="BE Spreadsheet", description=f"[Click here to access the spreadsheet]({spreadsheet_link})", color=discord.Color.blue())
        embed.set_footer(text="This is the official spreadsheet for various BE values, such as healing and damage.")
        await interaction.response.send_message(embed=embed)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(spreadsheet(client))
