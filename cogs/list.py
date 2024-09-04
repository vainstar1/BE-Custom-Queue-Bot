import discord
from discord import app_commands
from discord.ext import commands
import os
import re
import asyncio
import shared_state

class JoinButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Join", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        if shared_state.customs_started:
            nickname = interaction.user.nick
            username = interaction.user.name

            if nickname:
                username = nickname

            if username not in shared_state.players_list:
                shared_state.players_list.append(username)
                await interaction.response.send_message(f"You have been added to the list.", ephemeral=True)
            else:
                await interaction.response.send_message(f"You are already in the list.", ephemeral=True)
        else:
            await interaction.response.send_message("Customs haven't started yet!", ephemeral=True)

class LeaveButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Leave", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        if shared_state.customs_started:
            nickname = interaction.user.nick
            username = interaction.user.name

            if nickname:
                username = nickname

            if username in shared_state.players_list:
                shared_state.players_list.remove(username)
                await interaction.response.send_message(f"{username} has been removed from the list.")
            else:
                await interaction.response.send_message(f"{username} is not in the list.")
        else:
            await interaction.response.send_message("Customs haven't started yet!")

class AddButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Add", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        # Create a modal with an input field for usernames
        modal = discord.ui.Modal(title="Add Usernames")
        modal.add_item(discord.ui.TextInput(label="Usernames", style=discord.TextStyle.short, placeholder="Enter usernames separated by spaces"))

        await interaction.response.send_modal(modal)

        # Wait for the modal response
        def check(m):
            return isinstance(m, discord.Interaction) and m.type == discord.InteractionType.modal_submit and m.user == interaction.user

        try:
            # Get modal response
            modal_interaction = await interaction.client.wait_for("interaction", timeout=60.0, check=check)

            # Extract the input from the modal
            input_value = modal_interaction.data['components'][0]['components'][0]['value'].strip()
            if input_value:
                usernames = input_value.split()
                added_users = []
                errors = []

                for username in usernames:
                    username = username.strip()

                    # Validate the input
                    if re.match(r'<@!?[0-9]+>', username):
                        await modal_interaction.response.send_message("Invalid input. Please do not include mentions.", ephemeral=True)
                        return

                    if username not in shared_state.players_list:
                        shared_state.players_list.append(username)
                        added_users.append(username)
                    else:
                        errors.append(f"{username} is already in the list.")

                # Provide feedback
                if added_users:
                    added_users_str = ', '.join(added_users)
                    await modal_interaction.response.send_message(f"{added_users_str} {'have' if len(added_users) > 1 else 'has'} been added to the list.")
                if errors:
                    errors_str = ' '.join(errors)
                    await modal_interaction.response.send_message(errors_str, ephemeral=True)
            else:
                await modal_interaction.response.send_message("No usernames were provided.", ephemeral=True)
        except asyncio.TimeoutError:
            await interaction.response.send_message("You took too long to respond. Please try again.", ephemeral=True)

class RemoveUserButton(discord.ui.Button):
    def __init__(self, username):
        super().__init__(label=username, style=discord.ButtonStyle.secondary)
        self.username = username

    async def callback(self, interaction: discord.Interaction):
        # Toggle selection status
        if self.username in shared_state.selected_users:
            shared_state.selected_users.remove(self.username)
            self.style = discord.ButtonStyle.secondary
        else:
            shared_state.selected_users.append(self.username)
            self.style = discord.ButtonStyle.success

        # Update the button style
        await interaction.response.edit_message(view=self.view)

class RemoveUserView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        # Move the confirmation button to the far right
        self.add_item(discord.ui.Button(label="Remove", style=discord.ButtonStyle.danger, custom_id="remove_button", row=1))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.type == discord.InteractionType.component:
            if interaction.data['custom_id'] == "remove_button":
                selected_users = shared_state.selected_users
                for user in selected_users:
                    if user in shared_state.players_list:
                        shared_state.players_list.remove(user)
                await interaction.response.send_message(f"Removed users: {', '.join(selected_users)}" if selected_users else "No users selected.")
                shared_state.selected_users.clear()
                return False
        return True

class RemoveButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Remove", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        if not shared_state.players_list:
            await interaction.response.send_message("No users to remove.", ephemeral=True)
            return
        
        view = RemoveUserView()
        for username in shared_state.players_list:
            view.add_item(RemoveUserButton(username))
        # Make the message ephemeral
        await interaction.response.send_message("Select users to remove:", view=view, ephemeral=True)

class RefreshButton(discord.ui.Button):
    def __init__(self, client: commands.Bot):
        super().__init__(label="Refresh", style=discord.ButtonStyle.secondary)
        self.client = client

    async def callback(self, interaction: discord.Interaction):
        # Create a fresh embed and view
        embed = await PlayerList(self.client).create_player_list_embed()
        view = CustomButtons(self.client)
        
        # Update the message
        await interaction.response.edit_message(embed=embed, view=view)


class CustomButtons(discord.ui.View):
    def __init__(self, client: commands.Bot):
        super().__init__(timeout=None)  # No timeout for the view
        self.client = client
        self.add_item(JoinButton())
        self.add_item(AddButton())
        self.add_item(RemoveButton())
        self.add_item(LeaveButton())
        self.add_item(RefreshButton(client))

class PlayerList(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="list", description="Displays the list of players and active custom code.")
    async def list(self, interaction: discord.Interaction):
        try:
            if shared_state.customs_started:
                embed = await self.create_player_list_embed()
                view = CustomButtons(self.client)
                await interaction.response.send_message(embed=embed, view=view)
            else:
                embed = discord.Embed(
                    title="Customs Not Started",
                    description="Customs haven't started yet! Use /start <code> to start them.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed)
        except discord.errors.NotFound:
            await interaction.followup.send("Something went wrong with the interaction, please try again.", ephemeral=True)

    async def create_player_list_embed(self):
        total_players = len(shared_state.players_list)
        code = shared_state.current_code or "No active custom code"
        if total_players > 0:
            players = "\n".join([f"{i + 1}. {user}" for i, user in enumerate(shared_state.players_list)])
            embed = discord.Embed(
                title="Player List",
                description=f"Total Players: {total_players}\nCode: {code}\n\n{players}",
                color=discord.Color.blue()
            )
        else:
            embed = discord.Embed(
                title="Player List",
                description=f"There is nobody in the current list.\n\nCode: {code}",
                color=discord.Color.orange()
            )
        return embed

async def setup(client: commands.Bot) -> None:
    await client.add_cog(PlayerList(client))
