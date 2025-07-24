# MIT License
#
# Copyright (c) 2025 Cr33dev , Cr33pkill , Luke
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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

# yes I know I could have done this better, this is the first version so don't expect too much (it all damn well works)

#arch
arch_newest_actual = "value"
arch_rss_url = "https://archlinux.org/feeds/news/"
arch_all_feed_list = []
#mint
mint_newest_actual = "value"
mint_rss_url = "https://blog.linuxmint.com/?feed=rss2"
mint_all_feed_list = []
#planet gnu
planet_newest_actual = "value"
planet_rss_url = "https://planet.gnu.org/rss20.xml"
planet_all_feed_list = []
#debian
debian_newest_actual = "value"
debian_rss_url = "https://bits.debian.org/feeds/atom.xml"
debian_all_feed_list = []
#slashdot
slashdot_newest_actual = "value"
slashdot_rss_url = "http://rss.slashdot.org/Slashdot/slashdotMain"
slashdot_all_feed_list = []
#lunduke
lunduke_newest_actual = "value"
lunduke_rss_url = "https://lunduke.substack.com/feed"
lunduke_all_feed_list = []

# main function function (ik that's a mouth-full) (im not explaining all this)

async def main_function(CHANNEL_ID):
    channel = client.get_channel(CHANNEL_ID)
    global arch_newest_actual, mint_newest_actual, planet_newest_actual
    global debian_newest_actual, slashdot_newest_actual, lunduke_newest_actual
    loop_allways_active =True
    while loop_allways_active:
        arch_feed = feedparser.parse(arch_rss_url)
        for entry in arch_feed.entries[:6]:
            arch_all_feed_list.append(entry.link)
        arch_latest_potential = arch_all_feed_list[0]

        #make the embed

        if arch_latest_potential != arch_newest_actual:
            title = "Latest Package Updates: Arch-Linux"
            line1 = "Newest"
            line3 = "Past"
            embed_description = "\n".join([line1, arch_all_feed_list[0], line3, arch_all_feed_list[1], arch_all_feed_list[2], arch_all_feed_list[3], arch_all_feed_list[4], arch_all_feed_list[5]])
            embed = discord.Embed(
                title=title,
                color=discord.Color.blue(),
                description=embed_description
            )

            # send the embed
            await channel.send(embed=embed)

            # prints data in terminal ( to disable hash till the next comment)
            print("Latest Package Updates: Arch-Linux")
            print("Newest")
            print(arch_all_feed_list[0])
            print("Past")
            print(arch_all_feed_list[1])
            print(arch_all_feed_list[2])
            print(arch_all_feed_list[3])
            print(arch_all_feed_list[4])
            print(arch_all_feed_list[5])
            arch_newest_actual = arch_all_feed_list[0]
            # the next comment
        else:
            print("nothing to add")
        response = requests.get(mint_rss_url, headers=headers)
        mint_feed = feedparser.parse(response.content)
        for entry in mint_feed.entries[:6]:
            mint_all_feed_list.append(entry.link)
        mint_latest_potential = mint_all_feed_list[0]
        if mint_latest_potential != mint_newest_actual:
            # make the embed

            title = "Latest Package Updates: Linux-Mint"
            line1 = "Newest"
            line3 = "Past"
            embed_description = "\n".join(
                [line1, mint_all_feed_list[0], line3, mint_all_feed_list[1], mint_all_feed_list[2],
                 mint_all_feed_list[3], mint_all_feed_list[4], mint_all_feed_list[5]])
            embed = discord.Embed(
                title=title,
                color=discord.Color.green(),
                description=embed_description
            )
            # send the embed
            await channel.send(embed=embed)

            # prints data in terminal ( to disable hash till the next comment)
            print("Latest Package Updates: Linux-Mint")
            print("Newest")
            print(mint_all_feed_list[0])
            print("Past")
            print(mint_all_feed_list[1])
            print(mint_all_feed_list[2])
            print(mint_all_feed_list[3])
            print(mint_all_feed_list[4])
            print(mint_all_feed_list[5])
            mint_newest_actual = mint_all_feed_list[0]
            # the next comment
        else:
            print("nothing to add")
        planet_feed = feedparser.parse(planet_rss_url)
        for entry in planet_feed.entries[:6]:
            planet_all_feed_list.append(entry.link)
        planet_latest_potential = planet_all_feed_list[0]
        if planet_latest_potential != planet_newest_actual:
            # make the embed
            title = "Latest Package Updates: planet-Linux"
            line1 = "Newest"
            line3 = "Past"
            embed_description = "\n".join(
                [line1, planet_all_feed_list[0], line3, planet_all_feed_list[1], planet_all_feed_list[2],
                 planet_all_feed_list[3], planet_all_feed_list[4], planet_all_feed_list[5]])
            embed = discord.Embed(
                title=title,
                color=discord.Color.purple(),
                description=embed_description
            )
            # send the embed
            await channel.send(embed=embed)

            # prints data in terminal ( to disable hash till the next comment)
            print("Latest Package Updates: Planet-Linux")
            print("Newest")
            print(planet_all_feed_list[0])
            print("Past")
            print(planet_all_feed_list[1])
            print(planet_all_feed_list[2])
            print(planet_all_feed_list[3])
            print(planet_all_feed_list[4])
            print(planet_all_feed_list[5])
            planet_newest_actual = planet_all_feed_list[0]
            # the next comment
        else:
            print("nothing to add")
        response = requests.get(debian_rss_url, headers=headers)
        debian_feed = feedparser.parse(response.content)
        for entry in debian_feed.entries[:6]:
            debian_all_feed_list.append(entry.link)
        debian_latest_potential = debian_all_feed_list[0]
        if debian_latest_potential != debian_newest_actual:
            # make the embed
            title = "Latest Package Updates: Debian"
            line1 = "Newest"
            line3 = "Past"
            embed_description = "\n".join(
                [line1, debian_all_feed_list[0], line3, debian_all_feed_list[1], debian_all_feed_list[2],
                 debian_all_feed_list[3], debian_all_feed_list[4], debian_all_feed_list[5]])
            embed = discord.Embed(
                title=title,
                color=discord.Color.red(),
                description=embed_description
            )
            # send the embed
            await channel.send(embed=embed)

            # prints data in terminal ( to disable hash till the next comment)
            print("Latest Package Updates: Debian")
            print("Newest")
            print(debian_all_feed_list[0])
            print("Past")
            print(debian_all_feed_list[1])
            print(debian_all_feed_list[2])
            print(debian_all_feed_list[3])
            print(debian_all_feed_list[4])
            print(debian_all_feed_list[5])
            debian_newest_actual = debian_all_feed_list[0]
            # the next comment
        else:
            print("nothing to add")
        slashdot_feed = feedparser.parse(slashdot_rss_url)
        for entry in slashdot_feed.entries[:6]:
            slashdot_all_feed_list.append(entry.link)
        slashdot_latest_potential = slashdot_all_feed_list[0]
        if slashdot_latest_potential != slashdot_newest_actual:
            # make the embed
            title = "Latest Package Updates: slashdot"
            line1 = "Newest"
            line3 = "Past"
            embed_description = "\n".join(
                [line1, slashdot_all_feed_list[0], line3, slashdot_all_feed_list[1], slashdot_all_feed_list[2],
                 slashdot_all_feed_list[3], slashdot_all_feed_list[4], slashdot_all_feed_list[5]])
            embed = discord.Embed(
                title=title,
                color=discord.Color.orange(),
                description=embed_description
            )
            # send the embed
            await channel.send(embed=embed)

            # prints data in terminal ( to disable hash till the next comment)
            print("Latest Package Updates: slashdot")
            print("Newest")
            print(slashdot_all_feed_list[0])
            print("Past")
            print(slashdot_all_feed_list[1])
            print(slashdot_all_feed_list[2])
            print(slashdot_all_feed_list[3])
            print(slashdot_all_feed_list[4])
            print(slashdot_all_feed_list[5])
            slashdot_newest_actual = slashdot_all_feed_list[0]
            # the next comment
        else:
            print("nothing to add")
        lunduke_feed = feedparser.parse(lunduke_rss_url)
        for entry in lunduke_feed.entries[:6]:
            lunduke_all_feed_list.append(entry.link)
        lunduke_latest_potential = lunduke_all_feed_list[0]
        if lunduke_latest_potential != lunduke_newest_actual:
            # make the embed
            title = "Latest Package Updates: lunduke"
            line1 = "Newest"
            line3 = "Past"
            embed_description = "\n".join(
                [line1, lunduke_all_feed_list[0], line3, lunduke_all_feed_list[1], lunduke_all_feed_list[2],
                 lunduke_all_feed_list[3], lunduke_all_feed_list[4], lunduke_all_feed_list[5]])
            embed = discord.Embed(
                title=title,
                color=discord.Color.dark_gray(),
                description=embed_description
            )
            # send the embed
            await channel.send(embed=embed)

            # prints data in terminal ( to disable hash till the next comment)
            print("Latest Package Updates: lunduke")
            print("Newest")
            print(lunduke_all_feed_list[0])
            print("Past")
            print(lunduke_all_feed_list[1])
            print(lunduke_all_feed_list[2])
            print(lunduke_all_feed_list[3])
            print(lunduke_all_feed_list[4])
            print(lunduke_all_feed_list[5])
            lunduke_newest_actual = lunduke_all_feed_list[0]
            # the next comment
        else:
            print("nothing to add")
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