import discord
from discord.ext import commands
from discord.ui import Button, View
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
flex_list = []

'''
User's name on the server - interaction.user.display_name
'''


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


class EmbedFlex(View):
    def __init__(self):
        super().__init__()
        self.player_list = []
        self.role_list = []
        self.name_list = []
        self.player_count = len(self.player_list)

    @discord.ui.button(label="Top", style=discord.ButtonStyle.success, custom_id="top_role_flex")
    async def top_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = 'Top Laner'
        user = interaction.user.name
        if user not in self.player_list:
            self.player_list.append(user)
            self.role_list.append(new_role)
            await interaction.response.send_message("You were given the role Top", ephemeral=True)
        else:
            index = self.player_list.index(user)
            self.role_list[index] = new_role
            await interaction.response.send_message("Your role has been switched to Top", ephemeral=True)
        name = interaction.user.display_name
        if name not in self.name_list:
            self.name_list.append(name)
        await self.update_embed(interaction)

    @discord.ui.button(label="Jungle", style=discord.ButtonStyle.success, custom_id="jng_role_flex")
    async def jng_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = 'Jungler'
        user = interaction.user.name
        if user not in self.player_list:
            self.player_list.append(user)
            self.role_list.append(new_role)
            await interaction.response.send_message("You were given the role Jungle", ephemeral=True)
        else:
            index = self.player_list.index(user)
            self.role_list[index] = new_role
            await interaction.response.send_message("Your role has been switched to Jungle", ephemeral=True)
        name = interaction.user.display_name
        if name not in self.name_list:
            self.name_list.append(name)
        await self.update_embed(interaction)

    @discord.ui.button(label="Middle", style=discord.ButtonStyle.success, custom_id="mid_role_flex")
    async def mid_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = 'Mid Laner'
        user = interaction.user.name
        if user not in self.player_list:
            self.player_list.append(user)
            self.role_list.append(new_role)
            await interaction.response.send_message("You were given the role Middle", ephemeral=True)
        else:
            index = self.player_list.index(user)
            self.role_list[index] = new_role
            await interaction.response.send_message("Your role has been switched to Middle", ephemeral=True)
        name = interaction.user.display_name
        if name not in self.name_list:
            self.name_list.append(name)
        await self.update_embed(interaction)

    @discord.ui.button(label="Bottom", style=discord.ButtonStyle.success, custom_id="bot_role_flex")
    async def bot_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = 'Bot Laner'
        user = interaction.user.name
        if user not in self.player_list:
            self.player_list.append(user)
            self.role_list.append(new_role)
            await interaction.response.send_message("You were given the role Bottom", ephemeral=True)
        else:
            index = self.player_list.index(user)
            self.role_list[index] = new_role
            await interaction.response.send_message("Your role has been switched to Bottom", ephemeral=True)
        name = interaction.user.display_name
        if name not in self.name_list:
            self.name_list.append(name)
        await self.update_embed(interaction)

    @discord.ui.button(label="Support", style=discord.ButtonStyle.success, custom_id="sup_role_flex")
    async def sup_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = 'Support'
        user = interaction.user.name
        if user not in self.player_list:
            self.player_list.append(user)
            self.role_list.append(new_role)
            await interaction.response.send_message("You were given the role Support", ephemeral=True)
        else:
            index = self.player_list.index(user)
            self.role_list[index] = new_role
            await interaction.response.send_message("Your role has been switched to Support", ephemeral=True)
        name = interaction.user.display_name
        if name not in self.name_list:
            self.name_list.append(name)
        await self.update_embed(interaction)

    @discord.ui.button(label="Fill", style=discord.ButtonStyle.primary, custom_id="fill_role_flex")
    async def fill_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = 'Fill'
        user = interaction.user.name
        if user not in self.player_list:
            self.player_list.append(user)
            self.role_list.append(new_role)
            await interaction.response.send_message("You were given the role Fill", ephemeral=True)
        else:
            index = self.player_list.index(user)
            self.role_list[index] = new_role
            await interaction.response.send_message("Your role has been switched to Fill", ephemeral=True)
        name = interaction.user.display_name
        if name not in self.name_list:
            self.name_list.append(name)
        await self.update_embed(interaction)

    @discord.ui.button(label="Leave Queue", style=discord.ButtonStyle.danger, custom_id="leave_flex")
    async def leave_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user.name
        if user not in self.player_list:
            await interaction.response.send_message("You were not in the queue", ephemeral=True)
        else:
            index = self.player_list.index(user)
            self.player_list.remove(user)
            del self.role_list[index]
            del self.name_list[index]
            await interaction.response.send_message("You have been removed from the queue", ephemeral=True)
        await self.update_embed(interaction)

    async def update_embed(self, interaction: discord.Interaction):
        num = len(self.player_list)
        if num >= 5:
            new_color = discord.Color.green()
        else:
            new_color = discord.Color.red()
        if num == 0:
            desc = "No players currently"
        else:
            desc = "Players currently waiting to play flex queue with others\n"
            for i in range(num):
                desc += f"\n- {self.name_list[i]} - {self.role_list[i]}"
            desc += "\n\nHave enough players? Join a call!"
        embed = discord.Embed(
            title="Flex Queue",
            description=f"{desc}",
            color=new_color
        )
        await interaction.message.edit(embed=embed, view=self)


class EmbedInhouse(View):
    def __init__(self):
        super().__init__()
        self.player_list_main = []
        self.role_list_main = []
        self.name_list_main = []
        self.player_list_b = []
        self.role_list_b = []
        self.name_list_b = []
        self.player_list_r = []
        self.role_list_r = []
        self.name_list_r = []

    @discord.ui.button(label="Top", style=discord.ButtonStyle.secondary, custom_id="top_role_ih")
    async def top_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = 'Top Laner'
        user = interaction.user.name
        if user not in self.player_list_main:
            self.player_list_main.append(user)
            self.role_list_main.append(new_role)
            await interaction.response.send_message("You were given the role Top", ephemeral=True)
        else:
            index = self.player_list_main.index(user)
            self.role_list_main[index] = new_role
            await interaction.response.send_message("Your role has been switched to Top", ephemeral=True)
        name = interaction.user.display_name
        if name not in self.name_list_main:
            self.name_list_main.append(name)
        await self.update_embed(interaction)

    @discord.ui.button(label="Jungle", style=discord.ButtonStyle.secondary, custom_id="jng_role_ih")
    async def jng_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = 'Jungler'
        user = interaction.user.name
        if user not in self.player_list_main:
            self.player_list_main.append(user)
            self.role_list_main.append(new_role)
            await interaction.response.send_message("You were given the role Jungle", ephemeral=True)
        else:
            index = self.player_list_main.index(user)
            self.role_list_main[index] = new_role
            await interaction.response.send_message("Your role has been switched to Jungle", ephemeral=True)
        name = interaction.user.display_name
        if name not in self.name_list_main:
            self.name_list_main.append(name)
        await self.update_embed(interaction)

    @discord.ui.button(label="Middle", style=discord.ButtonStyle.secondary, custom_id="mid_role_ih")
    async def mid_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = 'Mid Laner'
        user = interaction.user.name
        if user not in self.player_list_main:
            self.player_list_main.append(user)
            self.role_list_main.append(new_role)
            await interaction.response.send_message("You were given the role Middle", ephemeral=True)
        else:
            index = self.player_list_main.index(user)
            self.role_list_main[index] = new_role
            await interaction.response.send_message("Your role has been switched to Middle", ephemeral=True)
        name = interaction.user.display_name
        if name not in self.name_list_main:
            self.name_list_main.append(name)
        await self.update_embed(interaction)

    @discord.ui.button(label="Bottom", style=discord.ButtonStyle.secondary, custom_id="bot_role_ih")
    async def bot_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = 'Bot Laner'
        user = interaction.user.name
        if user not in self.player_list_main:
            self.player_list_main.append(user)
            self.role_list_main.append(new_role)
            await interaction.response.send_message("You were given the role Bottom", ephemeral=True)
        else:
            index = self.player_list_main.index(user)
            self.role_list_main[index] = new_role
            await interaction.response.send_message("Your role has been switched to Bottom", ephemeral=True)
        name = interaction.user.display_name
        if name not in self.name_list_main:
            self.name_list_main.append(name)
        await self.update_embed(interaction)

    @discord.ui.button(label="Support", style=discord.ButtonStyle.secondary, custom_id="sup_role_ih")
    async def sup_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = 'Support'
        user = interaction.user.name
        if user not in self.player_list_main:
            self.player_list_main.append(user)
            self.role_list_main.append(new_role)
            await interaction.response.send_message("You were given the role Support", ephemeral=True)
        else:
            index = self.player_list_main.index(user)
            self.role_list_main[index] = new_role
            await interaction.response.send_message("Your role has been switched to Support", ephemeral=True)
        name = interaction.user.display_name
        if name not in self.name_list_main:
            self.name_list_main.append(name)
        await self.update_embed(interaction)

    @discord.ui.button(label="Fill", style=discord.ButtonStyle.secondary, custom_id="fill_role_ih")
    async def fill_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        new_role = 'Fill'
        user = interaction.user.name
        if user not in self.player_list_main:
            self.player_list_main.append(user)
            self.role_list_main.append(new_role)
            await interaction.response.send_message("You were given the role Fill", ephemeral=True)
        else:
            index = self.player_list_main.index(user)
            self.role_list_main[index] = new_role
            await interaction.response.send_message("Your role has been switched to Fill", ephemeral=True)
        name = interaction.user.display_name
        if name not in self.name_list_main:
            self.name_list_main.append(name)
        await self.update_embed(interaction)

    @discord.ui.button(label="Leave Queue", style=discord.ButtonStyle.danger, custom_id="leave_ih")
    async def leave_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user.name
        if user not in self.player_list_main:
            await interaction.response.send_message("You were not in the queue", ephemeral=True)
        else:
            index = self.player_list_main.index(user)
            self.player_list_main.remove(user)
            del self.role_list_main[index]
            del self.name_list_main[index]
            await interaction.response.send_message("You have been removed from the queue", ephemeral=True)
        await self.update_embed(interaction)

    @discord.ui.button(label="Start Match", style=discord.ButtonStyle.success, disabled=True, custom_id="start_ih")
    async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user.name
        if user not in self.player_list_main:
            await interaction.response.send_message("You were not in the queue", ephemeral=True)
        else:
            index = self.player_list_main.index(user)
            self.player_list_main.remove(user)
            del self.role_list_main[index]
            del self.name_list_main[index]
            await interaction.response.send_message("You have been removed from the queue", ephemeral=True)
        await self.update_embed(interaction)

    async def update_embed(self, interaction: discord.Interaction):
        num = len(self.player_list_main)
        if num >= 1:
            new_color = discord.Color.green()
            # self.add_item(StartButton(7))
            self.start_button.disabled = False
        else:
            new_color = discord.Color.red()
        if num == 0:
            desc = "No players currently"
            self.start_button.disabled = True
        else:
            desc = "Waiting Room\n"
            for i in range(num):
                desc += f"\n- {self.name_list_main[i]} - {self.role_list_main[i]}"
            desc += "\n\nHave enough players? Join a call!"
        embed = discord.Embed(
            title="In-house Match Lobby",
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


class ToggleView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.first_button_visible = True

        self.first_button = discord.ui.Button(label="Show Second Button", style=discord.ButtonStyle.primary)
        self.second_button = discord.ui.Button(label="Show First Button", style=discord.ButtonStyle.primary)

        self.first_button.callback = self.first_button_callback
        self.second_button.callback = self.second_button_callback

        self.add_item(self.first_button)
        self.add_item(self.second_button)
        self.update_buttons()

    def update_buttons(self):
        self.first_button.disabled = not self.first_button_visible
        self.second_button.disabled = self.first_button_visible

    async def first_button_callback(self, interaction: discord.Interaction):
        self.first_button_visible = False
        self.update_buttons()
        await interaction.response.edit_message(view=self)

    async def second_button_callback(self, interaction: discord.Interaction):
        self.first_button_visible = True
        self.update_buttons()
        await interaction.response.edit_message(view=self)


@bot.command(name="toggle_buttons", help="Displays an embed with toggleable buttons.")
async def toggle_buttons(ctx):
    view = ToggleView()
    embed = discord.Embed(
        title="Toggle Buttons",
        description="Click the buttons to toggle their visibility.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=view)


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
