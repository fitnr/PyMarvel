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
    def name(self):
        """
        The canonical name of the resource.

        :returns: str
        """
        return self.dict['name']


class CharacterSummary(Summary):

    """
    CharacterSummary object
    """

    @property
    def role(self):
        return self.dict['role']


class ComicSummary(Summary):

    """
    CommicSummary object
    """


class CreatorSummary(Summary):

    """
    CreatorSummary object
    """

    @property
    def role(self):
        return self.dict['role']


class EventSummary(Summary):

    """
    EventSummary object
    """


class SeriesSummary(Summary):

    """
    SeriesSummary object
    """


class StorySummary(Summary):

    """
    StorySummary object
    """

    @property
    def type(self):
        return self.dict['type']
