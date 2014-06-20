# -*- coding: utf-8 -*-

from .core import MarvelObject
from .summaries import CharacterSummary, ComicSummary, CreatorSummary, EventSummary, SeriesSummary, StorySummary


class DataWrapper(MarvelObject):

    """
    Base DataWrapper
    """

    @property
    def data(self):
        return DataContainer(self.marvel, self.dict['data'], self.item_class)

    def next(self, **kwargs):
        """
        Returns new DataWrapper
        Returns None if max has been reached

        :param method: A method in the Marvel class to run (e.g. get_comics)
        :type function
        """

        # Don't run on a non-successful request
        if self.code != 200:
            return

        # Don't run if count is 0
        if self.data.count == 0:
            return

        # Don't run if number requested is less than limit requested (at the
        # end)
        if self.data.count < self.data.limit:
            return

        params = dict((k, v) for k, v in self.params.items())
        params['offset'] = self.data.offset + self.data.count
        params.update(kwargs)  # passed arguments override params

        # don't send request if we're past the top
        if params['offset'] > self.data.total:
            return

        return self.getter(**params)

    def previous(self, **kwargs):
        """
        Returns new DataWrapper
        returns None if offset is already 0

        :param method: A method in the Marvel class to run (e.g. get_comics)
        :type function
        """
        # Don't run on a non-successful request
        if self.code != 200:
            return

        params = dict((k, v) for k, v in self.params.items())
        params['offset'] = max(self.data.offset - self.data.count, 0)
        params.update(kwargs)  # passed arguments override params

        # don't send request if we're at the bottom
        if self.data.offset <= 0:
            return

        return self.getter(**params)

    @property
    def code(self):
        """
        The HTTP status code of the returned result.

        :returns: int
        """
        return int(self.dict.get('code'))

    @property
    def status(self):
        """
        A string description of the call status.

        :returns: str
        """
        return self.dict.get('status')

    @property
    def etag(self):
        """
        A digest value of the content returned by the call.

        :returns: str
        """
        return self.dict.get('etag')


class DataContainer(MarvelObject):

    """
    Base DataContainer
    """

    def __init__(self, marvel, response, item_class):
        """
        :param marvel: Instance of Marvel class
        :type marvel: marvel.Marvel
        :param dict: Dict of object, created from json response.
        :type dict: dict
        :param item_class: Instance of a structure
        :type marvel: marvel.MarvelObject
        """
        super(DataContainer, self).__init__(marvel, response)
        self.item_class = item_class

    @property
    def results(self):
        return self.list_to_instance_list(self.dict.get('results'), self.item_class)

    @property
    def offset(self):
        """
        The requested offset (number of skipped results) of the call.

        :returns: int
        """
        return int(self.dict.get('offset'))

    @property
    def limit(self):
        """
        The requested result limit.

        :returns: int
        """
        return int(self.dict.get('limit'))

    @property
    def total(self):
        """
        The total number of resources available given the current filter set.

        :returns: int
        """
        return int(self.dict.get('total'))

    @property
    def count(self):
        """
        The total number of results returned by this call.

        :returns: int
        """
        return int(self.dict.get('count'))

    @property
    def result(self):
        """
        Returns the first item in the results list.
        Useful for methods that should return only one results.

        :returns: marvel.MarvelObject
        """
        return self.results[0]


class DataItem(MarvelObject):

    @property
    def id(self):
        return int(self.dict.get('id'))

    @property
    def modified(self):
        return self.str_to_datetime(self.dict.get('modified'))

    @property
    def description(self):
        return self.dict.get('description', None)

    @property
    def modified_raw(self):
        return self.dict.get('modified')

    @property
    def resourceURI(self):
        return self.dict.get('resourceURI')

    @property
    def characters(self):
        return ListWrapper(self.marvel, self.dict.get('characters'), CharacterSummary)

    @property
    def comics(self):
        return ListWrapper(self.marvel, self.dict.get('comics'), ComicSummary)

    @property
    def events(self):
        return ListWrapper(self.marvel, self.dict.get('events'), EventSummary)

    @property
    def creators(self):
        return ListWrapper(self.marvel, self.dict.get('creators'), CreatorSummary)

    @property
    def series(self):
        return ListWrapper(self.marvel, self.dict.get('series'), SeriesSummary)

    @property
    def stories(self):
        return ListWrapper(self.marvel, self.dict.get('stories'), StorySummary)

    def get_creators(self, **kwargs):
        """
        Returns a full CharacterDataWrapper object this character.
        :returns:  CharacterDataWrapper -- A new request to API. Contains full results set.
        """
        return self.get_related_resource(self.marvel.get_creators, **kwargs)

    def get_characters(self, **kwargs):
        """
        Returns a full CharacterDataWrapper object this character.
        :returns:  CharacterDataWrapper -- A new request to API. Contains full results set.
        """
        return self.get_related_resource(self.marvel.get_characters, **kwargs)

    def get_comics(self, **kwargs):
        """
        Returns a full ComicDataWrapper object this character.
        :returns:  ComicDataWrapper -- A new request to API. Contains full results set.
        """
        return self.get_related_resource(self.marvel.get_comics, **kwargs)

    def get_events(self, **kwargs):
        """
        Returns a full EventDataWrapper object this character.
        :returns:  EventDataWrapper -- A new request to API. Contains full results set.
        """
        return self.get_related_resource(self.marvel.get_events, **kwargs)

    def get_series(self, **kwargs):
        """
        Returns a full SeriesDataWrapper object this character.
        :returns:  SeriesDataWrapper -- A new request to API. Contains full results set.
        """
        return self.get_related_resource(self.marvel.get_series, **kwargs)

    def get_stories(self, **kwargs):
        """
        Returns a full StoryDataWrapper object this character.
        :returns:  StoriesDataWrapper -- A new request to API. Contains full results set.
        """
        return self.get_related_resource(self.marvel.get_stories, **kwargs)


class ListWrapper(MarvelObject):

    """
    Base List object
    """

    def __init__(self, marvel, items, _class):
        """
        :param marvel: Instance of Marvel class
        :type marvel: marvel.Marvel
        :param dict: list of objects
        :type items: dict
        :param _class: Type of the elements
        :type params: class

        """
        self.marvel = marvel
        self.dict = items or dict()
        self._class = _class

    @property
    def available(self):
        """
        The number of total available resources in this list. Will always be greater than or equal to the "returned" value.

        :returns: int
        """
        return int(self.dict.get('available'))

    @property
    def items(self):
        """
        Returns List of StorySummary objects
        """
        return self.list_to_instance_list(self.dict.get('items'), self._class)

    @property
    def returned(self):
        """
        The number of resources returned in this collection (up to 20).

        :returns: int
        """
        return int(self.dict.get('returned'))

    @property
    def collectionURI(self):
        """
        The path to the full list of resources in this collection.

        :returns: str
        """
        return self.dict.get('collectionURI')


class TextObject(MarvelObject):

    @property
    def type(self):
        """
        The canonical type of the text object (e.g. solicit text, preview text, etc.).

        :returns: str
        """
        return self.dict.get('type')

    @property
    def language(self):
        """
        The IETF language tag denoting the language the text object is written in.

        :returns: str
        """
        return self.dict.get('language')

    @property
    def text(self):
        """
        The text.

        :returns: str
        """
        return self.dict.get('text')


class Image(MarvelObject):

    @property
    def path(self):
        """
        The directory path of to the image.

        :returns: str
        """
        return self.dict.get('path')

    @property
    def extension(self):
        """
        The file extension for the image.

        :returns: str
        """
        return self.dict.get('extension')

    def __repr__(self):
        return "%s.%s" % (self.path, self.extension)
