'''
Created on 26 Jan 2015

@author: chriseisbrown
'''
class Article(object):
    def __init__(self):
        self._id = ""
        self.URL = ""
        self.id_type = ""
        self.title = ""
        self.version = None
        self.abstract_text = ""
        self.journal = ""
        self.publish_date = None

    def display(self):
        print 'Activity:', self._id, ' ', self.id_type, ' ', self.title, ' ', self.version, ' ', self.abstract_text
        print 'Published:', self.publish_date, ' ', self.journal

