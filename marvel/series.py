# -*- coding: utf-8 -*-

__author__ = 'Garrett Pennington'
__date__ = '02/07/14'

from .structures import DataWrapper, DataContainer, DataItem, Image
from .summaries import SeriesSummary


class SeriesDataWrapper(DataWrapper):

    @property
    def data(self):
        return DataContainer(self.marvel, self.dict['data'], Series)

    def next(self, **kwargs):
        return self._next(self.marvel.get_series, **kwargs)

    def previous(self, **kwargs):
        return self._previous(self.marvel.get_series, **kwargs)


class Series(DataItem):

    """
    Series object
    Takes a dict of character attrs
    """
    _resource_url = 'series'

    @property
    def title(self):
        return self.dict['title']

    @property
    def urls(self):
        return self.dict['urls']

    @property
    def startYear(self):
        return int(self.dict['startYear'])

    @property
    def endYear(self):
        return int(self.dict['endYear'])

    @property
    def rating(self):
        return self.dict['rating']

    @property
    def thumbnail(self):
        return Image(self.marvel, self.dict['thumbnail'])

    @property
    def next(self):
        return SeriesSummary(self.marvel, self.dict['next'])

    @property
    def previous(self):
        return SeriesSummary(self.marvel, self.dict['previous'])

    @property
    def series(self):
        raise AttributeError("'Series' has no attribute series")

    def get_series(self):
        raise AttributeError("'Series' has no attribute get_series")


