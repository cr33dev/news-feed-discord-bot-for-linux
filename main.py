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

### USERS WHO MODIFY CODE BEFORE THIS POINT: BEWARE YE ARE ENTERING UNDOCUMENTED TERRITORY ###

# discord bot token, server ID, and channel ID
TOKEN = ''
GUILD =
CHANNEL_ID =
# options for customization:
titleOnly = False   # Forces embeds to only show article title (and author/pub date when possible)  (False by default)
forceList = False   # Forces emebds to always show previous stories instead of content description  (False by default)
appendList = False  # Forces feeds with valid content descriptions to also display previous stories (False by default)
refreshRate = 1800  # Determines how often the bot checks the feed list. Measured in seconds.       (1800 by default)

### USERS WHO MODIFY CODE BEYOND THIS POINT: BEWARE YE ARE ENTERING UNDOCUMENTED TERRITORY ###

# discord init
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)
# rss browser skin
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    )
}
# add RSS feed links. MUST BE A URL POINTING DIRECTLY TO RSS FEED OR ELSE IT WON'T WORK.
rss_url_list = ["https://archlinux.org/feeds/news/","https://blog.linuxmint.com/?feed=rss2","https://planet.gnu.org/rss20.xml","https://bits.debian.org/feeds/feed.rss","https://rss.slashdot.org/Slashdot/slashdotMain","https://lunduke.substack.com/feed"]
# what does this even do? - seafer6969
newest_value_list = ["value","value","value","value","value","value"]
# main
async def main_function(chan_id):
    channel = client.get_channel(chan_id)
    # various variables needed for the previous story list maker
    global rss_url_list, newest_value_list, temp_all_feed_list
    loop_allways_active = True
    while loop_allways_active:
        for i in range(len(rss_url_list)): # loop for going through all RSS feeds
            index_number = i
            temp_all_feed_list = [] # reset the temporary feed list
            response = requests.get(rss_url_list[index_number], headers=headers)
            temp = feedparser.parse(response.content)
            # lopp for making previous stories list
            for entry in temp.entries[:6]:
                temp_all_feed_list.append("[" + entry.title +"]" + "(" + entry.link + ")")
            if newest_value_list[index_number] != temp_all_feed_list[0]:
                #this will be referenced in embedFValue a lot
                embedList = "\n".join(
                        [temp_all_feed_list[1],
                         temp_all_feed_list[2],
                         temp_all_feed_list[3],
                        ]
                )
                # parse feed elements to variables usable by discord.Embed
                embedImage = ""
                embedAuthor = ""
                embedPub = ""
                embedFValue = ""
                embedFName = ""
                embedDesc = ""
                # name and assign guaranteed elements
                print(str(entry.title) + "\n" + str(entry.link))
                # check for author
                try:
                    if "author" in entry:
                        embedAuthor = str(entry.author)
                        print(str(entry.author))
                except:
                    embedAuthor = ""
                    print("This feed has no author data!")
                # check for publish by date
                try:
                    if "published" in entry:
                        embedPub = str(entry.published)
                        print(str(entry.published))
                except:
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
                embed.set_footer(text = embedPub )
                # add user configured elements: image (titleOnly), text vs list (forceList, appendList)
                embed.set_image(url = embedImage)
                embed.add_field(name = embedFName, value = embedFValue)
                # send message, reset previous stories counter.
                await channel.send(embed=embed)
                newest_value_list[index_number] = temp_all_feed_list[0]
            else:
                print(f"nothing to add for {rss_url_list[index_number]}")
        await asyncio.sleep(refreshRate)
# start bot
@client.event
async def on_ready():
    # print initial information to console
    print("\nHello there... \n")
    print("INFO: Logged in")
    print(f"INFO: User: {client.user}")
    print(f"INFO: ID: {client.user.id}")
    print(f"INFO: Channel ID: {client.user.id}\n")
    if titleOnly:   print("DEBUG: Option 'titleOnly' is enabled: descriptions and images won't be parsed!")
    if forceList:   print("DEBUG: Option 'forceList' is enabled: descriptions won't be parsed!")
    if appendList:  print("DEBUG: Option 'appendList' is enabled: 'embedList' will be shown regardless of 'entry.description' contents!")
    print("DEBUG: Option refreshRate is set to " + str(refreshRate) + ". Bot will scan RSS feeds every " + str(refreshRate / 60) + " minutes!")
    print("\nThere are " + str(len(rss_url_list)) + " entries in rss_url_list.")
    print("Raw contents of rss_url_list is \n" + str(rss_url_list))
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
        await channel.send("There are " + str(len(rss_url_list)) + " entries in `rss_url_list`")
        await channel.send("Raw contents of `rss_url_list` is:\n`" + str(rss_url_list) + "`")
    else:
        print(f"DEBUG: Could not find channel with ID {CHANNEL_ID}")
    asyncio.create_task(main_function(CHANNEL_ID))
client.run(TOKEN)
