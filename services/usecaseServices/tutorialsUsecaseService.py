import re
import string

from constants import Usecases
from constants import USECASE_CONFIG
from services.NLP import Raker
from services.NLP import TextRanker
from services.store import storeIOService

escapes = ''.join([chr(char) for char in range(1, 32)])
translator = str.maketrans('', '', escapes)
cleanr = re.compile('<.*?>')
printable = set(string.printable)

class TextFetcher():

    def __init__(self, item):
        self.item = item
        self.cleanDescription = None
        self.cleanTitle = None

    def _isClean(self):
        return self.cleanDescription and self.cleanTitle

    def _getDescription(self):
        return self.item.get('description', '') 
    
    def _getTitle(self):
        return self.item.get('title', '')

    # https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
    def cleanhtml(self, text):
        return re.sub(cleanr, '', text)

    # https://stackoverflow.com/questions/8689795/how-can-i-remove-non-ascii-characters-but-leave-periods-and-spaces-using-python
    def removeNonPrintable(self, s):
        return ''.join(map(lambda x: x if x in printable else ' ', s))

    def getCleanDescription(self):
        description = self.cleanhtml(self._getDescription())
        cleanDescription = self.removeNonPrintable(description.translate(translator))
        self.cleanDescription = cleanDescription
        return cleanDescription

    def getCleanTitle(self):
        title = self.cleanhtml(self._getTitle())
        cleanTitle = self.removeNonPrintable(title.translate(translator))
        self.cleanTitle = cleanTitle
        return cleanTitle
        
    def getText(self):
        title, description = self.getCleanedFields()
        category = self.item.get('category', '')
        
        self.cleanTitle = title
        self.cleanDescription = description

        return title + ' ' + description + ' ' + ' ' + category

    def getCleanedFields(self):
        return (self.getCleanTitle() or '', self.getCleanDescription() or '')

    def getCleanedItem(self):
        if self._isClean:
            title = self.cleanTitle
            description = self.cleanDescription
        else:
            title, description = self.getCleanedFields()
            self.cleanTitle = title
            self.cleanDescription = description

        self.item["title"] = title
        self.item["description"] = description
        return self.item

        

class TutorialsUsecaseService():
    
    def __init__(self):
        self.identifier = Usecases.TUTORIAL_REPOSITORY
        self.processedItems = []
        self.notProcessedItems = []
        self.filters = USECASE_CONFIG.get(self.identifier).get('filters')
        self.categories = USECASE_CONFIG.get(self.identifier).get('categories')

    def passesFilter(self, itemKeywords):
        return any(keyword for keyword in itemKeywords if keyword in self.filters)

    def addCategories(self, itemKeywords, item):
        categories = list(filter(lambda x: x in self.categories, itemKeywords))
        categoryList = categories or []
        if item.get('category'):
            categoryList = categoryList + item.get('category').split(',')

        item["categories"] = list(set(categoryList))

    # temporary method
    def getRakeKeywords(self, item):
        text = TextFetcher(item).getText()

        print("Rake keywords:")
        print("text:", text)
        raker = Raker(text)
        itemKeywords = raker.getKeywords()
        print("keywords", itemKeywords)
        print(" ")
        print(" ")
        return itemKeywords

    # temporary method
    def getTextRankerKeywords(self, item):
        text = TextFetcher(item).getText()
        print("TextRanker keywords:")
        print("text:", text)
        textRanker = TextRanker(text)
        itemKeywords = textRanker.getKeywords()
        print("keywords", itemKeywords)
        print(" ")
        print(" ")
        return itemKeywords

    def processItem(self, item):
        """
        clean up formatting, include any extra fields, add to existing fields like "categories"
        fields: 'title', 'description', 'category', 'link', 'pubDate'
        """
        # itemCopyToProcess = item

        textFetcher = TextFetcher(item)
        text = textFetcher.getText()
        item = textFetcher.getCleanedItem()
        keywords = text.lower().split(' ')

        # filters: if keywords don't inlcude a filter, discard item
        if self.passesFilter(keywords):

            ## categories: categories included in keywords should be attached to item
            self.addCategories(keywords, item)

            self.processedItems.append(item)

            print('title', item.get('title'))
            print('keywords', keywords)
            print('categories:', item.get('categories'))
            print(' ')
            print(' ')
        else:
            self.notProcessedItems.append(item)

    def processItems(self, items):

        for item in items:
            # self.getRakeKeywords(item)
            # self.getTextRankerKeywords(item)
            self.processItem(item)
            
        # write processed to csv. this will override whatever is existing in the csv file
        # write notProcessed to separate csv.
        storeIOService.store('tutorials', {item.get('link'): item for item in self.processedItems if item.get('link')})
        
        storeIOService.store('not_tutorials', {item.get('link'): item for item in self.notProcessedItems if item.get('link')})

    def run(self, sourceData):
        """
        Filter the sourceData to find items that classify as tutorials.
        Categorize the tutorials by the tags listed in USECASE_CONFIG categories.
        Save the filtered and enriched items in self.processedItems
        """
        for url, items in sourceData.items():
            print('processing items from {}...'.format(url))
            self.processItems(items)

    def getProcessedItems(self):
        return self.processedItems

    def generateItemListInHTML(self):
        """
        Create an html list of the processedItems.
        HTML will include input elements for selecting items to save to usecase repositories.
        HTML will include input elements for correcting any potentially incorrect item categorizations
        """
        pass

tutorialsUsecaseService = TutorialsUsecaseService()