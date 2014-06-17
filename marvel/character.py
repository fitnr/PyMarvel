# -*- coding: utf-8 -*-

__author__ = 'Garrett Pennington'
__date__ = '02/07/14'

from .structures import DataItem, DataWrapper, DataContainer


class CharacterDataWrapper(DataWrapper):

    @property
    def data(self):
        return DataContainer(self.marvel, self.dict['data'], Character)

    def next(self):
        return self._next(self.marvel.get_characters)

    def previous(self):
        return self._previous(self.marvel.get_characters)


class Character(DataItem):

    """
    Character object
    Takes a dict of character attrs
    """
    _resource_url = 'characters'

    @property
    def name(self):
        return self.dict['name']

    @property
    def resourceURI(self):
        return self.dict['resourceURI']

    @property
    def urls(self):
        return self.dict['urls']

    @property
    def wiki(self):
        for item in self.dict['urls']:
            if item['type'] == 'wiki':
                return item['url']
        return None

    @property
    def detail(self):
        for item in self.dict['urls']:
            if item['type'] == 'detail':
                return item['url']
        return None

    @property
    def thumbnail(self):
        return "%s.%s" % (self.dict['thumbnail']['path'], self.dict['thumbnail']['extension'])

    @property
    def characters(self):
        raise AttributeError("'Character' has no attribute characters")

    def get_characters(self, **kwargs):
        raise AttributeError("'Character' has no attribute get_characters")


