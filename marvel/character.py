# -*- coding: utf-8 -*-

__author__ = 'Garrett Pennington'
__date__ = '02/07/14'

from .core import MarvelObject, DataWrapper, DataContainer, Summary, List


class CharacterDataWrapper(DataWrapper):

    @property
    def data(self):
        return CharacterDataContainer(self.marvel, self.dict['data'])

    def next(self):
        return self._next(self.marvel.get_characters)

    def previous(self):
        return self._previous(self.marvel.get_characters)


class CharacterDataContainer(DataContainer):

    @property
    def results(self):
        return self.list_to_instance_list(self.dict['results'], Character)


class Character(MarvelObject):

    """
    Character object
    Takes a dict of character attrs
    """
    _resource_url = 'characters'

    @property
    def id(self):
        return self.dict['id']

    @property
    def name(self):
        return self.dict['name']

    @property
    def description(self):
        return self.dict['description']

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
    def comics(self):
        from .comic import ComicList
        """
        Returns ComicList object
        """
        return ComicList(self.marvel, self.dict['comics'])

    @property
    def events(self):
        from .event import EventList
        """
        Returns EventList object
        """
        return EventList(self.marvel, self.dict['events'])

    @property
    def stories(self):
        from .story import StoryList
        """
        Returns StoryList object
        """
        return StoryList(self.marvel, self.dict['comics'])

    @property
    def series(self):
        from .series import SeriesList
        """
        Returns SeriesList object
        """
        return SeriesList(self.marvel, self.dict['series'])

    def get_characters(self, **kwargs):
        raise AttributeError("'Character' has no attribute get_characters")


class CharacterList(List):

    """
    CharacterList object
    """
    @property
    def items(self):
        """
        Returns List of CharacterSummary objects
        """
        return self.list_to_instance_list(self.dict['items'], CharacterSummary)


class CharacterSummary(Summary):

    """
    CharacterSummary object
    """

    @property
    def role(self):
        return self.dict['role']
