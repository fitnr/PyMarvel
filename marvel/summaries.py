from os import path
from .core import MarvelObject


class Summary(MarvelObject):

    """
    Base Summary object
    """

    @property
    def resourceURI(self):
        """
        The path to the individual resource.

        :returns: str
        """
        return self.dict['resourceURI']

    @property
    def id(self):
        return path.basename(self.resourceURI)

    @property
    def name(self):
        """
        The canonical name of the resource.

        :returns: str
        """
        return self.dict['name']

    def get(self, **kwargs):
        kwargs['id'] = self.id
        return self.get_related_resource(self.getter, **kwargs)


class CharacterSummary(Summary):

    """
    CharacterSummary object
    """
    _resource_url = 'characters'

    @property
    def getter(self):
        return self.marvel.get_character

    @property
    def role(self):
        return self.dict['role']


class ComicSummary(Summary):

    """
    CommicSummary object
    """
    _resource_url = 'comics'

    @property
    def getter(self):
        return self.marvel.get_comic


class CreatorSummary(Summary):

    """
    CreatorSummary object
    """

    _resource_url = 'creators'

    @property
    def getter(self):
        return self.marvel.get_creator

    @property
    def role(self):
        return self.dict['role']


class EventSummary(Summary):

    """
    EventSummary object
    """
    _resource_url = 'events'

    @property
    def getter(self):
        return self.marvel.get_event


class SeriesSummary(Summary):

    """
    SeriesSummary object
    """
    _resource_url = 'series'

    @property
    def getter(self):
        return self.marvel.get_single_series


class StorySummary(Summary):

    """
    StorySummary object
    """
    _resource_url = 'stories'

    @property
    def getter(self):
        return self.marvel.get_story

    @property
    def type(self):
        return self.dict['type']
