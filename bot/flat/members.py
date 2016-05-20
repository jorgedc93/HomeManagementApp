#!/usr/bin/env python3.5
# coding=utf-8
#

class Member(object):

    def __init__(self, name, total):
        self.name = name
        self.total = total

    def to_dict(self):
        return {
            "name": self.name,
            "total": self.total
        }
