# -*- coding: utf-8 -*-

__author__ = 'Garrett Pennington'
__date__ = '02/07/14'

from .core import MarvelObject
from .structures import DataWrapper, DataItem, DataContainer, TextObject, Image
from .summaries import ComicSummary

class ComicDataWrapper(DataWrapper):

    """
    :param marvel: Instance of Marvel class
    :type marvel: marvel.Marvel
    :parm dict: Dict of object, created from json response.
    :type dict: dict
    :parm params: Optional dict of query params sent to original API call
    :type params: dict
    
    """
    @property
    def data(self):
        return DataContainer(self.marvel, self.dict['data'], Comic)

    def next(self):
        return self._next(self.marvel.get_comics)

    def previous(self):
        return self._previous(self.marvel.get_comics)


class Comic(DataItem):

    """
    :param marvel: Instance of Marvel class
    :type marvel: marvel.Marvel
    :param dict: Dict of object, created from json response.
    :type dict: dict    
    """
    _resource_url = 'comics'

    @property
    def digitalId(self):
        return int(self.dict['digitalId'])

    @property
    def title(self):
        return self.dict['title']

    @property
    def issueNumber(self):
        return float(self.dict['issueNumber'])

    @property
    def variantDescription(self):
        return self.dict['description']

    @property
    def isbn(self):
        return self.dict['isbn']

    @property
    def upc(self):
        return self.dict['upc']

    @property
    def diamondCode(self):
        return self.dict['diamondCode']

    @property
    def ean(self):
        return self.dict['ean']

    @property
    def issn(self):
        return self.dict['issn']

    @property
    def format(self):
        return self.dict['format']

    @property
    def pageCount(self):
        return int(self.dict['pageCount'])

    @property
    def textObjects(self):
        """
        :returns: list -- List of TextObjects
        """
        return self.list_to_instance_list(self.dict['textObjects'], TextObject)

    @property
    def urls(self):
        return self.dict['urls']

    @property
    def series(self):
        return self.dict['series']

    @property
    def variants(self):
        """
        Returns List of ComicSummary objects
        """
        return self.list_to_instance_list(self.dict['variants'], ComicSummary)

    @property
    def collections(self):
        """
        Returns List of ComicSummary objects
        """
        return self.list_to_instance_list(self.dict['collections'], ComicSummary)

    @property
    def collectedIssues(self):
        """
        Returns List of ComicSummary objects
        """
        return self.list_to_instance_list(self.dict['collectedIssues'], ComicSummary)

    @property
    def dates(self):
        return self.list_to_instance_list(self.dict['dates'], ComicDate)

    @property
    def prices(self):
        return self.list_to_instance_list(self.dict['prices'], ComicPrice)

    @property
    def thumbnail(self):
        return Image(self.marvel, self.dict['thumbnail'])

    @property
    def images(self):
        return self.list_to_instance_list(self.dict['images'], Image)

    @property
    def comics(self):
        raise AttributeError("'Comic' has no attribute comics")

    def get_comics(self):
        raise AttributeError("'Comic' has no attribute get_comics")


class ComicDate(MarvelObject):

    """
    ComicDate object
    """
    @property
    def type(self):
        return self.dict['type']

    @property
    def date(self):
        return self.str_to_datetime(self.dict['date'])

    @property
    def date_raw(self):
        return self.dict['date']


class ComicPrice(MarvelObject):

    """
    ComicPrice object
    """
    @property
    def type(self):
        return self.dict['type']

    @property
    def price(self):
        return float(self.dict['price'])
