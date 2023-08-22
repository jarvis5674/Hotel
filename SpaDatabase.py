import datetime
import time
import sys
import os
from .Appointment import Appointment
from .Database import Database, Schema
from .Group import Group
from .Guest import Guest
from .Service import Service
from .Criteria import *


GUEST_TABLE_NAME = "Guest"
GUEST_TABLE_FIELDS = [
    ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
    ("first_name", "TEXT"),
    ("last_name", "TEXT"),
    ("vacation_start", "INTEGER"),
    ("vacation_end", "INTEGER"),
    ("group_id", "INTEGER")
]

GROUP_TABLE_NAME = "TravelGroup"
GROUP_TABLE_FIELDS = [
    ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
    ("description", "TEXT"),
    ("owner_id", "INTEGER")
]

SERVICE_TABLE_NAME = "Service"
SERVICE_TABLE_FIELDS = [
    ("id", "INTEGER"),
    ("name", "TEXT"),
    ("price", "REAL"),
]

SERVICE_TYPE_TABLE_NAME = "ServiceType"
SERVICE_TYPE_TABLE_FIELDS = [
    ("service_id", "INTEGER"),
    ("subtype_id", "INTEGER"),
    ("name", "TEXT"),
]

SERVICE_TIME_TABLE_NAME = "ServiceTime"
SERVICE_TIME_TABLE_FIELDS = [
    ("service_id", "INTEGER"),
    ("minutes", "INTEGER")
]

APPOINTMENT_TABLE_NAME = "Appointment"
APPOINTMENT_TABLE_FIELDS = [
    ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
    ("date", "INTEGER"),
    ("guest_id", "INTEGER"),
    ("service_id", "INTEGER"),
    ("service_type", "INTEGER"),
    ("service_time", "INTEGER"),
    ("status", "TEXT"),
    ("created_at", "INTEGER")
]

CREDENTIAL_TABLE_NAME = "Credentials"
CREDENTIAL_TABLE_FIELDS = [
    ("username", "TEXT"),
    ("password", "TEXT"),
    ("admin_rights", "INTEGER")
]

_SECONDS_IN_EIGHT_HOURS = 8 * 60 * 60
_SECONDS_IN_TWENTY_HOURS = 20 * 60 * 60


class SpaDatabase(Database):
    """ Specialized database for MiYE """

    def __init__(self, path):
        super(SpaDatabase, self).__init__(path)

        if not os.path.exists(self._path):
            sys.stderr.write("Database file does not exist. Creating new database\n")
            self.reset()

    def get_all_guests(self):
        query = "SELECT * FROM %s" % (GUEST_TABLE_NAME,)
        self._make_query(query)
        return [Guest(*x) for x in self.results]

    def get_guests(self, criteria = None):
        """ Get guest """
        def build_where_clause():
            """ build the where clause """
            if isinstance(criteria, int):
                return "WHERE %s = %s" % (GUEST_TABLE_FIELDS[0][0], criteria)
            if isinstance(criteria, Group):
                return "WHERE %s = %s" % (GUEST_TABLE_FIELDS[5][0], criteria.id)

        query = "SELECT * FROM %s " % (GUEST_TABLE_NAME,)
        where = build_where_clause()

        if where:
            query += " " + where

        self._make_query(query)
        return [Guest(*x) for x in self.results]

    def get_all_appointments(self, criteria=None):
        """ Get all the appointments """
        def build_where_clause():
            """ build the where clause """
            if isinstance(criteria, int):
                return "WHERE %s = %s" % (APPOINTMENT_TABLE_FIELDS[2][0], criteria)
            elif isinstance(criteria, Guest):
                return "WHERE %s = %s" % (APPOINTMENT_TABLE_FIELDS[2][0], criteria)
            elif isinstance(criteria, GuestCriteria):
                return "WHERE %s = %s" % (APPOINTMENT_TABLE_FIELDS[2][0], criteria.guest_id)
            elif isinstance(criteria, GroupCriteria):
                return "INNER JOIN {0} ON {0}.{1} = {2}.{3} WHERE {0}.{4}={5}".format(
                    GUEST_TABLE_NAME,
                    GUEST_TABLE_FIELDS[0][0],
                    APPOINTMENT_TABLE_NAME,
                    APPOINTMENT_TABLE_FIELDS[2][0],
                    GUEST_TABLE_FIELDS[5][0],
                    criteria.group_id
                )
            elif isinstance(criteria, tuple):
                clause = []
                for x in criteria:
                    if isinstance(x, datetime.date):
                        date = x
                        lower_limit = time.mktime(date.timetuple()) + _SECONDS_IN_EIGHT_HOURS - self._UTC_OFFSET_TIMEDELTA
                        upper_limit = time.mktime(date.timetuple()) + _SECONDS_IN_TWENTY_HOURS - self._UTC_OFFSET_TIMEDELTA

                        clause.append("{0}>={1} AND {0}<={2}".format(APPOINTMENT_TABLE_FIELDS[1][0], int(lower_limit), int(upper_limit)))
                    if isinstance(x, int):
                        clause.append("{0}={1}".format(APPOINTMENT_TABLE_FIELDS[3][0], x))

                return "WHERE {}".format(" AND ".join(clause))
            elif isinstance (criteria, TimeSpanCriteria):
                return "WHERE %s > %s AND %s < %s" % (APPOINTMENT_TABLE_FIELDS[1][0], criteria.min, APPOINTMENT_TABLE_FIELDS [1][0], criteria.max)

        query = "SELECT * FROM %s" % (APPOINTMENT_TABLE_NAME,)
        where = build_where_clause()

        if where:
            query += " " + where
        self._make_query(query)
        return [Appointment(*x) for x in self.results]

    def get_all_services(self):
        query = """SELECT T.service_id, T.subtype_id, T.name, S.name, S.price, M.minutes \
        FROM {0} T \
        INNER JOIN {1} S \
        ON T.service_id = S.id \
        INNER JOIN {2} M
        ON M.service_id = S.id""".format(SERVICE_TYPE_TABLE_NAME, SERVICE_TABLE_NAME, SERVICE_TIME_TABLE_NAME)
        self._make_query(query)

        sys.stderr.write("{}\n".format(self.results))
        return [Service(*x) for x in self.results]

    def get_all_credentials(self):
        query = "SELECT {}, {} FROM {}".format(
            CREDENTIAL_TABLE_FIELDS[0][0],
            CREDENTIAL_TABLE_FIELDS[2][0],
            CREDENTIAL_TABLE_NAME
        )

        self._make_query(query)
        return [x for x in self.results]

    def insert_guest(self, guest):
        """ insert a guest """
        query = "INSERT OR IGNORE INTO %s VALUES %s" % (GUEST_TABLE_NAME, str(guest))
        self._insert_query(query)
        return self.results[0][0]

    def insert_group(self, group):
        """ insert a group """
        query = "INSERT OR IGNORE INTO %s VALUES %s" % (GROUP_TABLE_NAME, str(group))
        return self._insert_query(query)

    def insert_credentials(self, username, password, admin_rights):
        """ insert a credential """
        query = "INSERT INTO {} values('{}', '{}', {})".format(
            CREDENTIAL_TABLE_NAME,
            username,
            password,
            admin_rights
        )
        return self._insert_query(query)

    def reset(self):
        if os.path.exists(self._path):
            os.remove(self._path)
        self.create_credentials_table()
        self.create_guest_table()
        self.create_group_table()
        self.create_service_table()
        self.create_appointment_table()

    def insert_appointment(self, appointment):
        query = "INSERT OR IGNORE INTO %s VALUES %s" % (APPOINTMENT_TABLE_NAME, str(appointment))
        self._insert_query(query)

    def cancel_appointment(self, appointment_id):
        """ cancel appointment """
        query = "UPDATE %s SET %s = 'CANCELLED' WHERE %s = '%s'" % (
            APPOINTMENT_TABLE_NAME,
            APPOINTMENT_TABLE_FIELDS[6][0],
            APPOINTMENT_TABLE_FIELDS[0][0],
            appointment_id
        )
        self._make_query(query)

    def void_appointment(self, appointment_id):
        """ void appointment """
        query = "UPDATE %s SET %s = 'VOIDED' WHERE %s = '%s'" % (
            APPOINTMENT_TABLE_NAME,
            APPOINTMENT_TABLE_FIELDS[6][0],
            APPOINTMENT_TABLE_FIELDS[0][0],
            appointment_id
        )
        self._make_query(query)

    def get_service_name(self, service_id=None, service_type=None):
        """ get the name of a service """
        if not service_id:
            query = "SELECT %s FROM %s" % (
                SERVICE_TABLE_FIELDS[1][0],
                SERVICE_TABLE_NAME,
            )
        elif not service_type:
            query = "SELECT %s FROM %s WHERE %s=%s" % (
                SERVICE_TABLE_FIELDS[1][0],
                SERVICE_TABLE_NAME,
                SERVICE_TABLE_FIELDS[0][0],
                service_id
            )
        else:
            query = """SELECT B.{0},A.{1}\
            FROM {2} A\
            INNER JOIN {7} B\
            ON A.{8}=B.{3}\
            WHERE B.{3}={4} AND B.{5}={6}""".format(
                SERVICE_TABLE_FIELDS[1][0], # service name
                SERVICE_TYPE_TABLE_FIELDS[2][0], # service type name
                SERVICE_TABLE_NAME,
                SERVICE_TYPE_TABLE_FIELDS[0][0], # service type
                service_id,
                SERVICE_TYPE_TABLE_FIELDS[1][0], # service id
                service_type,
                SERVICE_TYPE_TABLE_NAME,
                SERVICE_TABLE_FIELDS[0][0],
            )

        self._make_query(query)
        return [" ".join(x) for x in self.results]

    def get_service_types(self, service_id):
        """ get the service types of a service """
        query = """SELECT %s FROM %s WHERE %s=%s""" % (
            SERVICE_TYPE_TABLE_FIELDS[2][0],
            SERVICE_TYPE_TABLE_NAME,
            SERVICE_TYPE_TABLE_FIELDS[0][0],
            service_id
        )
        self._make_query(query)
        return self.results

    def get_group(self, group_id):
        """ get the group from an id"""
        query = "SELECT * FROM %s WHERE id = '%s'" % (GROUP_TABLE_NAME, group_id)
        self._make_query(query)
        group_data = self.results[0]
        return Group(*group_data)

    def get_service_time(self, service_id):
        """ get the service time of a service """
        query = """SELECT %s FROM %s WHERE %s=%s""" % (
            SERVICE_TIME_TABLE_FIELDS[1][0],
            SERVICE_TIME_TABLE_NAME,
            SERVICE_TIME_TABLE_FIELDS[0][0],
            service_id
        )

        self._make_query(query)
        return self.results

    def get_service_price(self, service_id):
        """ get the price of a service """
        query = """ SELECT %s FROM %s WHERE %s = %s """ % (
            SERVICE_TABLE_FIELDS[2][0],
            SERVICE_TABLE_NAME,
            SERVICE_TABLE_FIELDS[0][0],
            service_id
        )

        self._make_query(query)
        return self.results[0][0]

    def check_credential(self, user_name, password):
        """ check credential """
        query = """ SELECT %s FROM %s WHERE %s = '%s' """ % (
            CREDENTIAL_TABLE_FIELDS[1][0],
            CREDENTIAL_TABLE_NAME,
            CREDENTIAL_TABLE_FIELDS[0][0],
            user_name
        )

        self._make_query(query)
        sys.stderr.write("{}".format(self.results))
        cache_password = self.results[0][0]

        self.results = None
        return cache_password == password

    def has_admin_rights(self, user_name):
        query = """ SELECT %s FROM %s WHERE %s = '%s' """ % (
            CREDENTIAL_TABLE_FIELDS[2][0],
            CREDENTIAL_TABLE_NAME,
            CREDENTIAL_TABLE_FIELDS[0][0],
            user_name
        )

        self._make_query(query)
        sys.stderr.write("{}\n".format(self.results))
        return bool(self.results[0][0])

    def create_guest_table(self):
        table_schema = Schema(GUEST_TABLE_NAME, GUEST_TABLE_FIELDS)
        self._create_table(table_schema)
        self._read_data_into_table("guest_data.csv", table_schema.editable_fields(), table_schema.name)

    def create_group_table(self):
        table_schema = Schema(GROUP_TABLE_NAME, GROUP_TABLE_FIELDS)
        self._create_table(table_schema)
        self._read_data_into_table("group_data.csv", table_schema.editable_fields(), table_schema.name)

    def create_credentials_table(self):
        table_schema = Schema(CREDENTIAL_TABLE_NAME, CREDENTIAL_TABLE_FIELDS)
        self._create_table(table_schema)
        self._read_data_into_table("credentials.csv", table_schema.editable_fields(), table_schema.name)

    def create_service_table(self):
        service_table_schema = Schema(SERVICE_TABLE_NAME, SERVICE_TABLE_FIELDS)
        self._create_table(service_table_schema)
        self._read_data_into_table(
            "service_type.csv",
            service_table_schema.editable_fields(),
            service_table_schema.name
        )

        service_type_table_schema = Schema(SERVICE_TYPE_TABLE_NAME, SERVICE_TYPE_TABLE_FIELDS)
        self._create_table(service_type_table_schema)
        self._read_data_into_table(
            "service_subtype.csv",
            service_type_table_schema.editable_fields(),
            service_type_table_schema.name
        )

        service_time_table_schema = Schema(SERVICE_TIME_TABLE_NAME, SERVICE_TIME_TABLE_FIELDS)
        self._create_table(service_time_table_schema)
        self._read_data_into_table(
            "service_time.csv",
            service_time_table_schema.editable_fields(),
            service_time_table_schema.name
        )

    def create_appointment_table(self):
        appointment_table_schema = Schema(APPOINTMENT_TABLE_NAME, APPOINTMENT_TABLE_FIELDS)
        self._create_table(appointment_table_schema)
        self._read_data_into_table(
            "appointment_data.csv",
            appointment_table_schema.editable_fields(),
            appointment_table_schema.name
        )

    def update_guest_group_id(self, guest, group_id):
        """ add a guest to a group """
        query = "UPDATE %s SET %s = '%s' WHERE %s = '%s'" % (
            GUEST_TABLE_NAME,
            GUEST_TABLE_FIELDS[5][0],
            group_id,
            GUEST_TABLE_FIELDS[0][0],
            guest.id
        )
        self._make_query(query)

    def list_groups(self):
        """ list all the groups """
        query = "SELECT * FROM %s" % (GROUP_TABLE_NAME)
        self._make_query(query)
        return [Group(*x) for x in self.results]

        
    


if __name__ == '__main__':
    _RESET_ALL = False

    if os.path.exists("temp.db") and _RESET_ALL:
        os.remove("temp.db")

    database = SpaDatabase("temp.db")

    database.create_service_table()
    database.get_all_services()
    print(database.results)

    database.create_guest_table()
    database.get_guests()
    print(database.results)

    database.create_appointment_table()
    database.get_all_appointments()
    print(database.results)

    database.get_all_appointments(15)
    print(database.results)

    database.get_all_appointments((datetime.date(2019, 10, 10),))
    print(database.results)

    database.get_all_appointments((datetime.date(2019, 10, 10), 4))
    print(database.results)

    print(database.get_service_name(1))
    print(database.results)

    print(database.get_service_name(2))
    print(database.results)

    print(database.get_service_name(3))
    print(database.results)

    print(database.get_service_types(4))
    print(database.results)

    print(database.get_service_types(1))
    print(database.results)

    print(database.get_service_types(2))
    print(database.results)

    print(database.get_service_types(3))
    print(database.results)

    print(database.get_service_types(4))
    print(database.results)

    print(database.get_service_name(1, 1))
    print(database.results)

    print(database.get_service_name(2, 1))
    print(database.results)

    print(database.get_service_name(2, 2))
    print(database.results)

    print(database.get_service_time(1))
    print(database.results)

    print(database.get_service_time(2))
    print(database.results)

    print(database.get_service_time(3))
    print(database.results)

    print(database.get_service_time(4))
    print(database.results)

    print(database.get_service_price(1))

    print(database.get_service_price(2))

    print(database.get_service_price(3))

    print(database.get_service_price(4))
