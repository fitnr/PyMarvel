# -*- coding: utf-8 -*-

__author__ = 'Garrett Pennington'
__date__ = '02/07/14'

from .core import MarvelObject, DataWrapper, DataContainer, Summary, List

class CreatorDataWrapper(DataWrapper):
    @property
    def data(self):
        return CreatorDataContainer(self.marvel, self.dict['data'])

    def next(self):
        return self._next(self.marvel.get_creators)

    def previous(self):
        return self._previous(self.marvel.get_creators)

class CreatorDataContainer(DataContainer):
    @property
    def results(self):
        return self.list_to_instance_list(self.dict['results'], Creator)


class Creator(MarvelObject):
    """
    Creator object
    Takes a dict of creator attrs
    """
    _resource_url = 'creators'

    @property
    def id(self):
        return int(self.dict['id'])

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
    def modified(self):
        return self.str_to_datetime(self.dict['modified'])

    @property
    def modified_raw(self):
        return self.dict['modified']

    @property
    def resourceURI(self):
        return self.dict['resourceURI']

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
        return "%s.%s" % (self.dict['thumbnail']['path'], self.dict['thumbnail']['extension'] )

    @property
    def series(self):
        """
        Returns SeriesList object
        """
        from .series import SeriesList
        return SeriesList(self.marvel, self.dict['series'])

    @property
    def stories(self):
        """
        Returns StoryList object
        """
        from .story import StoryList
        return StoryList(self.marvel, self.dict['stories'])

    @property
    def comics(self):
        from .comic import ComicList
        """
        Returns ComicList object
        """
        return ComicList(self.marvel, self.dict['comics'])

    @property
    def events(self):
        """
        Returns EventList object
        """
        from .event import EventList
        return EventList(self.marvel, self.dict['events'])
        
    def get_creators(self):
        raise AttributeError("'Creator' has no attribute get_creators")

class CreatorList(List):
    """
    CreatorList object
    """

    @property
    def items(self):
        """
        Returns List of CreatorSummary objects
        """
        return self.list_to_instance_list(self.dict['items'], CreatorSummary)

class CreatorSummary(Summary):
    """
    CreatorSummary object
    """
        
    @property
    def role(self):
        return self.dict['role']
