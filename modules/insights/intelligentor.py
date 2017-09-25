#! /usr/bin/env python
# -*- coding: utf-8 -*-

from . import socialnetworks
from . import intelrss

class Intelligentor():

    def __init__(self, search):
        self.search = search
        self.result = None


    def __iter__(self):
        self._parse_search()
        return iter(self.result)


    def _parse_search(self):

        search = self.search.split(" ")
        print(search)
        if search[0].startswith("/"):
            command = search[0]
            search.pop(0)

        if command == "/social":
            self._social(search)

        elif command == "/rss":
            self._rss(search)

    def _social(self, search):
        sn = socialnetworks.SocialNetworks(search)
        self.result = sn

    def _rss(self, search):
        result = intelrss.RSS(search)
        self.result = result.get()
