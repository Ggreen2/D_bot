import discord
from discord.ext import commands
from discord.ui import Button, View
import json
import asyncio

"""
DISCORD TEXT FORMATTING
italic - *
bold - **
bold and italic - ***
underlined - __
strikethrough - ~~
block quote - > (just one, multi-line quotes use one on each line)
spoiler - ||
"""

intents = discord.Intents.default()
intents.message_content = True

# Set your desired command prefix here
bot = commands.Bot(command_prefix='?', intents=intents)

# classes & variables

# A list to store the names of users who have clicked "Join"
player_list_main = []

'''
User's name on the server - interaction.user.display_name
'''


def check_if_exists_main(player) -> bool:
    exists = False
    for item in player_list_main:
        if item.get_user() == player.get_user():
            exists = True
    return exists


def get_index_main(player) -> int:
    index = 0
    for item in player_list_main:
        if item.get_user() == player.get_user():
            return index
        else:
            index += 1
    return -1


def add_player_main(player):
    if not check_if_exists_main(player):
        player_list_main.append(player)


class Player:
    def __init__(self, user: str, name: str, role: str = "Fill"):
        self.user = user
        self.name = name
        self.role = role
        self.head2head = []

    def get_user(self):
        return self.user

    def get_name(self):
        return self.name

    def get_role(self):
        return self.role

    def set_role(self, new_role):
        self.role = new_role

    def check_if_exists(self, user: str) -> bool:
        exists = False
        for item in self.head2head:
            if item.get_user() == user:
                exists = True
        return exists

    def add_head2head(self, user: str, name: str):
        if not self.check_if_exists(user):
            self.head2head.append(HeadToHead(user, name))

    def get_index(self, user) -> int:
        index = 0
        for item in self.head2head:
            if item.get_user() == user:
                return index
            else:
                index += 1
        return -1

    def get_stats(self, user, name):
        if self.check_if_exists(user):
            return_me = f"{name} - {self.head2head[self.get_index(user)].stats()}"
        else:
            return_me = f"You have played no games with {name}"
        return return_me

    def update_head2head(self, user, name, same_team: bool, did_win: bool):
        if not self.check_if_exists(user):
            self.add_head2head(user, name)
        curr_h_2_h = self.head2head[self.get_index(user)]
        if same_team:
            if did_win:
                curr_h_2_h.win_game_with()
            else:
                curr_h_2_h.lose_game_with()
        else:
            if did_win:
                curr_h_2_h.win_game_against()
            else:
                curr_h_2_h.lose_game_against()


class HeadToHead:
    def __init__(self, user, name):
        self.user = user
        self.name = name
        self.games_with_won = 0.0
        self.games_with_total = 0.0
        self.games_against_won = 0.0
        self.games_against_total = 0.0

    def stats(self):
        result = ""
        if self.games_with_total > 0:
            result += f"{round((self.games_with_won / self.games_with_total), 2)}% winrate while on your team ({self.games_with_won}/{self.games_with_total} games), "
        else:
            result += f"You have played no games with {self.name} on your team, "
        if self.games_against_total > 0:
            result += f"{round((self.games_against_won / self.games_against_total), 2)}% winrate against them ({self.games_against_won}/{self.games_against_total} games)"
        else:
            result += f"You have played no games against {self.name}"
        return result

    def get_user(self):
        return self.user

    def get_name(self):
        return self.name

    def win_game_with(self):
        self.games_with_total += 1
        self.games_with_won += 1

    def lose_game_with(self):
        self.games_with_total += 1

    def win_game_against(self):
        self.games_against_total += 1
        self.games_against_won += 1

    def lose_game_against(self):
        self.games_against_total += 1

        # basic layout


class EmbedView(View):
    def __init__(self):
        super().__init__()
        self.page = 0

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary, custom_id="next_page")
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page += 1
        if self.page > 2:
            self.page = 0
        await self.update_embed(interaction)

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary, custom_id="prev_page")
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page -= 1
        if self.page < 0:
            self.page = 2
        await self.update_embed(interaction)

    async def update_embed(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Dynamic Embed",
            description=f"This is page {self.page + 1}",
            color=discord.Color.blue()
        )
        await interaction.response.edit_message(embed=embed, view=self)


'''
TODO:
- Need to go through all buttons and functions in both embedflex and embedinhouse to change that they first check if player exists in main player
list, if not then add them (obv), and then call their role from there. both embeds will have a unique list JUST FOR THAT INSTANCE,
essentially where you call player list for them
'''


class EmbedFlex(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.player_list_flex = []

    def check_if_exists_flex(self, player) -> bool:
        exists = False
        for item in self.player_list_flex:
            if item.get_user() == player.get_user():
                exists = True
        return exists

    def get_index_flex(self, player) -> int:
        index = 0
        for item in self.player_list_flex:
            if item.get_user() == player.get_user():
                return index
            else:
                index += 1
        return -1

    @discord.ui.button(label="Top", style=discord.ButtonStyle.success, custom_id="top_role_flex")
    async def top_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = "Top"
        new_player = Player(interaction.user.name, interaction.user.display_name, new_role)
        if not check_if_exists_main(new_player):
            add_player_main(new_player)
        player_list_main[get_index_main(new_player)].set_role(new_role)
        if not self.check_if_exists_flex(new_player):
            self.player_list_flex.append(new_player)
            await interaction.response.send_message("You were given the role Top lane", ephemeral=True)
        else:
            self.player_list_flex[self.get_index_flex(new_player)].set_role(new_role)
            await interaction.response.send_message("Your role has been switched to Top lane", ephemeral=True)
        await self.update_embed(interaction)

    @discord.ui.button(label="Jungle", style=discord.ButtonStyle.success, custom_id="jng_role_flex")
    async def jng_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = "Jung"
        new_player = Player(interaction.user.name, interaction.user.display_name, new_role)
        if not check_if_exists_main(new_player):
            add_player_main(new_player)
        player_list_main[get_index_main(new_player)].set_role(new_role)
        if not self.check_if_exists_flex(new_player):
            self.player_list_flex.append(new_player)
            await interaction.response.send_message("You were given the role Jungler", ephemeral=True)
        else:
            self.player_list_flex[self.get_index_flex(new_player)].set_role(new_role)
            await interaction.response.send_message("Your role has been switched to Jungler", ephemeral=True)
        await self.update_embed(interaction)

    @discord.ui.button(label="Middle", style=discord.ButtonStyle.success, custom_id="mid_role_flex")
    async def mid_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = "Mid"
        new_player = Player(interaction.user.name, interaction.user.display_name, new_role)
        if not check_if_exists_main(new_player):
            add_player_main(new_player)
        player_list_main[get_index_main(new_player)].set_role(new_role)
        if not self.check_if_exists_flex(new_player):
            self.player_list_flex.append(new_player)
            await interaction.response.send_message("You were given the role Mid Laner", ephemeral=True)
        else:
            self.player_list_flex[self.get_index_flex(new_player)].set_role(new_role)
            await interaction.response.send_message("Your role has been switched to Mid Laner", ephemeral=True)
        await self.update_embed(interaction)

    @discord.ui.button(label="Bottom", style=discord.ButtonStyle.success, custom_id="bot_role_flex")
    async def bot_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = "Bot"
        new_player = Player(interaction.user.name, interaction.user.display_name, new_role)
        if not check_if_exists_main(new_player):
            add_player_main(new_player)
        player_list_main[get_index_main(new_player)].set_role(new_role)
        if not self.check_if_exists_flex(new_player):
            self.player_list_flex.append(new_player)
            await interaction.response.send_message("You were given the role Bot Laner", ephemeral=True)
        else:
            self.player_list_flex[self.get_index_flex(new_player)].set_role(new_role)
            await interaction.response.send_message("Your role has been switched to Bot Laner", ephemeral=True)
        await self.update_embed(interaction)

    @discord.ui.button(label="Support", style=discord.ButtonStyle.success, custom_id="sup_role_flex")
    async def sup_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = "Sup"
        new_player = Player(interaction.user.name, interaction.user.display_name, new_role)
        if not check_if_exists_main(new_player):
            add_player_main(new_player)
        player_list_main[get_index_main(new_player)].set_role(new_role)
        if not self.check_if_exists_flex(new_player):
            self.player_list_flex.append(new_player)
            await interaction.response.send_message("You were given the role Support", ephemeral=True)
        else:
            self.player_list_flex[self.get_index_flex(new_player)].set_role(new_role)
            await interaction.response.send_message("Your role has been switched to Support", ephemeral=True)
        await self.update_embed(interaction)

    @discord.ui.button(label="Fill", style=discord.ButtonStyle.primary, custom_id="fill_role_flex")
    async def fill_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = "Fill"
        new_player = Player(interaction.user.name, interaction.user.display_name, new_role)
        if not check_if_exists_main(new_player):
            add_player_main(new_player)
        player_list_main[get_index_main(new_player)].set_role(new_role)
        if not self.check_if_exists_flex(new_player):
            self.player_list_flex.append(new_player)
            await interaction.response.send_message("You were given the role Fill", ephemeral=True)
        else:
            self.player_list_flex[self.get_index_flex(new_player)].set_role(new_role)
            await interaction.response.send_message("Your role has been switched to Fill", ephemeral=True)
        await self.update_embed(interaction)

    @discord.ui.button(label="Leave Queue", style=discord.ButtonStyle.danger, custom_id="leave_flex")
    async def leave_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_player = Player(interaction.user.name, interaction.user.display_name)
        if not check_if_exists_main(new_player):
            add_player_main(new_player)
        if not self.check_if_exists_flex(new_player):
            await interaction.response.send_message("You were not in the queue", ephemeral=True)
        else:
            del self.player_list_flex[self.get_index_flex(new_player)]
            await interaction.response.send_message("You have been removed from the queue", ephemeral=True)
        await self.update_embed(interaction)

    async def update_embed(self, interaction: discord.Interaction):
        num = len(self.player_list_flex)
        if num >= 5:
            new_color = discord.Color.green()
        else:
            new_color = discord.Color.red()
        if num == 0:
            desc = "No players currently"
        else:
            desc = "Players currently waiting to play flex queue with others\n"
            for i in range(num):
                desc += f"\n- {self.player_list_flex[i].get_name()} - {self.player_list_flex[i].get_role()}"
            desc += "\n\nHave enough players? Join a call!"
        embed = discord.Embed(
            title="Flex Queue",
            description=f"{desc}",
            color=new_color
        )
        await interaction.message.edit(embed=embed, view=self)


class EmbedInhouse(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.player_list_inhouse = []

    def check_if_exists_inhouse(self, player) -> bool:
        exists = False
        for item in self.player_list_inhouse:
            if item.get_user() == player.get_user():
                exists = True
        return exists

    def get_index_inhouse(self, player) -> int:
        index = 0
        for item in self.player_list_inhouse:
            if item.get_user() == player.get_user():
                return index
            else:
                index += 1
        return -1

    @discord.ui.button(label="Top", style=discord.ButtonStyle.secondary, custom_id="top_role_flex")
    async def top_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = "Top"
        new_player = Player(interaction.user.name, interaction.user.display_name, new_role)
        if not check_if_exists_main(new_player):
            add_player_main(new_player)
        player_list_main[get_index_main(new_player)].set_role(new_role)
        if not self.check_if_exists_inhouse(new_player):
            self.player_list_inhouse.append(new_player)
            await interaction.response.send_message("You were given the role Top lane", ephemeral=True)
        else:
            self.player_list_inhouse[self.get_index_inhouse(new_player)].set_role(new_role)
            await interaction.response.send_message("Your role has been switched to Top lane", ephemeral=True)
        await self.update_embed(interaction)

    @discord.ui.button(label="Jungle", style=discord.ButtonStyle.secondary, custom_id="jng_role_flex")
    async def jng_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = "Jung"
        new_player = Player(interaction.user.name, interaction.user.display_name, new_role)
        if not check_if_exists_main(new_player):
            add_player_main(new_player)
        player_list_main[get_index_main(new_player)].set_role(new_role)
        if not self.check_if_exists_inhouse(new_player):
            self.player_list_inhouse.append(new_player)
            await interaction.response.send_message("You were given the role Jungler", ephemeral=True)
        else:
            self.player_list_inhouse[self.get_index_inhouse(new_player)].set_role(new_role)
            await interaction.response.send_message("Your role has been switched to Jungler", ephemeral=True)
        await self.update_embed(interaction)

    @discord.ui.button(label="Middle", style=discord.ButtonStyle.secondary, custom_id="mid_role_flex")
    async def mid_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = "Mid"
        new_player = Player(interaction.user.name, interaction.user.display_name, new_role)
        if not check_if_exists_main(new_player):
            add_player_main(new_player)
        player_list_main[get_index_main(new_player)].set_role(new_role)
        if not self.check_if_exists_inhouse(new_player):
            self.player_list_inhouse.append(new_player)
            await interaction.response.send_message("You were given the role Mid Laner", ephemeral=True)
        else:
            self.player_list_inhouse[self.get_index_inhouse(new_player)].set_role(new_role)
            await interaction.response.send_message("Your role has been switched to Mid Laner", ephemeral=True)
        await self.update_embed(interaction)

    @discord.ui.button(label="Bottom", style=discord.ButtonStyle.secondary, custom_id="bot_role_flex")
    async def bot_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = "Bot"
        new_player = Player(interaction.user.name, interaction.user.display_name, new_role)
        if not check_if_exists_main(new_player):
            add_player_main(new_player)
        player_list_main[get_index_main(new_player)].set_role(new_role)
        if not self.check_if_exists_inhouse(new_player):
            self.player_list_inhouse.append(new_player)
            await interaction.response.send_message("You were given the role Bot Laner", ephemeral=True)
        else:
            self.player_list_inhouse[self.get_index_inhouse(new_player)].set_role(new_role)
            await interaction.response.send_message("Your role has been switched to Bot Laner", ephemeral=True)
        await self.update_embed(interaction)

    @discord.ui.button(label="Support", style=discord.ButtonStyle.secondary, custom_id="sup_role_flex")
    async def sup_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = "Sup"
        new_player = Player(interaction.user.name, interaction.user.display_name, new_role)
        if not check_if_exists_main(new_player):
            add_player_main(new_player)
        player_list_main[get_index_main(new_player)].set_role(new_role)
        if not self.check_if_exists_inhouse(new_player):
            self.player_list_inhouse.append(new_player)
            await interaction.response.send_message("You were given the role Support", ephemeral=True)
        else:
            self.player_list_inhouse[self.get_index_inhouse(new_player)].set_role(new_role)
            await interaction.response.send_message("Your role has been switched to Support", ephemeral=True)
        await self.update_embed(interaction)

    @discord.ui.button(label="Fill", style=discord.ButtonStyle.primary, custom_id="fill_role_flex")
    async def fill_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = "Fill"
        new_player = Player(interaction.user.name, interaction.user.display_name, new_role)
        if not check_if_exists_main(new_player):
            add_player_main(new_player)
        player_list_main[get_index_main(new_player)].set_role(new_role)
        if not self.check_if_exists_inhouse(new_player):
            self.player_list_inhouse.append(new_player)
            await interaction.response.send_message("You were given the role Fill", ephemeral=True)
        else:
            self.player_list_inhouse[self.get_index_inhouse(new_player)].set_role(new_role)
            await interaction.response.send_message("Your role has been switched to Fill", ephemeral=True)
        await self.update_embed(interaction)

    @discord.ui.button(label="Leave Queue", style=discord.ButtonStyle.danger, custom_id="leave_flex")
    async def leave_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_player = Player(interaction.user.name, interaction.user.display_name)
        if not check_if_exists_main(new_player):
            add_player_main(new_player)
        if not self.check_if_exists_inhouse(new_player):
            await interaction.response.send_message("You were not in the queue", ephemeral=True)
        else:
            del self.player_list_inhouse[self.get_index_inhouse(new_player)]
            await interaction.response.send_message("You have been removed from the queue", ephemeral=True)
        await self.update_embed(interaction)

    @discord.ui.button(label="Start Match", style=discord.ButtonStyle.success, disabled=True, custom_id="start_ih")
    async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Game starting!", ephemeral=True)

    async def update_embed(self, interaction: discord.Interaction):
        num = len(self.player_list_inhouse)
        if num >= 1:
            new_color = discord.Color.green()
            self.start_button.disabled = False
        else:
            new_color = discord.Color.red()
            self.start_button.disabled = True
        if num == 0:
            desc = "No players currently"
        else:
            desc = "Waiting Room\n"
            for i in range(num):
                desc += f"\n- {self.player_list_inhouse[i].get_name()} - {self.player_list_inhouse[i].get_role()}"
            desc += "\n\nHave enough players? Join a call!"
        embed = discord.Embed(
            title="In-House Match Lobby",
            description=f"{desc}",
            color=new_color
        )
        await interaction.message.edit(embed=embed, view=self)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command(name="glaze", aliases=["g"], help="ego boost")
async def glaze(ctx):
    user_name = ctx.author.display_name
    await ctx.send(user_name + ' is the fucking goat and no one can compare!')


@bot.command(name="flex", aliases=["f"], help="creates a flex queue for players to join")
async def flex(ctx):
    embed = discord.Embed(
        title="Flex Queue",
        description="No players currently",
        color=discord.Color.red()
    )
    view = EmbedFlex()
    await ctx.send(embed=embed, view=view)


@bot.command(name="inhouse", aliases=["ih"], help="creates an in-house lobby for players to join")
async def inhouse(ctx):
    embed = discord.Embed(
        title="In-house Match Lobby",
        description="No players currently",
        color=discord.Color.red()
    )
    view = EmbedInhouse()
    await ctx.send(embed=embed, view=view)


@bot.command(name="stats", aliases=["s"],
             help="gets head to head stats of you compared to another player, if you've played together before")
async def stats(ctx, member: discord.Member):
    # Collect the username of the mentioned person
    mentioned_user = member.mention
    username = member.name
    await ctx.send(f'You mentioned {mentioned_user}, whose username is {username}')


# class EmbedFlex(View):
#     def init(self):
#         super().init()
#         self.player_list = []
#         self.role_list = []
#         self.name_list = []
#         self.player_count = len(self.player_list)
#         self.data_file = 'flex_data.json'  # JSON file to store data
#
#         # Load data from JSON file on initialization
#         self.load_data()
#
#     # Function to save data to JSON file
#     def save_data(self):
#         data = {
#             'player_list': self.player_list,
#             'role_list': self.role_list,
#             'name_list': self.name_list
#         }
#         with open(self.data_file, 'w') as file:
#             json.dump(data, file)
#
#     # Function to load data from JSON file
#     def load_data(self):
#         try:
#             with open(self.data_file, 'r') as file:
#                 data = json.load(file)
#                 self.player_list = data.get('player_list', [])
#                 self.role_list = data.get('role_list', [])
#                 self.name_list = data.get('name_list', [])
#         except FileNotFoundError:
#             # Handle the case where the file doesn't exist yet
#             pass


# @bot.command()
# async def c(ctx):
#     await ctx.send("List of Working Commands - all called by \"?\"\n> c - lists commands\n> glaze - ego boost\n> f - creates a flex queue for players to join\n> ih - creates an in-house lobby for players to join")


bot.run('TOKEN')

'''
BACKPACK

bot.command(help="prints text formatting examples")
async def font_test(ctx):
    await ctx.send('*italic*, **bold**, ***italic and bold***, __underlined__, ~~strikethrough~~, ||spoiler||')
    await ctx.send(
        '> Time is too slow for those who wait, too swift for those who fear, too long for those who grieve, too short for those who rejoice, but for those who love, time is eternity.')


@bot.command(help="displays embed with basic text and images")
async def embed(ctx):
    embed = discord.Embed(
        title="Sample Embed",
        description="This is a sample embed message.",
        color=discord.Color.blue()
    )
    embed.add_field(name="Field 1", value="This is a value", inline=False)
    embed.add_field(name="Field 2", value="Another value", inline=True)
    embed.set_footer(text="Footer text")
    embed.set_author(name="Author Name", icon_url="https://images.wsj.net/im-976761/?width=1278&size=1")
    embed.set_thumbnail(url="https://images.wsj.net/im-976761/?width=1278&size=1")
    embed.set_image(url="https://images.wsj.net/im-976761/?width=1278&size=1")

    await ctx.send(embed=embed)


@bot.command(help="displays basic dynamic embed")
async def embed2(ctx):
    embed = discord.Embed(
        title="Dynamic Embed",
        description="This is page 1",
        color=discord.Color.blue()
    )
    view = EmbedView()
    await ctx.send(embed=embed, view=view)


'''
