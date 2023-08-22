import sys
from .utils import *


class Appointment:
    """ Class that stores appointments when customers are using the service """

    def __init__(self, *args):
        sys.stderr.write("{}\n".format(args))
        self.id = args[0]
        self.date_time = datetime.datetime.utcfromtimestamp(args[1])
        self.guest_id = args[2]
        self.service_id = args[3]
        self.service_type = args[4]
        self.service_time = args[5]
        self.status = args[6]
        self.created_at = datetime.datetime.utcfromtimestamp(args[7])

    def __str__(self):
        return """(%s,'%s',%s,%s,%s,%s,'%s','%s')""" % (
            self.id if self.id is not None else 'NULL',
            datetime_to_unix(self.date_time),
            self.guest_id,
            self.service_id,
            self.service_type if self.service_type is not None else 'NULL',
            self.service_time if self.service_time is not None else 'NULL',
            self.status,
            datetime_to_unix(self.created_at)
        )

    def overlaps_with(self, other_appointment):
        sys.stderr.write("self {} {}\n".format(self.start_time, self.end_time))
        sys.stderr.write("other {} {}\n".format(other_appointment.start_time, other_appointment.end_time))
        if other_appointment.end_time > self.start_time:
            return True
        if other_appointment.start_time < self.end_time:
            return True
        return False

    @property
    def end_time(self):
        return self.start_time + self.service_time * 60

    @property
    def start_time(self):
        return datetime_to_unix(self.date_time)
