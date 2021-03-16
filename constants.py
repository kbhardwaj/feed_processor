class Usecases:
    TUTORIAL_REPOSITORY = 'tutorialRepository'
    EVENTS_REPOSITORY = 'eventsRepository'
    SOCIAL_REPOSITORY = 'social'

USECASE_CONFIG = {
    Usecases.TUTORIAL_REPOSITORY: {
        # topics were manually added to feed sources in the rss endpoint.
        'topic': ['Programming', 'GameDev'],

        # filters are keyword tags.
        # at least one of the filters needs to be present in order for the source to be included
        'filters': ['tutorial', 'tutorials', 'guide', 'how', 'technique', 'techniques', 'project'],
        
        # search for categories in the text of the feeds. Attach catgories to the results
        'categories': [
            'javascript', 'python', 'data science', 'golang', 'chat', 'chatbot', 'realtime', 'webdev', 
            'web development', 'c++', 'java', 'machine learning', 'nlp', 'frontend', 'react',
            'vue', 'next.js', 'html', 'css', 'git', 'bitcoin', 'crypto', 'cryptocurrency', 'ethereum', 'eth',
        ],
    },
    Usecases.EVENTS_REPOSITORY: {

    },
    Usecases.SOCIAL_REPOSITORY: {

    },
}