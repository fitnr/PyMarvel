# -*- coding: utf-8 -*-

__author__ = 'Garrett Pennington'
__date__ = '02/07/14'

import hashlib
import datetime

import requests

from .character import Character, CharacterDataWrapper
from .comic import ComicDataWrapper, Comic
from .creator import CreatorDataWrapper, Creator
from .event import EventDataWrapper, Event
from .series import SeriesDataWrapper, Series
from .story import StoryDataWrapper, Story

DEFAULT_API_VERSION = 'v1'


class Marvel(object):

    """Marvel API class

    This class provides methods to interface with the Marvel API

    >>> m = Marvel("acb123....", "efg456...")

    """

    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key

    def _endpoint(self):
        return "http://gateway.marvel.com/%s/public/" % (DEFAULT_API_VERSION)

    def _call(self, resource_url, **params):
        """
        Calls the Marvel API endpoint

        :param resource_url: url slug of the resource
        :type resource_url: str
        :param params: query params to add to endpoint
        :type params: str
        
        :returns:  response -- Requests response
        """
        url = "{0}{1}".format(self._endpoint(), resource_url)
        params.update(self._auth())
        return requests.get(url, params=params).json()

    def _auth(self):
        """
        Creates hash from api keys and returns all required parametsrs
        
        :returns:  str -- URL encoded query parameters containing "ts", "apikey", and "hash"
        """
        ts = datetime.datetime.now().strftime("%Y-%m-%d%H:%M:%S")
        hash_string = hashlib.md5(
            "%s%s%s" % (ts, self.private_key, self.public_key)).hexdigest()
        auth = {
            'ts': ts,
            'apikey': self.public_key,
            'hash': hash_string
        }
        return auth

    # public methods
    def get_character(self, id, **kwargs):
        """Fetches a single character by id.

        get /v1/public/characters

        :param id: ID of Character
        :type params: int
        
        :returns:  CharacterDataWrapper

        >>> m = Marvel(public_key, private_key)
        >>> cdw = m.get_character(1009718)
        >>> print cdw.data.count
        1
        >>> print cdw.data.results[0].name
        Wolverine

        """
        url = "%s/%s" % (Character.resource_url(), id)
        response = self._call(url)
        return CharacterDataWrapper(self, response, **kwargs)

    def get_characters(self, **kwargs):
        """Fetches lists of comic characters with optional filters.

        get /v1/public/characters/{characterId}

        :returns:  CharacterDataWrapper

        >>> m = Marvel(public_key, private_key)
        >>> cdw = m.get_characters(orderBy="name,-modified", limit="5", offset="15")
        >>> print cdw.data.count
        1401
        >>> for result in cdw.data.results:
        ...     print result.name
        Aginar
        Air-Walker (Gabriel Lan)
        Ajak
        Ajaxis
        Akemi
        
        """
        # pass url string and params string to _call
        response = self._call(Character.resource_url(), **kwargs)
        return CharacterDataWrapper(self, response, **kwargs)

    def get_comic(self, id, **kwargs):
        """Fetches a single comic by id.
        
        get /v1/public/comics/{comicId}
        
        :param id: ID of Comic
        :type params: int
        
        :returns:  ComicDataWrapper

        >>> m = Marvel(public_key, private_key)
        >>> cdw = m.get_comic(1009718)
        >>> print cdw.data.count
        1
        >>> print cdw.data.result.name
        Some Comic
        """

        url = "%s/%s" % (Comic.resource_url(), id)
        response = self._call(url)
        return ComicDataWrapper(self, response, **kwargs)

    def get_comics(self, **kwargs):
        """
        Fetches list of comics.

        get /v1/public/comics
                
        :returns:  ComicDataWrapper
        
        >>> m = Marvel(public_key, private_key)
        >>> cdw = m.get_comics(orderBy="issueNumber,-modified", limit="10", offset="15")
        >>> print cdw.data.count
        10
        >>> print cdw.data.results[0].name
        Some Comic

        """

        response = self._call(Comic.resource_url(), **kwargs)
        return ComicDataWrapper(self, response, **kwargs)

    def get_creator(self, id, **kwargs):
        """Fetches a single creator by id.

        get /v1/public/creators/{creatorId}

        :param id: ID of Creator
        :type params: int
        
        :returns:  CreatorDataWrapper

        >>> m = Marvel(public_key, private_key)
        >>> cdw = m.get_creator(30)
        >>> print cdw.data.count
        1
        >>> print cdw.data.result.fullName
        Stan Lee
        """

        url = "%s/%s" % (Creator.resource_url(), id)
        response = self._call(url)
        return CreatorDataWrapper(self, response, **kwargs)

    def get_creators(self, **kwargs):
        """Fetches lists of creators.
        
        get /v1/public/creators
        
        :returns:  CreatorDataWrapper

        >>> m = Marvel(public_key, private_key)
        >>> cdw = m.get_creators(lastName="Lee", orderBy="firstName,-modified", limit="5", offset="15")
        >>> print cdw.data.total
        25
        >>> print cdw.data.results[0].fullName
        Alvin Lee
        """

        response = self._call(Creator.resource_url(), **kwargs)
        return CreatorDataWrapper(self, response, **kwargs)

    def get_event(self, id, **kwargs):
        """Fetches a single event by id.

        get /v1/public/event/{eventId}

        :param id: ID of Event
        :type params: int
        
        :returns:  EventDataWrapper

        >>> m = Marvel(public_key, private_key)
        >>> response = m.get_event(253)
        >>> print response.data.result.title
        Infinity Gauntlet
        """

        url = "%s/%s" % (Event.resource_url(), id)
        response = self._call(url)
        return EventDataWrapper(self, response, **kwargs)

    def get_events(self, **kwargs):
        """Fetches lists of events.

        get /v1/public/events

        :returns:  EventDataWrapper

        >>> #Find all the events that involved both Hulk and Wolverine
        >>> #hulk's id: 1009351
        >>> #wolverine's id: 1009718
        >>> m = Marvel(public_key, private_key)
        >>> response = m.get_events(characters="1009351,1009718")
        >>> print response.data.total
        38
        >>> events = response.data.results
        >>> print events[1].title
        Age of Apocalypse
        """

        response = self._call(Event.resource_url(), **kwargs)
        return EventDataWrapper(self, response, **kwargs)

    def get_single_series(self, id):
        """Fetches a single comic series by id.

        get /v1/public/series/{seriesId}

        :param id: ID of Series
        :type params: int
        
        :returns:  SeriesDataWrapper
        
        >>> m = Marvel(public_key, private_key)
        >>> response = m.get_single_series(12429)
        >>> print response.data.result.title
        5 Ronin (2010)
        """

        url = "%s/%s" % (Series.resource_url(), id)
        response = self._call(url)
        return SeriesDataWrapper(self, response)

    def get_series(self, **kwargs):
        """Fetches lists of events.

        get /v1/public/events
        
        :returns:  SeriesDataWrapper
        
        >>> #Find all the series that involved Wolverine
        >>> #wolverine's id: 1009718
        >>> m = Marvel(public_key, private_key)
        >>> response = m.get_series(characters="1009718")
        >>> print response.data.total
        435
        >>> series = response.data.results
        >>> print series[0].title
        5 Ronin (2010)
        """

        response = self._call(Series.resource_url(), **kwargs)
        return SeriesDataWrapper(self, response, **kwargs)

    def get_story(self, id, **kwargs):
        """Fetches a single story by id.

        get /v1/public/stories/{storyId}

        :param id: ID of Story
        :type params: int
        
        :returns:  StoryDataWrapper
        
        >>> m = Marvel(public_key, private_key)
        >>> response = m.get_story(29)
        >>> print response.data.result.title
        Caught in the heart of a nuclear explosion, mild-mannered scientist Bruce Banner finds himself...
        """

        url = "%s/%s" % (Story.resource_url(), id)
        response = self._call(url)
        return StoryDataWrapper(self, response, **kwargs)

    def get_stories(self, **kwargs):
        """Fetches lists of stories.

        get /v1/public/stories
        
        :returns:  StoryDataWrapper
        
        >>> #Find all the stories that involved both Hulk and Wolverine
        >>> #hulk's id: 1009351
        >>> #wolverine's id: 1009718
        >>> m = Marvel(public_key, private_key)
        >>> response = m.get_stories(characters="1009351,1009718")
        >>> print response.data.total
        4066
        >>> stories = response.data.results
        >>> print stories[1].title
        Cover #477
        """

        response = self._call(Story.resource_url(), **kwargs)
        return StoryDataWrapper(self, response, **kwargs)
