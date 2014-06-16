# -*- coding: utf-8 -*-

__author__ = 'Garrett Pennington'
__date__ = '02/07/14'

from datetime import datetime


class MarvelObject(object):

    """
    Base class for all Marvel API classes
    """

    def __init__(self, marvel, response, **params):
        """
        :param marvel: Instance of Marvel class
        :type marvel: marvel.Marvel
        :param dict: Dict of object, created from json response.
        :type response: dict
        :param params: Optional dict of query params sent to original API call
        :type params: dict

        """
        self.marvel = marvel
        self.dict = response or dict()
        self.params = params or dict()

    def __unicode__(self):
        """
        :returns:  str -- Name or Title of Resource
        """
        try:
            return self.dict['name']
        except:
            return self.dict['title']

    def to_dict(self):
        """
        :returns:  dict -- Dictionary representation of the Resource
        """
        return self.dict

    @classmethod
    def resource_url(cls):
        """
        :returns:  str -- Resource URL
        """
        return cls._resource_url

    def list_to_instance_list(self, _list, _Class):
        """
        Takes a list of resource dicts and returns a list
        of resource instances, defined by the _Class param.

        :param _self: Original resource calling the method
        :type _self: core.MarvelObject
        :param _list: List of dicts describing a Resource.
        :type _list: list
        :param _Class: The Resource class to create a list of (Comic, Creator, etc).
        :type _Class: core.MarvelObject

        :returns:  list -- List of Resource instances (Comic, Creator, etc).
        """
        items = []
        for item in _list:
            items.append(_Class(self.marvel, item))
        return items

    def get_related_resource(self, method, **kwargs):
        """
        Takes a related resource Class
        and returns the related resource DataWrapper.
        For Example: Given a Character instance, return
        a ComicsDataWrapper related to that character.
        /comics/?character=id

        :param method: The method of marvel class to run
        :type method:
        :param kwargs: dict of query params for the API
        :type kwargs: dict

        :returns:  DataWrapper -- DataWrapper for requested Resource
        """
        # Copy params
        # resource_url name matches the key for the id.
        params = dict((k, v) for k, v in self.params)
        params[self._resource_url] = self.id

        # kwargs override the internal values
        params.update(kwargs)
        return method(**params)

    def str_to_datetime(self, _str):
        """
        Converts '2013-11-20T17:40:18-0500' format to 'datetime' object

        :returns: datetime
        """
        # Hacked off %z timezone because reasons
        return datetime.strptime(_str[:-5], '%Y-%m-%dT%H:%M:%S')

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


class DataWrapper(MarvelObject):

    """
    Base DataWrapper
    """

    def _next(self, method):
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

        return method(**params)

    def _previous(self, method):
        """
        Returns new DataWrapper
        returns None if offset is already 0

        :param method: A method in the Marvel class to run (e.g. get_comics)
        :type function
        """
        # Don't run on a non-successful request
        if self.code != 200:
            return

        if self.data.offset == 0:
            return

        params = dict((k, v) for k, v in self.params.items())
        params['offset'] = max(self.data.offset - self.data.count, 0)

        return method(**params)

    @property
    def code(self):
        """
        The HTTP status code of the returned result.

        :returns: int
        """
        return int(self.dict['code'])

    @property
    def status(self):
        """
        A string description of the call status.

        :returns: str
        """
        return self.dict['status']

    @property
    def etag(self):
        """
        A digest value of the content returned by the call.

        :returns: str
        """
        return self.dict['etag']

    def get_creators(self):
        raise AttributeError('"{0}" has no attribute {1}'.format(
            self.__class__.__name__, 'get_creators'))

    def get_characters(self):
        raise AttributeError('"{0}" has no attribute {1}'.format(
            self.__class__.__name__, 'get_characters'))

    def get_comics(self):
        raise AttributeError(
            '"{0}" has no attribute {1}'.format(self.__class__.__name__, 'get_comics'))

    def get_events(self):
        raise AttributeError(
            '"{0}" has no attribute {1}'.format(self.__class__.__name__, 'get_events'))

    def get_series(self):
        raise AttributeError(
            '"{0}" has no attribute {1}'.format(self.__class__.__name__, 'get_series'))

    def get_stories(self):
        raise AttributeError(
            '"{0}" has no attribute {1}'.format(self.__class__.__name__, 'get_stories'))


class DataContainer(MarvelObject):

    """
    Base DataContainer
    """

    def __init__(self, marvel, response):
        """
        :param marvel: Instance of Marvel class
        :type marvel: marvel.Marvel
        :param dict: Dict of object, created from json response.
        :type dict: dict
        """
        self.marvel = marvel
        self.dict = response

    @property
    def offset(self):
        """
        The requested offset (number of skipped results) of the call.

        :returns: int
        """
        return int(self.dict['offset'])

    @property
    def limit(self):
        """
        The requested result limit.

        :returns: int
        """
        return int(self.dict['limit'])

    @property
    def total(self):
        """
        The total number of resources available given the current filter set.

        :returns: int
        """
        return int(self.dict['total'])

    @property
    def count(self):
        """
        The total number of results returned by this call.

        :returns: int
        """
        return int(self.dict['count'])

    @property
    def result(self):
        """
        Returns the first item in the results list.
        Useful for methods that should return only one results.

        :returns: marvel.MarvelObject
        """
        return self.results[0]


class List(MarvelObject):

    """
    Base List object
    """

    @property
    def available(self):
        """
        The number of total available resources in this list. Will always be greater than or equal to the "returned" value.

        :returns: int
        """
        return int(self.dict['available'])

    @property
    def returned(self):
        """
        The number of resources returned in this collection (up to 20).

        :returns: int
        """
        return int(self.dict['returned'])

    @property
    def collectionURI(self):
        """
        The path to the full list of resources in this collection.

        :returns: str
        """
        return self.dict['collectionURI']


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


class TextObject(MarvelObject):

    @property
    def type(self):
        """
        The canonical type of the text object (e.g. solicit text, preview text, etc.).

        :returns: str
        """
        return self.dict['type']

    @property
    def language(self):
        """
        The IETF language tag denoting the language the text object is written in.

        :returns: str
        """
        return self.dict['language']

    @property
    def text(self):
        """
        The text.

        :returns: str
        """
        return self.dict['text']


class Image(MarvelObject):

    @property
    def path(self):
        """
        The directory path of to the image.

        :returns: str
        """
        return self.dict['path']

    @property
    def extension(self):
        """
        The file extension for the image.

        :returns: str
        """
        return self.dict['extension']

    def __repr__(self):
        return "%s.%s" % (self.path, self.extension)
