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


# imports obv
import discord
from discord.ext import commands
import feedparser
import requests
import asyncio

# variable setting to start

# do not fricking show to people (bot token and server ids)

# token of the bot you want it to run of (duhh) keep the fricking quotes
TOKEN = ''
# the guild its in (server id) backwards compatability forces this (old codebases grrrr)
GUILD =
# channel you want the damn updates in (maybe or maybe) (im tired rn)
CHANNEL_ID =

# dumb intents (you have to have this for some reason)
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)

# for picky rss requests
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    )
}


# RSS FEEDS - for help adding refer to the documentation pdf

# Add the RSS link below
rss_url_list = ["https://archlinux.org/feeds/news/","https://blog.linuxmint.com/?feed=rss2","https://planet.gnu.org/rss20.xml","https://bits.debian.org/feeds/feed.rss","https://rss.slashdot.org/Slashdot/slashdotMain","https://lunduke.substack.com/feed"]
# add RSS "Values" here
newest_value_list = ["value","value","value","value","value","value"]
# add titles here
titles = ["Latest Package Updates: Arch-Linux","Latest Package Updates: Linux-Mint","Latest Package Updates: planet-Linux","Latest Package Updates: Debian","Latest News: slashdot","Latest News: lunduke"]


# will store the links temperately before they are outputted (Do NOT change)
temp_all_feed_list = []

# main function function (ik that's a mouth-full) (im not explaining all this)

async def main_function(chan_id):
    channel = client.get_channel(chan_id)
    global rss_url_list, newest_value_list, temp_all_feed_list, titles
    loop_allways_active = True
    while loop_allways_active:
        for i in range(len(rss_url_list)):
            index_number = i
            temp_all_feed_list = [] # reset the temporary feed list
            response = requests.get(rss_url_list[index_number], headers=headers)
            temp = feedparser.parse(response.content)
            for entry in temp.entries[:6]:
                temp_all_feed_list.append(entry.link)
            if newest_value_list[index_number] != temp_all_feed_list[0]:
                title = titles[index_number]
                line1 = "Newest"
                line3 = "Past"
                embed_description = "\n".join(
                    [line1, temp_all_feed_list[0], line3, temp_all_feed_list[1], temp_all_feed_list[2],temp_all_feed_list[3], temp_all_feed_list[4], temp_all_feed_list[5]])
                embed = discord.Embed(
                    title=title,
                    color=discord.Color.red(),
                    description=embed_description
                )
                # send the embed
                await channel.send(embed=embed)
                newest_value_list[index_number] = temp_all_feed_list[0]

                # prints data in terminal ( to disable hash till the next comment)
                # print(title)
                # print(line1)
                # print(temp_all_feed_list[0])
                # print(line3)
                # print(temp_all_feed_list[1])
                # print(temp_all_feed_list[2])
                # print(temp_all_feed_list[3])
                # print(temp_all_feed_list[4])
                # print(temp_all_feed_list[5])
                # the next comment
            else:
                print(f"nothing to add for {titles[index_number]}")
        await asyncio.sleep(1800)

# start when bot ready
@client.event
async def on_ready():
    print("Logged in")
    print(f"User: {client.user}")
    print(f"ID: {client.user.id}")
    print(f"Channel ID: {client.user.id}")

    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("Hello! I'm online and ready to go!")
    else:
        print(f"❌ Could not find channel with ID {CHANNEL_ID}")
    asyncio.create_task(main_function(CHANNEL_ID))
client.run(TOKEN)
# this is a comment im adding to make sure i have git setup on my computer
