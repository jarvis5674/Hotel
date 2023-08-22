from .utils import *


class Guest:
    """ represents a guest at the spa"""

    def __init__(self, *args):
        self.id = args[0]
        self.first_name = args[1]
        self.last_name = args[2]
        self.vacation_start = datetime.datetime.utcfromtimestamp(args[3] or datetime_to_unix(datetime.datetime.now()))
        self.vacation_end = datetime.datetime.utcfromtimestamp(args[4] or datetime_to_unix(datetime.datetime.now()))
        self.group_id = args[5] or None

    def __str__(self):
        return """(%s,'%s','%s', %s, %s, %s)""" % (
            self.id or 'NULL',
            self.first_name,
            self.last_name,
            datetime_to_unix(self.vacation_start),
            datetime_to_unix(self.vacation_end),
            self.group_id or 'NULL'
        )