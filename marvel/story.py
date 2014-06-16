# -*- coding: utf-8 -*-

__author__ = 'Garrett Pennington'
__date__ = '02/07/14'

from .core import MarvelObject, DataWrapper, DataContainer, Summary, List, Image

class StoryDataWrapper(DataWrapper):
    @property
    def data(self):
        return StoryDataContainer(self.marvel, self.dict['data'])

    def next(self):
        return self._next(self.marvel.get_stories)

    def previous(self):
        return self._previous(self.marvel.get_stories)


class StoryDataContainer(DataContainer):
    @property
    def results(self):
        return self.list_to_instance_list(self.dict['results'], Story)

class Story(MarvelObject):
    """
    Story object
    Takes a dict of character attrs
    """
    _resource_url = 'stories'

    @property
    def id(self):
        return self.dict['id']

    @property
    def title(self):
        return self.dict['title']

    @property
    def description(self):
        """
        :returns:  str -- A description of the series.
        """
        return self.dict['description']

    @property
    def resourceURI(self):
        return self.dict['resourceURI']

    @property
    def type(self):
        return self.dict['type']

    @property
    def modified(self):
        return self.str_to_datetime(self.dict['modified'])

    @property
    def modified_raw(self):
        return self.dict['modified']

    @property
    def thumbnail(self):
        return Image(self.marvel, self.dict['thumbnail'])

    @property
    def comics(self):
        from .comic import ComicList
        return ComicList(self.marvel, self.dict['comics'])

    @property
    def series(self):
        from .series import SeriesList
        return SeriesList(self.marvel, self.dict['series'])

    @property
    def events(self):
        from .event import EventList
        return EventList(self.marvel, self.dict['events'])

    @property
    def characters(self):
        from .character import CharacterList
        return CharacterList(self.marvel, self.dict['characters'])

    @property
    def creators(self):
        from .creator import CreatorList
        return CreatorList(self.marvel, self.dict['creators'])

    @property
    def originalIssue(self):
        from .comic import ComicSummary
        return ComicSummary(self.marvel, self.dict['originalIssue'])

    def get_stories(self):
        raise AttributeError("'Story' has no attribute get_stories")


class StoryList(List):
    """
    StoryList object
    """

    @property
    def items(self):
        """
        Returns List of StorySummary objects
        """
        return self.list_to_instance_list(self.dict['items'], StorySummary)

class StorySummary(Summary):
    """
    StorySummary object
    """

    @property
    def type(self):
        return self.dict['type']
