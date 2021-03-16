import requests
from constants import Usecases
from constants import USECASE_CONFIG
from services.usecaseServices import tutorialsUsecaseService
import xml.etree.ElementTree as ET

# Services
# - 

class FeedsService():

    def __init__(self):
        self.sourceData = {}
        self.usecases = [
            tutorialsUsecaseService,
        ]

    def getFeedSources(self):
        r = requests.get('https://learn.alphabits.io/api/feeds/rss')
        sources = r.json()
        return sources

    def _retrieveFromSource(self, source):
        items = []
        sourceUrl = source.get('url')
        if not sourceUrl:
            return
        # should this method handle the source data type? (xml, html, json)
        # Yes, but not yet. I don't need it yet because all the sources are xml.
        # If I add sources to /api/feeds/ that are not xml, then I'll need to handle those conditions here
        
        sourceTopics = ','.join(source.get('topics'))
        
        try:
            r = requests.get(sourceUrl)
            root = ET.fromstring(r.content)

            # To view all elements (tags) we can use a wildcard such as "*"
            for child in root.iter('*'):
                children = child.getchildren()
                item = {}
                for c in children:
                    if c.tag in ['title', 'description', 'category', 'link', 'pubDate']:
                        text = c.text
                        if c.tag == 'category':
                            text = text + ',' + sourceTopics

                        item[c.tag] = text
                if item.get('title') and item.get('description'):
                    items.append(item)

            self.sourceData[sourceUrl] = items
        except Exception as e:
            print('exception: source - {}'.format(sourceUrl), str(e))
            return

    def retrieveFromSources(self, sources):
        for source in sources:
            self._retrieveFromSource(source)

    def processSourceDataForUsecases(self):
        """
        filter raw sources by Usecase filters (check in constants.py).
        
        Process and Enrich
        Attach usecase categories to each item in sources.
        Attach date to each item in sources
        """
        for usecase in self.usecases:
            usecase.run(self.sourceData)

    def parseFeeds(self, feedSources):
        """
        input: USECASE_CONFIG
        output: usecases data, based on input config
        """
        # usecaseIdentifiers = list(self.usecases.keys())
        usecaseIdentifiers = [usecase.identifier for usecase in self.usecases]

        # search: "flatten list comprehension python"
        topicLists = [USECASE_CONFIG.get(usecaseIdentifier).get('topic') for usecaseIdentifier in usecaseIdentifiers]
        
        # list
        # allTopics = [topic for sublist in topicLists for topic in sublist]
        # dict
        allTopics = {topic: 1 for sublist in topicLists for topic in sublist}

        # sources are the feed sources that have been filtered by the topics and need to be requested
        sources = filter(lambda source: any([(topic in allTopics) for topic in source.get('topics', [])]), feedSources)

        # retrieve the raw sources just once
        # loop through sources and make requests to urls and save responses to self.sourceData
        self.retrieveFromSources(sources)

        # for each usecase in self.usecases, 
        # process the sourceData accordingly and save the results to the usecase service's "processedItems"
        self.processSourceDataForUsecases()

    # called periodically by crontab
    def run(self):
        """
        Add all new feed processing functions here.
        - getFeedSources
        """

        feedSources = self.getFeedSources()
        
        self.parseFeeds(feedSources)