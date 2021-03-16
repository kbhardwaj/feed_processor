from main import FeedsService

feedsService = FeedsService()
feedsService.run()

sources = feedsService.getFeedSources()

source = {
    'name': "theultralinx.",
    'url': "http://theultralinx.com/feed",
    'topics': [
        "Design"
    ]
}

sourceData = feedsService._retrieveFromSource(source)


items = []
r = requests.get(source.get('url'))
root = ET.fromstring(r.content)


# this script was iterated on a few times to get the final data structure.
# Earlier versions included empty items.
# I even got it wrong by creating an item for each tag instead of an item for each set of tags that constitute an item
for child in root.iter('*'):
    children = child.getchildren()
    item = {}
    for c in children:
        if c.tag in ['title', 'description', 'category']:
            item[c.tag] = c.text
    if item.get('title') and item.get('description'):
        items.append(item)


# Exception message for some source URLs when attempting to retrieve and parse XML feeds
# exception: source - https://www.youtube.com/channel/UCOKHwx1VCdgnxwbjyb9Iu1g not well-formed (invalid token): line 1, column 235
# exception: source - http://blendersushi.blogspot.com/feed not well-formed (invalid token): line 26, column 4
# exception: source - https://www.davidrevoy.com/feed syntax error: line 1, column 49
# exception: source - https://www.youtube.com/channel/UCVA3cYOgsTN4hs3v7pjne7w not well-formed (invalid token): line 1, column 235
# exception: source - https://www.iamag.co undefined entity: line 50, column 0
# exception: source - http://artofsoulburn.blogspot.com/feed not well-formed (invalid token): line 22, column 2
# exception: source - https://realtimevfx.com/latest mismatched tag: line 36, column 4
# exception: source - https://www.ronenbekerman.com/feed mismatched tag: line 6, column 2
# exception: source - https://blog.michelanders.nl/feed not well-formed (invalid token): line 23, column 4
# exception: source - https://www.thepixellab.net/feed mismatched tag: line 6, column 2
# exception: source - https://www.tomlooman.com/feed junk after document element: line 1, column 43
# exception: source - https://evermotion.org/feed not well-formed (invalid token): line 29, column 93
# exception: source - https://www.reddit.com/r/unrealengine/.rss syntax error: line 2, column 0
# exception: source - https://unrealpossibilities.blogspot.com/feed not well-formed (invalid token): line 18, column 41
# exception: source - https://www.reddit.com/r/learnprogramming/.rss syntax error: line 2, column 0
# exception: source - http://android-developers.googleblog.com/feed not well-formed (invalid token): line 8, column 42
# exception: source - https://codeascraft.com/feed mismatched tag: line 6, column 2
# exception: source - https://www.codeproject.com/feed no element found: line 1, column 0
# exception: source - https://danluu.com/atom/index.xml no element found: line 1, column 0
# exception: source - https://davidwalsh.name not well-formed (invalid token): line 2, column 11
# exception: source - https://dev.to mismatched tag: line 64, column 4
# exception: source - https://dropboxtechblog.wordpress.com/feed not well-formed (invalid token): line 8, column 87
# exception: source - https://www.freecodecamp.org/news not well-formed (invalid token): line 103, column 65
# exception: source - http://lambda-the-ultimate.org/feed mismatched tag: line 8, column 211
# exception: source - https://martinfowler.com/feed mismatched tag: line 234, column 2
# exception: source - https://netflixtechblog.com?source=rss----2615bd06b42e---4 not well-formed (invalid token): line 1, column 3518
# exception: source - http://planetpython.org/feed mismatched tag: line 6, column 2
# exception: source - http://scotch.io/feed not well-formed (invalid token): line 108, column 240
# exception: source - https://www.hanselman.com/blog/feed not well-formed (invalid token): line 66, column 18
# exception: source - http://blog.golang.org/feed syntax error: line 1, column 0

# Exceptions After fixes
# exception: source - https://www.ronenbekerman.com/feed/ mismatched tag: line 6, column 2
# exception: source - https://www.thepixellab.net/feed mismatched tag: line 6, column 2
# exception: source - https://www.tomlooman.com/feed/ junk after document element: line 1, column 43
# exception: source - https://www.reddit.com/r/unrealengine/.rss syntax error: line 2, column 0
# exception: source - https://www.reddit.com/r/learnprogramming/.rss syntax error: line 2, column 0
# exception: source - http://android-developers.googleblog.com/feed not well-formed (invalid token): line 8, column 42
# exception: source - https://codeascraft.com/feed/ mismatched tag: line 6, column 2