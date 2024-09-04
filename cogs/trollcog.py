import discord
from discord import app_commands
from discord.ext import commands
import shared_state

class TicTacToeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    class TicTacToeGame:
        def __init__(self):
            self.board = [' ' for _ in range(9)]
            self.current_turn = 'X'
            self.winner = None

        def make_move(self, pos):
            if self.board[pos] == ' ':
                self.board[pos] = self.current_turn
                if self.check_winner():
                    self.winner = self.current_turn
                else:
                    self.current_turn = 'O' if self.current_turn == 'X' else 'X'
                return True
            return False

        def check_winner(self):
            win_conditions = [
                [0, 1, 2], [3, 4, 5], [6, 7, 8],  # horizontal
                [0, 3, 6], [1, 4, 7], [2, 5, 8],  # vertical
                [0, 4, 8], [2, 4, 6]              # diagonal
            ]
            for condition in win_conditions:
                if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != ' ':
                    return True
            return False

        def is_full(self):
            return ' ' not in self.board

        def get_board_str(self):
            return (f"{self.board[0]} | {self.board[1]} | {self.board[2]}\n"
                    f"---------\n"
                    f"{self.board[3]} | {self.board[4]} | {self.board[5]}\n"
                    f"---------\n"
                    f"{self.board[6]} | {self.board[7]} | {self.board[8]}\n")

    @app_commands.command(name="start_game", description="Start a new Tic Tac Toe game")
    async def start_game(self, interaction: discord.Interaction):
        if interaction.channel.id in self.games:
            await interaction.response.send_message("A game is already in progress in this channel.")
        else:
            self.games[interaction.channel.id] = self.TicTacToeGame()
            await interaction.response.send_message("Started a new game of Tic Tac Toe!\n" + self.games[interaction.channel.id].get_board_str())

    @app_commands.command(name="move", description="Make a move in the Tic Tac Toe game")
    async def move(self, interaction: discord.Interaction, position: int):
        if interaction.channel.id not in self.games:
            await interaction.response.send_message("No game is currently in progress in this channel. Use /start_game to start a new game.")
        else:
            game = self.games[interaction.channel.id]
            if game.winner:
                await interaction.response.send_message(f"The game is over! {game.winner} has won.")
            elif game.is_full():
                await interaction.response.send_message("The game is over! It's a draw.")
            else:
                if game.make_move(position - 1):
                    board_str = game.get_board_str()
                    if game.winner:
                        await interaction.response.send_message(board_str + f"\n{game.winner} wins!")
                    elif game.is_full():
                        await interaction.response.send_message(board_str + "\nIt's a draw!")
                    else:
                        await interaction.response.send_message(board_str + f"\n{game.current_turn}'s turn")
                else:
                    await interaction.response.send_message("Invalid move. Try again.")

    @app_commands.command(name="end_game", description="End the current Tic Tac Toe game")
    async def end_game(self, interaction: discord.Interaction):
        if interaction.channel.id in self.games:
            del self.games[interaction.channel.id]
            await interaction.response.send_message("Ended the current game.")
        else:
            await interaction.response.send_message("No game is currently in progress in this channel.")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(TicTacToeCog(client))