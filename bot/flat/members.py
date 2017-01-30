# coding=utf-8
#

from flat.api_actions import get_users_from_api_endpoint


class Member(object):

    def __init__(self, name, total):
        self.name = name
        self.total = total

    def to_dict(self):
        return {
            "name": self.name,
            "total": self.total
        }


def get_members(home):
    user_list = get_users_from_api_endpoint(home)
    return [Member(user["username"], user["total"]).to_dict() for user in user_list]
