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
