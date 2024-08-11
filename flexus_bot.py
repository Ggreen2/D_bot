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
            return_me = f"{self.head2head[self.get_index(user)].stats()}"
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
        self.games_with_won = 0
        self.games_with_total = 0
        self.games_against_won = 0
        self.games_against_total = 0

    def stats(self):
        result = ""
        if self.games_with_total > 0:
            result += f"{round(((self.games_with_won / (self.games_with_total * 1.0)) * 100), 2)}% winrate while on your team ({self.games_with_won}/{self.games_with_total} games), "
        else:
            result += f"You have played no games with {self.name} on your team, "
        if self.games_against_total > 0:
            result += f"and you have {round(((self.games_against_won / (self.games_against_total * 1.0)) * 100), 2)}% winrate against them ({self.games_against_won}/{self.games_against_total} games)"
        else:
            result += f"and you have played no games against {self.name}"
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
- add the functionality to actually generate teams, decide winner, and just call the already made get_stats method, and also add the method for someone to manually enter a game's info
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
            await interaction.response.send_message("You were given the role Top Lane", ephemeral=True)
        else:
            self.player_list_flex[self.get_index_flex(new_player)].set_role(new_role)
            await interaction.response.send_message("Your role has been switched to Top Lane", ephemeral=True)
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
            await interaction.response.send_message("You were given the role Mid Lane", ephemeral=True)
        else:
            self.player_list_flex[self.get_index_flex(new_player)].set_role(new_role)
            await interaction.response.send_message("Your role has been switched to Mid Lane", ephemeral=True)
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
            await interaction.response.send_message("You were given the role Bot Lane", ephemeral=True)
        else:
            self.player_list_flex[self.get_index_flex(new_player)].set_role(new_role)
            await interaction.response.send_message("Your role has been switched to Bot Lane", ephemeral=True)
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

    def get_players_with_role(self, check_me_role):
        return_list = []
        for item in self.player_list_inhouse:
            if item.get_role() == check_me_role:
                return_list.append(item)
        return return_list

    @discord.ui.button(label="Top", style=discord.ButtonStyle.secondary, custom_id="top_role_flex")
    async def top_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = "Top"
        new_player = Player(interaction.user.name, interaction.user.display_name, new_role)
        if not check_if_exists_main(new_player):
            add_player_main(new_player)
        player_list_main[get_index_main(new_player)].set_role(new_role)
        if not self.check_if_exists_inhouse(new_player):
            self.player_list_inhouse.append(new_player)
            await interaction.response.send_message("You were given the role Top Lane", ephemeral=True)
        else:
            self.player_list_inhouse[self.get_index_inhouse(new_player)].set_role(new_role)
            await interaction.response.send_message("Your role has been switched to Top Lane", ephemeral=True)
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
            await interaction.response.send_message("You were given the role Mid Lane", ephemeral=True)
        else:
            self.player_list_inhouse[self.get_index_inhouse(new_player)].set_role(new_role)
            await interaction.response.send_message("Your role has been switched to Mid Lane", ephemeral=True)
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
            await interaction.response.send_message("You were given the role Bot Lane", ephemeral=True)
        else:
            self.player_list_inhouse[self.get_index_inhouse(new_player)].set_role(new_role)
            await interaction.response.send_message("Your role has been switched to Bot Lane", ephemeral=True)
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
        await interaction.channel.send("Game Starting!")
        await interaction.message.delete()
        await asyncio.sleep(3)
        await interaction.channel.last_message.delete()
        desc = ""
        for i in range(len(self.player_list_inhouse)):
            desc += f"\n- {self.player_list_inhouse[i].get_name()} - {self.player_list_inhouse[i].get_role()}"
        team_selection_embed = discord.Embed(title="Team Time Chaps!",
                                             description="Please select which way you'd like teams to be selected",
                                             color=discord.Color.dark_gold())
        team_selection_embed.add_field(name="Manually",
                                       value="Players decide which two players become team captains, who then pick teams in snake draft order - **IMPORTANT**: During manual captain selection, the first captain picked will be able to choose the first *player*, whilst the second captain picked will be able to choose which *side of the map* his or her team gets",
                                       inline=False)
        team_selection_embed.add_field(name="Random MMR",
                                       value="Players are split evenly into teams based on MMR calculated and held just in this server, based on past total of wins and losses",
                                       inline=False)
        team_selection_embed.add_field(name="List of Players", value=f"{desc}", inline=False)
        team_selection_embed.set_footer(text="This message is sponsored by PepsiCo")
        captain_view = EmbedInhouseTeamSelection(self.player_list_inhouse)
        await interaction.channel.send(embed=team_selection_embed, view=captain_view)

        '''
        CODE FOR NEW EMBED (chained), just gotta make a class for the little guy

        second_view = SecondView()
        embed = discord.Embed(title="Second Embed", 
                              description="Press the button below to delete this embed.",
                              color=discord.Color.green())
        await interaction.channel.send(embed=embed, view=second_view)
        '''

    async def update_embed(self, interaction: discord.Interaction):
        num = len(self.player_list_inhouse)
        if num >= 1:
            new_color = discord.Color.green()
            self.start_button.disabled = False
        else:
            new_color = discord.Color.red()
            self.start_button.disabled = True
        embed = discord.Embed(
            title="In-House Match Lobby",
            color=new_color
        )
        if num == 0:
            embed.add_field(name="", value="***No Players Currently***")
        else:
            # for i in range(num):
            #     desc += f"\n- {self.player_list_inhouse[i].get_name()} - {self.player_list_inhouse[i].get_role()}"
            top_list_ih = self.get_players_with_role("Top")
            jng_list_ih = self.get_players_with_role("Jung")
            mid_list_ih = self.get_players_with_role("Mid")
            bot_list_ih = self.get_players_with_role("Bot")
            sup_list_ih = self.get_players_with_role("Sup")
            fill_list_ih = self.get_players_with_role("Fill")
            if len(top_list_ih) == 2:
                self.top_button.disabled = True
            else:
                self.top_button.disabled = False
            if len(jng_list_ih) == 2:
                self.jng_button.disabled = True
            else:
                self.jng_button.disabled = False
            if len(mid_list_ih) == 2:
                self.mid_button.disabled = True
            else:
                self.mid_button.disabled = False
            if len(bot_list_ih) == 2:
                self.bot_button.disabled = True
            else:
                self.bot_button.disabled = False
            if len(sup_list_ih) == 2:
                self.sup_button.disabled = True
            else:
                self.sup_button.disabled = False
            if len(top_list_ih) > 0:
                p_top = ""
                for item in top_list_ih:
                    p_top += f"\n- {item.get_name()}"
                embed.add_field(name="Top Lane", value=f"{p_top}", inline=False)
            if len(jng_list_ih) > 0:
                p_jng = ""
                for item in jng_list_ih:
                    p_jng += f"\n- {item.get_name()}"
                embed.add_field(name="Jungler", value=f"{p_jng}", inline=False)
            if len(mid_list_ih) > 0:
                p_mid = ""
                for item in mid_list_ih:
                    p_mid += f"\n- {item.get_name()}"
                embed.add_field(name="Mid Lane", value=f"{p_mid}", inline=False)
            if len(bot_list_ih) > 0:
                p_bot = ""
                for item in bot_list_ih:
                    p_bot += f"\n- {item.get_name()}"
                embed.add_field(name="Bot Lane", value=f"{p_bot}", inline=False)
            if len(sup_list_ih) > 0:
                p_sup = ""
                for item in sup_list_ih:
                    p_sup += f"\n- {item.get_name()}"
                embed.add_field(name="Support", value=f"{p_sup}", inline=False)
            if len(fill_list_ih) > 0:
                p_fill = ""
                for item in fill_list_ih:
                    p_fill += f"\n- {item.get_name()}"
                embed.add_field(name="Fill", value=f"{p_fill}", inline=False)
            embed.set_footer(text="Have enough players? Hop in a call!")
        await interaction.message.edit(embed=embed, view=self)


class EmbedInhouseTeamSelection(View):
    def __init__(self, p_list):
        super().__init__(timeout=None)
        self.player_list_inhouse = p_list

    '''
    HOW WE GONNA DO DIS:

    im going to (in this order):
    make it run with manual captains
    then be able to save all data on shutdown/startup
    then add elo system

    manual captains pick snake style (i think just buttons for everyone's names tbh) maybe something else idfk

    and then

    pick players obv, if you are not the current captain allowed to be choosing, you will be sent an ephemeral msg telling you so and your pick will not go through

    once teams are picked, send a new embed (name like manual teams idk, so u can name other one random teams) that prints both teams (with red side and blue side labelled) 
    *during manual captain selection, just mention first captain picked gets first
    PLAYER selection, and then at the end of people selection, the OTHER captain gets to pick SIDES via BUTTONS (again only letting the correct captain pick a button lest the user
    be sent an ephemeral message)

    regardless of either ManualTeams or Random Teams embed used, both will call MatchResults embed at the end, displaying both teams, and each players' current elo post-update, with
    the added or subtracted amount on the side in parantheses (Ex. Drayble - 1345 (+25))
    '''

    @discord.ui.button(label="Manually Assign Teams", style=discord.ButtonStyle.primary, custom_id="manual_teams_ih")
    async def manual_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        manual_selection_embed = discord.Embed(title="Manual Team Selection",
                                               description="DECIDE THIS IN CALL AND THEN CLICK THE APPROPRIATE PLAYER'S BUTTON: The first captain picked will be able to choose the first *player*, whilst the second captain picked will be able to choose which *side of the map* his or her team gets",
                                               color=discord.Color.green())
        manual_selection_embed.add_field(name="Order of Events for Snake Draft:",
                                         value="- Captain 1 picks 1 players\n- Captain 2 picks 2 players\n- Captain 1 picks 2 players\n- Captain 2 picks 2 players (his or her team is now complete)\n- Captain 1 gets the remaining player\n- Captain 2 picks either *blue side* or *red side* for his or her team, Captain 1's team gets the other side",
                                         inline=False)
        manual_selection_embed.add_field(name="The first captain's name may now be clicked", value="", inline=False)
        manual_view = EmbedInhouseManualTeams(self.player_list_inhouse)
        await interaction.message.delete()
        await interaction.channel.send(embed=manual_selection_embed, view=manual_view)

    @discord.ui.button(label="Randomly Assign Teams", style=discord.ButtonStyle.success, disabled=True,
                       custom_id="random_teams_ih")
    async def random_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.send("random teams")


class EmbedInhouseManualTeams(View):
    def __init__(self, p_list):
        super().__init__(timeout=None)
        self.player_list_inhouse = p_list
        self.team1 = []
        self.team2 = []
        self.counter = 0

        for i in range(len(self.player_list_inhouse)):
            self.children[
                i].label = f"{self.player_list_inhouse[i].get_name()} ({self.player_list_inhouse[i].get_role()})"

    @discord.ui.button(label="Placeholder", style=discord.ButtonStyle.success, disabled=False, custom_id="p0")
    async def p0_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        button.disabled = True
        await self.update_lists(self.player_list_inhouse[0])
        await self.update_embed(interaction)

    @discord.ui.button(label="Placeholder", style=discord.ButtonStyle.success, disabled=False, custom_id="p1")
    async def p1_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        button.disabled = True
        await self.update_lists(self.player_list_inhouse[1])
        await self.update_embed(interaction)

    @discord.ui.button(label="Placeholder", style=discord.ButtonStyle.success, disabled=False, custom_id="p2")
    async def p2_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        button.disabled = True
        await self.update_lists(self.player_list_inhouse[2])
        await self.update_embed(interaction)

    @discord.ui.button(label="Placeholder", style=discord.ButtonStyle.success, disabled=False, custom_id="p3")
    async def p3_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        button.disabled = True
        await self.update_lists(self.player_list_inhouse[3])
        await self.update_embed(interaction)

    @discord.ui.button(label="Placeholder", style=discord.ButtonStyle.success, disabled=False, custom_id="p4")
    async def p4_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        button.disabled = True
        await self.update_lists(self.player_list_inhouse[4])
        await self.update_embed(interaction)

    @discord.ui.button(label="Placeholder", style=discord.ButtonStyle.success, disabled=False, custom_id="p5")
    async def p5_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        button.disabled = True
        await self.update_lists(self.player_list_inhouse[5])
        await self.update_embed(interaction)

    @discord.ui.button(label="Placeholder", style=discord.ButtonStyle.success, disabled=False, custom_id="p6")
    async def p6_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        button.disabled = True
        await self.update_lists(self.player_list_inhouse[6])
        await self.update_embed(interaction)

    @discord.ui.button(label="Placeholder", style=discord.ButtonStyle.success, disabled=False, custom_id="p7")
    async def p7_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        button.disabled = True
        await self.update_lists(self.player_list_inhouse[7])
        await self.update_embed(interaction)

    @discord.ui.button(label="Placeholder", style=discord.ButtonStyle.success, disabled=False, custom_id="p8")
    async def p8_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        button.disabled = True
        await self.update_lists(self.player_list_inhouse[8])
        await self.update_embed(interaction)

    @discord.ui.button(label="Placeholder", style=discord.ButtonStyle.success, disabled=False, custom_id="p9")
    async def p9_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        button.disabled = True
        await self.update_lists(self.player_list_inhouse[9])
        await self.update_embed(interaction)

    async def update_lists(self, choice):
        if self.counter == 0:
            self.team1.append(choice)
        elif self.counter == 1:
            self.team2.append(choice)
        elif self.counter == 2:
            self.team1.append(choice)
        elif self.counter == 3:
            self.team2.append(choice)
        elif self.counter == 4:
            self.team2.append(choice)
        elif self.counter == 5:
            self.team1.append(choice)
        elif self.counter == 6:
            self.team1.append(choice)
        elif self.counter == 7:
            self.team2.append(choice)
        elif self.counter == 8:
            self.team2.append(choice)
        elif self.counter == 9:
            self.team1.append(choice)
        else:
            pass

    async def update_embed(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Manual Team Selection",
            description=f"",
            color=discord.Color.blue() if self.counter % 2 == 0 else discord.Color.red()
        )
        '''
        Captain 1 picks 1 players
        Captain 2 picks 2 players
        Captain 1 picks 2 players
        Captain 2 picks 2 players (his or her team is now complete)
        Captain 1 gets the remaining player
        Captain 2 picks either blue side or red side for his or her team, Captain 1's team gets the other side
        '''
        if self.counter == 0:
            embed.add_field(name=f"Team {self.team1[0].get_name()}",
                            value=f"{self.team1[0].get_name()} - {self.team1[0].get_role()}", inline=False)
            embed.add_field(name=f"The second captain's name may now be clicked", value="", inline=False)
        elif self.counter == 1:
            embed.add_field(name=f"Team {self.team1[0].get_name()}",
                            value=f"{self.team1[0].get_name()} - {self.team1[0].get_role()}", inline=False)
            embed.add_field(name=f"Team {self.team2[0].get_name()}",
                            value=f"{self.team2[0].get_name()} - {self.team2[0].get_role()}", inline=False)
            embed.add_field(name=f"{self.team1[0].get_name()} may now pick a player", value="", inline=False)
        elif self.counter == 2:
            embed.add_field(name=f"Team {self.team1[0].get_name()}",
                            value=f"{self.team1[0].get_name()} - {self.team1[0].get_role()}\n{self.team1[1].get_name()} - {self.team1[1].get_role()}",
                            inline=False)
            embed.add_field(name=f"Team {self.team2[0].get_name()}",
                            value=f"{self.team2[0].get_name()} - {self.team2[0].get_role()}", inline=False)
            embed.add_field(name=f"{self.team2[0].get_name()} may now pick a player", value="", inline=False)
        elif self.counter == 3:
            embed.add_field(name=f"Team {self.team1[0].get_name()}",
                            value=f"{self.team1[0].get_name()} - {self.team1[0].get_role()}\n{self.team1[1].get_name()} - {self.team1[1].get_role()}",
                            inline=False)
            embed.add_field(name=f"Team {self.team2[0].get_name()}",
                            value=f"{self.team2[0].get_name()} - {self.team2[0].get_role()}\n{self.team2[1].get_name()} - {self.team2[1].get_role()}",
                            inline=False)
            embed.add_field(name=f"{self.team2[0].get_name()} may now pick another player", value="", inline=False)
        elif self.counter == 4:
            embed.add_field(name=f"Team {self.team1[0].get_name()}",
                            value=f"{self.team1[0].get_name()} - {self.team1[0].get_role()}\n{self.team1[1].get_name()} - {self.team1[1].get_role()}",
                            inline=False)
            embed.add_field(name=f"Team {self.team2[0].get_name()}",
                            value=f"{self.team2[0].get_name()} - {self.team2[0].get_role()}\n{self.team2[1].get_name()} - {self.team2[1].get_role()}\n{self.team2[2].get_name()} - {self.team2[2].get_role()}",
                            inline=False)
            embed.add_field(name=f"{self.team1[0].get_name()} may now pick a player", value="", inline=False)
        elif self.counter == 5:
            embed.add_field(name=f"Team {self.team1[0].get_name()}",
                            value=f"{self.team1[0].get_name()} - {self.team1[0].get_role()}\n{self.team1[1].get_name()} - {self.team1[1].get_role()}\n{self.team1[2].get_name()} - {self.team1[2].get_role()}",
                            inline=False)
            embed.add_field(name=f"Team {self.team2[0].get_name()}",
                            value=f"{self.team2[0].get_name()} - {self.team2[0].get_role()}\n{self.team2[1].get_name()} - {self.team2[1].get_role()}\n{self.team2[2].get_name()} - {self.team2[2].get_role()}",
                            inline=False)
            embed.add_field(name=f"{self.team1[0].get_name()} may now pick another player", value="", inline=False)
        elif self.counter == 6:
            embed.add_field(name=f"Team {self.team1[0].get_name()}",
                            value=f"{self.team1[0].get_name()} - {self.team1[0].get_role()}\n{self.team1[1].get_name()} - {self.team1[1].get_role()}\n{self.team1[2].get_name()} - {self.team1[2].get_role()}\n{self.team1[3].get_name()} - {self.team1[3].get_role()}",
                            inline=False)
            embed.add_field(name=f"Team {self.team2[0].get_name()}",
                            value=f"{self.team2[0].get_name()} - {self.team2[0].get_role()}\n{self.team2[1].get_name()} - {self.team2[1].get_role()}\n{self.team2[2].get_name()} - {self.team2[2].get_role()}",
                            inline=False)
            embed.add_field(name=f"{self.team2[0].get_name()} may now pick a player", value="", inline=False)
        elif self.counter == 7:
            embed.add_field(name=f"Team {self.team1[0].get_name()}",
                            value=f"{self.team1[0].get_name()} - {self.team1[0].get_role()}\n{self.team1[1].get_name()} - {self.team1[1].get_role()}\n{self.team1[2].get_name()} - {self.team1[2].get_role()}\n{self.team1[3].get_name()} - {self.team1[3].get_role()}",
                            inline=False)
            embed.add_field(name=f"Team {self.team2[0].get_name()}",
                            value=f"{self.team2[0].get_name()} - {self.team2[0].get_role()}\n{self.team2[1].get_name()} - {self.team2[1].get_role()}\n{self.team2[2].get_name()} - {self.team2[2].get_role()}\n{self.team2[3].get_name()} - {self.team2[3].get_role()}",
                            inline=False)
            embed.add_field(name=f"{self.team2[0].get_name()} may now pick another player", value="", inline=False)
        elif self.counter == 8:
            embed.add_field(name=f"Team {self.team1[0].get_name()}",
                            value=f"{self.team1[0].get_name()} - {self.team1[0].get_role()}\n{self.team1[1].get_name()} - {self.team1[1].get_role()}\n{self.team1[2].get_name()} - {self.team1[2].get_role()}\n{self.team1[3].get_name()} - {self.team1[3].get_role()}",
                            inline=False)
            embed.add_field(name=f"Team {self.team2[0].get_name()}",
                            value=f"{self.team2[0].get_name()} - {self.team2[0].get_role()}\n{self.team2[1].get_name()} - {self.team2[1].get_role()}\n{self.team2[2].get_name()} - {self.team2[2].get_role()}\n{self.team2[3].get_name()} - {self.team2[3].get_role()}\n{self.team2[4].get_name()} - {self.team2[4].get_role()}",
                            inline=False)
            embed.add_field(
                name=f"Please click the final player's button to be added to Team {self.team1[0].get_name()}", value="",
                inline=False)
        elif self.counter == 9:
            embed.add_field(name=f"Team {self.team1[0].get_name()}",
                            value=f"{self.team1[0].get_name()} - {self.team1[0].get_role()}\n{self.team1[1].get_name()} - {self.team1[1].get_role()}\n{self.team1[2].get_name()} - {self.team1[2].get_role()}\n{self.team1[3].get_name()} - {self.team1[3].get_role()}\n{self.team1[4].get_name()} - {self.team1[4].get_role()}",
                            inline=False)
            embed.add_field(name=f"Team {self.team2[0].get_name()}",
                            value=f"{self.team2[0].get_name()} - {self.team2[0].get_role()}\n{self.team2[1].get_name()} - {self.team2[1].get_role()}\n{self.team2[2].get_name()} - {self.team2[2].get_role()}\n{self.team2[3].get_name()} - {self.team2[3].get_role()}\n{self.team2[4].get_name()} - {self.team2[4].get_role()}",
                            inline=False)
        else:
            pass
        self.counter += 1
        await interaction.message.edit(embed=embed, view=self)
        if self.counter == 9:
            manual_selection_embed = discord.Embed(title="In-House Current Match",
                                                   description="Click the appropriate button to determine match winner, click multiple times for multiple matches",
                                                   color=discord.Color.green())
            embed.add_field(name=f"Team {self.team1[0].get_name()}",
                            value=f"{self.team1[0].get_name()} - {self.team1[0].get_role()}\n{self.team1[1].get_name()} - {self.team1[1].get_role()}\n{self.team1[2].get_name()} - {self.team1[2].get_role()}\n{self.team1[3].get_name()} - {self.team1[3].get_role()}\n{self.team1[4].get_name()} - {self.team1[4].get_role()}")
            embed.add_field(name=f"Team {self.team2[0].get_name()}",
                            value=f"{self.team2[0].get_name()} - {self.team2[0].get_role()}\n{self.team2[1].get_name()} - {self.team2[1].get_role()}\n{self.team2[2].get_name()} - {self.team2[2].get_role()}\n{self.team2[3].get_name()} - {self.team2[3].get_role()}\n{self.team2[4].get_name()} - {self.team2[4].get_role()}")
            manual_view = EmbedInhouseMatch(self.player_list_inhouse)
            await interaction.message.delete()
            await interaction.channel.send(embed=manual_selection_embed, view=manual_view)


class EmbedInhouseMatch(View):
    def __init__(self, team1, team2):
        super().__init__(timeout=None)
        self.team1 = team1
        self.team2 = team2

        self.children[0].label = f"Team {self.team1[0].get_name()} Won"
        self.children[1].label = f"Team {self.team2[0].get_name()} Won"

    @discord.ui.button(label="Placeholder", style=discord.ButtonStyle.success, disabled=False, custom_id="team1_wins")
    async def team1_wins_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.send(f"Team {self.team1[0].get_name()} Won")

    @discord.ui.button(label="Placeholder", style=discord.ButtonStyle.success, disabled=False, custom_id="team2_wins")
    async def team2_wins_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.send(f"Team {self.team2[0].get_name()} Won")


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
        color=discord.Color.red()
    )
    embed.add_field(name="", value="***No Players Currently***")
    view = EmbedInhouse()
    await ctx.send(embed=embed, view=view)


@bot.command(name="stats", aliases=["s"],
             help="gets head to head stats of you compared to as many players as you want, if you've played together before")
async def stats(ctx, *members: discord.Member):
    if not members:
        await ctx.send(
            "Hey halfwit, you used this command incorrectly. Please @ at least one person in the server to get your head-to-head stats about them!")
        return
    # Collect the user and name of person who typed command
    call_user = ctx.author.name
    call_name = ctx.author.display_name
    call_pfp = ctx.author.avatar.url
    # Collect the user and name of person who got @'ed
    mentioned_users = [member.name for member in members]
    mentioned_names = [member.display_name for member in members]
    total_mentioned_users = len(members)
    new_player = Player(call_user, call_name)
    if not check_if_exists_main(new_player):
        add_player_main(new_player)
    index = get_index_main(new_player)
    embed = discord.Embed(
        title=f"{call_name} Head to Head Stats",
        color=discord.Color.gold()
    )
    for i in range(total_mentioned_users):
        embed.add_field(name=f"{mentioned_names[i]}",
                        value=f"{player_list_main[index].get_stats(mentioned_users[i], mentioned_names[i])}",
                        inline=False)
    embed.set_thumbnail(url=call_pfp)
    await ctx.send(embed=embed)


@bot.command(name="roll", help="Returns the display names of the mentioned users.")
async def roll(ctx, *members: discord.Member):
    if not members:
        await ctx.send("Please mention at least one user.")
        return

    # Collect display names of all mentioned users
    names = [member.display_name for member in members]

    # Send the collected names as a message
    await ctx.send(f"Mentioned users: {', '.join(names)}")


@bot.command()
async def magic_trick(ctx):
    embed = discord.Embed(
        title="Fuck you,",
        description="lil bitch",
        color=discord.Color.dark_red()
    )
    message = await ctx.send(embed=embed)
    await message.delete(delay=3)  # Deletes the message after 5 seconds


class DeleteView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.danger)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()


@bot.command()
async def delete_embed(ctx):
    embed = discord.Embed(
        title="Self-deleting Embed",
        description="This embed will be deleted when you press the button.",
        color=discord.Color.red()
    )
    view = DeleteView()
    await ctx.send(embed=embed, view=view)


@bot.command()
async def player_list(ctx):
    for i in range(len(player_list_main)):
        await ctx.send(f"{player_list_main[i].get_name()}")


@bot.command()
async def aids(ctx, member: discord.Member):
    call_user = ctx.author.name
    call_name = ctx.author.display_name
    mentioned_user = member.name
    mentioned_name = member.display_name
    new_player = Player(call_user, call_name)
    if not check_if_exists_main(new_player):
        add_player_main(new_player)
    index = get_index_main(new_player)
    player_list_main[index].update_head2head(mentioned_user, mentioned_name, True, True)
    player_list_main[index].update_head2head(mentioned_user, mentioned_name, True, False)
    player_list_main[index].update_head2head(mentioned_user, mentioned_name, False, True)
    player_list_main[index].update_head2head(mentioned_user, mentioned_name, False, False)
    await ctx.send("cocknballs")


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
