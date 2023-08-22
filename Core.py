import sys
import hashlib
from . import resources
from .Constants import *
from .SpaDatabase import SpaDatabase


class Core:
    """ Core logic """

    def __init__(self):
        self.database = SpaDatabase(DATABASE_PATH)
        self.admin_rights = None
        pass

    def authenticate(self, username, password):
        """ authenticate to determine admin rights """
        sha256 = hashlib.sha256()
        sha256.update(str.encode(password))
        digest = sha256.hexdigest()

        sys.stderr.write("{}\n".format(digest))

        if not self.database.check_credential(username, digest):
            return False

        self.admin_rights = self.database.has_admin_rights(username)

        return True

    def register_appointment(self, appointment):
        """ register an appointment in the database """

        appointment_date = appointment.date_time
        service = appointment.service_id
        guest_id = appointment.guest_id

        guest = self.database.get_guests(guest_id)[0]

        day_appointments = self.database.get_all_appointments((appointment_date,))
        guest_appointments = [x for x in day_appointments if x.guest_id == guest.id and x.status == "RESERVED"]
        service_appointments = [x for x in day_appointments if x.service_id == service and x.status == "RESERVED"]

        has_overlap = False
        service_overlap = False

        for i in guest_appointments:
            has_overlap |= appointment.overlaps_with(i)
            sys.stderr.write("{}\n".format(has_overlap))

        for i in service_appointments:
            service_overlap |= appointment.overlaps_with(i)

        sys.stderr.write("{}\n".format(service_overlap))

        self.database.insert_appointment(appointment)
        sys.stderr.write("appointment inserted\n")

    def reset_database(self):
        sys.stderr.write("core reset database\n")
        self.database.reset()

    def register_guest(self, guest):
        return self.database.insert_guest(guest)

    def add_guest_to_group(self, guest, group):
        """ update guest to a group """
        valid_group_ids = [group.id for group in self.database.list_groups()]
        sys.stderr.write("{}\n".format(valid_group_ids))
        sys.stderr.write("{}\n".format(group.id in valid_group_ids))

        if group.id in valid_group_ids:
            self.database.update_guest_group_id(guest, group.id)
        else:
            raise RuntimeError(resources.strings.INVALID_GROUP_ID)

    def register_group(self, group):
        """ insert a group """
        self.database.insert_group(group)
        return self.database.results[0][0]

    def register_credentials(self, username, password, admin_rights=False):
        """ register an account with the database """
        # TODO: Check if username already exists

        sha256 = hashlib.sha256()
        sha256.update(str.encode(password))
        digest = sha256.hexdigest()

        self.database.insert_credentials(username, digest, admin_rights)


