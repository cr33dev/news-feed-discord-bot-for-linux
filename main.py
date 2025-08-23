# Main.py
#
# Copyright (C) 2025 Luke (cr33pkill , cr33dev) and Jack (seafer, seafer6969)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# dependencies
import discord
from discord.ext import commands
import feedparser
import requests
import asyncio
import re
from urllib.parse import urlparse

### USERS WHO MODIFY CODE BEFORE THIS POINT: BEWARE YE ARE ENTERING UNDOCUMENTED TERRITORY ###

# discord bot token, server ID, and channel ID
TOKEN = ''
GUILD =
CHANNEL_ID =
# options for customization:
titleOnly = False   # Forces embeds to only show article title (and author/pub date when possible)  (False by default)
forceList = False   # Forces emebds to always show previous stories instead of content description  (False by default)
appendList = True  # Forces feeds with valid content descriptions to also display previous stories (False by default)
refreshRate = 1800  # Determines how often the bot checks the feed list. Measured in seconds.       (1800 by default)
rssUrlList = ["https://archlinux.org/feeds/news/","https://blog.linuxmint.com/?feed=rss2","https://planet.gnu.org/rss20.xml","https://bits.debian.org/feeds/feed.rss","https://rss.slashdot.org/Slashdot/slashdotMain","https://lunduke.substack.com/feed"]

### USERS WHO MODIFY CODE BEYOND THIS POINT: BEWARE YE ARE ENTERING UNDOCUMENTED TERRITORY ###

# discord init
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix=">", intents=intents)
# rss browser skin
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    )
}
# what does this even do? - seafer6969
newestValueList = ["value","value","value","value","value","value"]
# main
async def main_function(chan_id):
    channel = client.get_channel(chan_id)
    # various variables needed for the previous story list maker
    global rssUrlList, newestValueList, previousArticlesContainer
    runLoop = True
    while runLoop:
        for i in range(len(rssUrlList)): # loop for going through all RSS feeds
            feedIndex = i
            previousArticlesContainer = [] # reset the temporary feed list
            response = requests.get(rssUrlList[feedIndex], headers=headers)
            temp = feedparser.parse(response.content)
            # loop for making previous stories list
            for entry in temp.entries[:6]:
                previousArticlesContainer.append("[" + entry.title +"]" + "(" + entry.link + ")")
            if newestValueList[feedIndex] != previousArticlesContainer[0]:
                #this will be referenced in embedFValue a lot
                embedList = "\n".join(
                        [previousArticlesContainer[1],
                         previousArticlesContainer[2],
                         previousArticlesContainer[3],
                        ]
                )
                # parse feed elements to variables usable by discord.Embed
                embedDesc = ""
                # name and assign guaranteed elements
                print(str(entry.title) + "\n" + str(entry.link))
                # check for author
                if "author" in entry:
                    embedAuthor = str(entry.author)
                    print(str(entry.author))
                else:
                    embedAuthor = ""
                    print("This feed has no author data!")
                # check for publish by date
                if "published" in entry:
                    embedPub = str(entry.published)
                    print(str(entry.published))
                else:
                    embedPub = ""
                    print("This feed has no 'published by' date data!")
                # check user configuration, check for image and description, assign variables accordingly
                if not titleOnly and not forceList:
                    if "image" in entry:
                        embedImage = str(entry.image['href'])
                        print(str(entry.image['href']))
                    else:
                        embedImage = ""
                        print("DEBUG: This feed has no image data!")
                    # ignore description data with HTML tags (we see your <p></p>)
                    if "description" in entry and "<p>" in entry.description:
                        embedFName = "Previous stories: "
                        embedFValue = embedList
                        print("DEBUG: This feed has ugly description data with HTML tags! (A list was added in its place)\n")
                    # resolve appendList
                    elif "description" in entry and appendList:
                        embedDesc = ' '.join(str(entry.description).split(' '))[:512] + '...'
                        embedFName = "Previous stories: "
                        embedFValue = embedList
                        print(' '.join(str(entry.description).split(' ')[:10]) + '...')
                        print("DEBUG: This description was provided with a previous stories list according to appendList = True.\n")
                    elif "description" in entry:
                        embedDesc = ' '.join(str(entry.description).split(' '))[:512] + '...'
                        embedFValue = ""
                        embedFName = ""
                        print(' '.join(str(entry.description).split(' ')[:10]) + '...\n')
                    # resolve empty description data (rare)
                    else:
                        embedFName = "Previous stories: "
                        embedFValue = embedList
                        print("DEBUG: This feed has no description data! (A list was added in its place)\n")
               # forceList true
                elif not titleOnly and forceList:
                    if "image" in entry:
                        embedImage = str(entry.image['href'])
                        print(str(entry.image['href']))
                    else:
                        embedImage = ""
                        print("DEBUG: This feed has no image data!")
                    embedFName = "Previous stories: "
                    embedFValue = embedList
                    print("DEBUG: forceList enabled: skipping description parse.\n")
                # titleOnly true
                elif titleOnly:
                    embedImage = ""
                    embedFName = ""
                    embedFValue = ""
                    embedDesc = ""
                    print("DEBUG: titleOnly enabled: skipping image and description.\n")

                # add default elements
                embed = discord.Embed(
                    # Universal guaranteed elements: title, link, color (from discord)
                    title="Newest story: " + str(entry.title),
                    url=str(entry.link),
                    color=discord.Color.purple(),
                    # description (if embedDesc = "" is empty, the embed simply has no description)
                    description=str(embedDesc)
                )
                # add default elements that require external declaration to discord.Embed()
                embed.set_author(name = embedAuthor)
                embed.set_footer(text = embedPub)
                # add user configured elements: image (titleOnly), text vs list (forceList, appendList)
                embed.set_image(url = embedImage)
                embed.add_field(name = embedFName, value = embedFValue)
                # identify the role for the buttons
                currentRole = feedHostList[i]
                guild = client.guilds[0]
                assignRole = discord.utils.get(guild.roles,name=currentRole)
                # this is supposed to be for changing the buttons after they're pressed: doesn't work.
#                class Subbed(discord.ui.View):
#                    @discord.ui.button(label="Subscribed", style=discord.ButtonStyle.green)
#                    async def clickedSubscribe(self, button: discord.ui.Button):
#                        button.disabled = True
#                class Unsubbed(discord.ui.View):
#                    @discord.ui.button(label="Unsubscribed", style=discord.ButtonStyle.red)
#                    async def clickedUnsubscribe(self, button: discord.ui.Button):
#                        button.disabled = True
                # make the buttons
                class Sub(discord.ui.View):
                    @discord.ui.button(label="Subscribe", style=discord.ButtonStyle.green)
                    async def clickSubscribe(self, interaction: discord.Interaction, button: discord.ui.Button):
                        await interaction.user.add_roles(assignRole)
                        await interaction.response.defer()
#                        await interaction.response.edit_message(view=Subbed())
                    @discord.ui.button(label="Unsubscribe", style=discord.ButtonStyle.red)
                    async def clickUnsubscribe(self, interaction: discord.Interaction, button: discord.ui.Button):
                        await interaction.user.remove_roles(assignRole)
                        await interaction.response.defer()
#                        await interaction.response.edit_message(view=Unsubbed())
                # ping subscriber, send embed, send buttons, reset previous stories counter.
                await channel.send(embed=embed, view=Sub())
                newestValueList[feedIndex] = previousArticlesContainer[0]
            else:
                print(f"\nINFO: No new stories from {rssUrlList[feedIndex]} for this cycle.")
        await asyncio.sleep(refreshRate)

# start bot
@client.event
async def on_ready():
    # server readout
    print("\nHello there... \n")
    print("INFO: Logged in!")
    print(f"INFO: User:         {client.user}")
    print(f"INFO: User ID:      {client.user.id}")
    print(f"INFO: Channel ID:   {CHANNEL_ID}")
    print(f"INFO: Guild ID:     {GUILD}")
    # feed checker (for role checker, maker)
    feedHost = ""
    global feedHostList #global for access in subscribtion function
    feedHostList = []
    print("\nINFO: Parsing feeds into suitable role names...")
    for j in range(len(rssUrlList)):
        hostListItem =  urlparse(rssUrlList[j])
        feedHost = hostListItem.hostname
        feedHostList.append(feedHost)
        print("----> Feed '" + str(rssUrlList[j]) + "' shortened to role name '" + str(feedHost) + "'")
    # role checker
    serverName = client.get_guild(GUILD)
    global rawServerRoleList #this is global for an experiment HEY MAYBE UNGLOBALIZE THIS IF YOU DONT NEED IT
    rawServerRoleList = serverName.roles
    roleNameList = []
    roleIDList = []
    print("\nINFO: Reading roles from server...")
    for k in range(len(rawServerRoleList)):
        roleName = rawServerRoleList[k].name
        roleID = rawServerRoleList[k].id
        roleNameList.append(roleName)
        roleIDList.append(roleID)
        print("----> Role '" + str(roleName) + "' was discovered with ID: " + str(roleID) + ".")
    # role maker
    print("\nINFO: Adding missing subscription roles to server...")
    rolesNotToMakeSet = set(feedHostList) & set(roleNameList)
    rolesNotToMakeList = list(rolesNotToMakeSet)
    rolesToMakeSet = set(feedHostList) - set(roleNameList)
    rolesToMakeList = list(rolesToMakeSet)
    for m in range(len(rolesNotToMakeList)):
        roleNotToMake = rolesNotToMakeList[m]
        print("----> Role '" + str(roleNotToMake) + "` already exists in the server; skipping...")
    for l in range(len(rolesToMakeList)):
        roleToMake = rolesToMakeList[l]
        await serverName.create_role(name=str(roleToMake), mentionable=True)
        print("----> Role '" + str(roleToMake) + "' doesn't exist in the server; adding...'")
    # options readout
    if titleOnly:   print("INFO: Option 'titleOnly' is enabled: descriptions and images won't be parsed.")
    else:           print("INFO: Option 'titleOnly' is disabled: descriptions and images will be parsed.")
    if forceList:   print("INFO: Option 'forceList' is enabled: descriptions won't be parsed.")
    else:           print("INFO: Option 'forceList' is disabled: descriptions will be parsed.")
    if appendList:  print("INFO: Option 'appendList' is enabled: 'embedList' will be shown regardless of 'entry.description' contents.")
    else:           print("INFO: Option 'appendList' is disabled: 'embedList' will only be shown if parsed description data from rss feed is faulty.")
    print("INFO: Option refreshRate is set to " + str(refreshRate) + ". Bot will scan RSS feeds every " + str(refreshRate / 60) + " minutes.")
    print("INFO: There are " + str(len(rssUrlList)) + " entries in rssUrlList.")
    print("INFO: Raw contents of rssUrlList is \n" + str(rssUrlList))
    print("\nFEED DEBUG DATA: TITLE, LINK, AUTHOR, PUBLISHED, IMAGE, DESCRIPTION:")
    # print intial information to discord channel
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("Hello there...")
        await channel.send(
            "Option: `titleOnly` is set to `" + str(titleOnly) + "`.\n" +
            "Option: `forceList` is set to `" + str(forceList) + "`.\n" +
            "Option: `appendList` is set to `" + str(appendList) + "`.\n" +
            "Option: `refreshRate` is set to `" + str(refreshRate) + "` seconds."
            )
        await channel.send("There are " + str(len(rssUrlList)) + " entries in `rssUrlList`")
        await channel.send("Raw contents of `rssUrlList` is:\n`" + str(rssUrlList) + "`")
        for n in range(len(rolesNotToMakeList)):
            await channel.send("The `" + str(rolesNotToMakeList[n] + "` role already existed in the server."))
        for o in range(len(rolesToMakeList)):
            await channel.send("The `" + str(rolesToMakeList[o]) + "` role was created in the server.")
    else:
        print(f"DEBUG: Could not find channel with ID {CHANNEL_ID}")
    asyncio.create_task(main_function(CHANNEL_ID))
client.run(TOKEN)
