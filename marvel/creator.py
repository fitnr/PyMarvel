# -*- coding: utf-8 -*-

__author__ = 'Garrett Pennington'
__date__ = '02/07/14'

from .structures import DataWrapper, DataItem


class CreatorDataWrapper(DataWrapper):

    def __init__(self, marvel, response, **params):
        super(CreatorDataWrapper, self).__init__(marvel, response, **params)

        self.item_class = Creator
        self.getter = self.marvel.get_creators


class Creator(DataItem):

    """
    Creator object
    Takes a dict of creator attrs
    """
    _resource_url = 'creators'

    @property
    def firstName(self):
        return self.dict['firstName']

    @property
    def middleName(self):
        return self.dict['middleName']

    @property
    def lastName(self):
        return self.dict['lastName']

    @property
    def suffix(self):
        return self.dict['suffix']

    @property
    def fullName(self):
        return self.dict['fullName']

    @property
    def urls(self):
        return self.dict['urls']

    """
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
    """

    @property
    def thumbnail(self):
        return "%s.%s" % (self.dict['thumbnail']['path'], self.dict['thumbnail']['extension'])

    @property
    def description(self):
        raise AttributeError("'Creator' has no attribute description")

    @property
    def creators(self):
        raise AttributeError("'Creator' has no attribute creators")

    def get_creators(self):
        raise AttributeError("'Creator' has no attribute get_creators")
