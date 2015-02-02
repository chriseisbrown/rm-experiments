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
        self.doc_version = ""
        self.abstract_text = ""
        self.journal = ""
        self.publish_date = None

    def display(self):
        print 'Article:', self._id, ' ', self.id_type, ' ', self.title.encode('utf-8'), ' ', self.abstract_text.encode('utf-8')
        print 'Published:', self.publish_date, ' ', self.version, ' ', self.doc_version, ' ', self.journal.encode('utf-8')

