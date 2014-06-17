# -*- coding: utf-8 -*-

__author__ = 'Garrett Pennington'
__date__ = '02/07/14'

from .structures import DataItem, DataWrapper, DataContainer, Image
from .summaries import EventSummary


class EventDataWrapper(DataWrapper):

    @property
    def data(self):
        return DataContainer(self.marvel, self.dict['data'], Event)

    def next(self):
        return self._next(self.marvel.get_events)

    def previous(self):
        return self._previous(self.marvel.get_events)


class Event(DataItem):

    """
    Event object
    Takes a dict of character attrs
    """
    _resource_url = 'events'

    @property
    def title(self):
        return self.dict['title']

    @property
    def urls(self):
        return self.dict['urls']

    @property
    def modified(self):
        return self.str_to_datetime(self.dict['modified'])

    @property
    def modified_raw(self):
        return self.dict['modified']

    @property
    def start(self):
        return self.str_to_datetime(self.dict['start'])

    @property
    def start_raw(self):
        return self.dict['start']

    @property
    def end(self):
        return self.str_to_datetime(self.dict['end'])

    @property
    def end_raw(self):
        return self.dict['end']

    @property
    def thumbnail(self):
        return Image(self.marvel, self.dict['thumbnail'])

    @property
    def next(self):
        return EventSummary(self.marvel, self.dict['next'])

    @property
    def previous(self):
        return EventSummary(self.marvel, self.dict['previous'])

    @property
    def events(self):
        raise AttributeError("'Event' has no attribute events")

    def get_events(self):
        raise AttributeError("'Event' has no attribute get_events")
