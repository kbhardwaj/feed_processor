from gensim.summarization import keywords

class TextRanker():

    def __init__(self, text):
        self.text = text

    def getKeywords(self):
        return (keywords(self.text).split('\n'))