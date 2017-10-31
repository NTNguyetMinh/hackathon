from __future__ import (
    absolute_import,
    unicode_literals,
)
from abc import ABCMeta, abstractmethod

class AbstractService(object):
    __metaclass__ = ABCMeta

    @property
    def url(self):
        pass

    @property
    def create_params(self, kwargs):
        pass

    @abstractmethod
    def send_request(self):
        pass

    @abstractmethod
    def process_response(self, response):
        pass

    def run(self, *kwargs):
        self.create_params(params=kwargs)
        response = self.send_request()
        result = self.process_response(response)
        return result
