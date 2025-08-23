# Cyrstal Orb
The Crystal Orb is a news service bot that posts articles from RSS feeds
to a news channel, allows users to subscribe to specific feeds, and uses
specific invite links to auto-role new members. 

## Options
The main.py has options variables at the top of the file that you can
modify to change the behavior of the bot, here they are with a little
explanation:
* titleOnly
    * Type: Boolean
    * Default state: false
    * Function: Changes the embed style to only show the title of the
    latest article. The title will be link-a-fied and clickable, and if
    the author and publish date are available they will be shown as well
* forceList
    * Type: Boolean
    * Default state: false
    * Function: Forces rss descriptions to be replaced by a list of
    previous articles regardless of whether they're usable.
* appendLIst
    * Type: Boolean
    * Default state: false
    * Function: Always appends the previous articles list to the rss
    description as a part of the embed. 
* refreshRate
    * Type: Integer
    * Default state: 1800
    * Function: The amount of time, measured in seconds, that the bot
    waits before checking the rss feeds for new articles.
* rssUrlList
    * Type: List
    * Default state: Empty
    * Contains each rss feed URL the bot will scrape

## To-do List
* Add feed-specific subscription feature.
    * Checks for roles dedicated to each rss feed.
    * Makes roles that are missing.
    * Subscribes / Unsubscribes users according to embed buttons.
* Add invite-link-specific auto-role feature.
    * Checks new users by which invite link they joined with.
    * Adds them to a different role according to each link.
    * Link to role relationship is determined by head of main.py
    configuration like with existing options.
* Fix feed dependent variables.
    * temp.entries on line 71
    * bizarre list of values on line 57

## Known Bugs
* All 'Subscribe' and 'Unsubscribe' buttons only modify the role of the
    most recent embeds feed.
