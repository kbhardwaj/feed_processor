import os
import webbrowser
from jinja2 import Environment, PackageLoader, select_autoescape
from services.store import storeIOService

env = Environment(
    loader=PackageLoader('services.view', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


"""
Get data from the store and create the jinja html templates to view the data in human readable form
"""
class WebViewer():

    def __init__(self):
        pass

    def _getPath(self):
        return os.path.abspath('services/view/tutorials/views/tutorials.html')

    def browserOpen(self):
        url = 'file://' + self._getPath()
        webbrowser.open(url)

    def view(self, templateName=None):
        templateName = templateName or 'tutorials'
        html = templateRenderer.render(templateName)

        with open(self._getPath(), 'w+') as f:
            f.write(html)
        
        self.browserOpen()

class TemplateRenderer():

    def __init__(self):
        self.store = storeIOService

    def getTemplateData(self, templateName):
        return self.store.get(templateName)

    def render(self, templateName='tutorials'):
        template = env.get_template('tutorials.html')
        # get the data from store. use data to render template
        templateData = self.getTemplateData(templateName)

        items = [v for k, v in templateData.items()]

        return template.render(items=items)

templateRenderer = TemplateRenderer()