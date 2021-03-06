# -*- coding: utf-8 -*-

__author__ = 'Garrett Pennington'
__date__ = '02/07/14'

from .structures import DataWrapper, DataItem, Image
from .summaries import ComicSummary


class StoryDataWrapper(DataWrapper):

    def __init__(self, marvel, response, **params):
        super(StoryDataWrapper, self).__init__(marvel, response, **params)

        self.item_class = Story
        self.getter = self.marvel.get_stories


class Story(DataItem):

    """
    Story object
    Takes a dict of character attrs
    """
    _resource_url = 'stories'

    @property
    def title(self):
        return self.dict['title']

    @property
    def type(self):
        return self.dict['type']

    @property
    def thumbnail(self):
        return Image(self.marvel, self.dict['thumbnail'])

    @property
    def originalIssue(self):
        return ComicSummary(self.marvel, self.dict['originalIssue'])

    @property
    def stories(self):
        raise AttributeError("'Story' has no attribute stories")

    def get_stories(self):
        raise AttributeError("'Story' has no attribute get_stories")
