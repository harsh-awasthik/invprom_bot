import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True  # Required to detect member join events

bot = commands.Bot(command_prefix='!', intents=intents)


invites_data = {}

special_invite_code = "INVITE_CODE" 

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
    # Cache invites for all guilds
    for guild in bot.guilds:
        invites_data[guild.id] = await guild.invites()
    print('Cached invites for all servers.')

@bot.event
async def on_member_join(member):
    # Fetch updated invites for the guild
    new_invites = await member.guild.invites()
    old_invites = invites_data[member.guild.id]

    for invite in old_invites:
        if invite.uses < get_invite(new_invites, invite.code).uses:
            if invite.code == special_invite_code:
                print("Starting to take action...")
                await action(member)
                print("Person Promoted successfully...")
                break

    # Update the cached invites
    invites_data[member.guild.id] = new_invites

def get_invite(invites, code):

    for invite in invites:
        if invite.code == code:
            return invite
    return None

async def action(member):
    role_to_be_assigned = "ENTER_THE_ROLE_TO_BE_ASSIGNED"

    await member.send(f"Welcome, {member.name}! You joined using a special invite link! And you're promoted to {role_to_be_assigned}")
    
    role = discord.utils.get(member.guild.roles, name=role_to_be_assigned)
    if role:
        await member.add_roles(role)

    print(f'Action completed for {member.name}')

bot.run('ENTER_BOT_KEY')
