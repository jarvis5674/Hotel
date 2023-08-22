import sys
import time
import getpass

from . import resources
from .utils import *
from .Constants import *
from .Core import Core
from .Group import Group
from .Guest import Guest
from .Interface import Interface
from .SpaDatabase import SpaDatabase
from .Appointment import Appointment
from .Criteria import *


class Program:
    """ main program in MiYE"""

    _SECONDS_IN_TEN_MINUTES = 60 * 10
    _SECONDS_IN_THIRTY_MINUTES = 60 * 30
    _SECONDS_IN_NINETY_MINUTES = 60 * 90

    def __init__(self):
        """ initializes and welcome user to MiYE """
        sys.stderr.write("initializing program\n")

        self.core = Core()
        self.interface = Interface()
        self.database = SpaDatabase(DATABASE_PATH)

        self._clerk_functions = [
            None,
            self._list_services,
            self._print_invoice,
            self._manage_appointments,
        ]

        self._admin_functions = [
            None,
            self._register_guest,
            self._manage_appointments,
            self._manage_groups,
            self._print_invoice,
            self._list_weekly_services,
            self._manage_database
        ]

        self._manage_group_functions = [
            None,
            self._create_group,
            self._add_guest_to_group,
            self._list_groups,
        ]

        self._manage_appointment_functions = [
            None,
            self._register_appointment,
            self._cancel_appointment,
            self._list_availability,
        ]

        self._manage_database_functions = [
            None,
            self._list_services,
            self._list_appointments,
            self._list_guests,
            self._list_groups,
            self._list_credentials,
            self._create_account,
            self.core.reset_database
        ]

        self.interface.clear_screen()

    @property
    def active_functions(self):
        return self._admin_functions if self.core.admin_rights else self._clerk_functions

    @property
    def menu_choices(self):
        return resources.strings.MENU if self.core.admin_rights else resources.strings.MENU_CLERK

    def start(self):
        self._authenticate()
        self._main_menu()

    def _authenticate(self):
        username = input(resources.strings.ENTER_USERNAME)
        password = getpass.getpass(resources.strings.ENTER_PASSWORD_PROMPT)

        if not self.core.authenticate(username, password):
            print(resources.strings.WRONG_LOGIN)
            exit(-1)

        self.interface.clear_screen(self.core.admin_rights)

    def _get_service_input(self):
        self.interface.display_message(resources.strings.ENTER_SERVICE)
        self.database.get_service_name()

        selection, service = self.interface.prompt_selection(self.database.results)
        sys.stderr.write("service entered {}\n".format(service))
        return selection

    def _get_service_type_input(self, service_id):
        self.database.get_service_types(service_id)
        if not self.database.results:
            return 1

        self.interface.display_message(resources.strings.ENTER_SERVICE_TYPE)

        selection, service_type = self.interface.prompt_selection(self.database.results)
        sys.stderr.write("service entered {}\n".format(service_type))
        return selection

    def _get_service_time_input(self, service_id):
        """ get the service time"""
        print()
        print(resources.strings.ENTER_SERVICE_TIME)
        self.database.get_service_time(service_id)
        for index, i in enumerate(self.database.results):
            print("{0} - {1} {2}".format(str(index + 1), i[0], resources.strings.MINUTES))

        minutes = int(input())
        if minutes > len(self.database.results):
            raise RuntimeError
        return int(self.database.results[minutes - 1][0])

    def _main_menu(self):
        """ main menu to prompt user to select action """
        self._menu(self.menu_choices, self.active_functions)
        print(resources.strings.EXIT)

    def _menu(self, menu, menu_functions):
        while True:
            for command in menu:
                print(command)

            key = input()
            if key == "E" or key == "e":
                self.interface.clear_screen(self.core.admin_rights)
                break
            try:
                selection = int(key)
                self.interface.clear_screen(self.core.admin_rights)
                menu_functions[selection]()
            except ValueError as e:
                self.interface.clear_screen(self.core.admin_rights)
                sys.stderr.write(str(e) + '\n')
                print(resources.strings.INVALID_SELECTION)
            except IndexError as e:
                self.interface.clear_screen(self.core.admin_rights)
                sys.stderr.write(str(e) + '\n')
                print(resources.strings.UNKNOWN_SELECTION)
            except RuntimeError as e:
                self.interface.clear_screen(self.core.admin_rights)
                sys.stderr.write(str(e) + '\n')
                print(str(e) if e else resources.strings.UNKNOWN_ERROR)
            except Exception as e:
                sys.stderr.write(str(e) + '\n')
                pass

            print()

    def _register_appointment(self):
        guest_id = self.interface.prompt_guest_id()
        guest = self.database.get_guests(guest_id)[0]
        self.interface.display_guests([guest])

        appointment_date = self.interface.prompt_date()

        if appointment_date < guest.vacation_start or appointment_date > guest.vacation_end:
            raise RuntimeError(resources.strings.GUEST_NOT_STAYING)

        appointment_time = self.interface.prompt_time()

        if appointment_time.hour < 8 or appointment_time.hour >= 20:
            raise RuntimeError(resources.strings.OUTSIDE_SERVICE_HOURS)

        service = self._get_service_input()
        service_type = self._get_service_type_input(service)
        service_time = self._get_service_time_input(service)

        end_time = (
                datetime.datetime.combine(appointment_date, appointment_time) + datetime.timedelta(
            minutes=service_time)).time()
        sys.stderr.write("{}\n".format(end_time))

        if end_time.hour >= 20:
            raise RuntimeError(resources.strings.OUTSIDE_SERVICE_HOURS)

        created_at = time.mktime(datetime.datetime.now().timetuple())
        sys.stderr.write("{}\n".format(appointment_time))
        appointment_datetime = time.mktime(appointment_date.timetuple()) + (
                appointment_time.hour * 60 + appointment_time.minute) * 60

        appointment = Appointment(None, int(appointment_datetime), guest.id, service, service_type, service_time,
                                  "RESERVED", created_at)
        self.core.register_appointment(appointment)

    def _register_guest(self):
        first_name, last_name = self.interface.prompt_guest_name()
        start_date = self.interface.prompt_date()
        end_date = self.interface.prompt_date()

        guest = Guest(None, first_name, last_name, datetime_to_unix(start_date), datetime_to_unix(end_date), None)
        sys.stderr.write("guest information: %s\n" % (str(guest),))
        self.core.register_guest(guest)
        sys.stderr.write("guest inserted\n")

    def _list_services(self):
        """ list all the services """
        sys.stderr.write("getting services\n")
        services = self.database.get_all_services()
        self.interface.display_services(services)

    def _list_guests(self):
        """ list all the guests """
        sys.stderr.write("getting guests\n")
        guests = self.database.get_guests()
        sys.stderr.write("printing guests\n")
        self.interface.display_guests(guests)

    def _list_appointments(self):
        """ list all the appointments """
        sys.stderr.write("getting appointments\n")
        appointments = self.database.get_all_appointments()
        self.interface.display_appointments(appointments)

    def _list_credentials(self):
        """ list all the credentials """
        credentials = self.database.get_all_credentials()
        self.interface.display_credentials(credentials)

    def _cancel_appointment(self):
        """ cancel an appointment """
        sys.stderr.write("cancelling appointment\n")
        guest_id = self.interface.prompt_guest_id()
        guest = self.database.get_guests(guest_id)[0]

        appointments = self.database.get_all_appointments(guest)
        self.interface.display_appointments(appointments)
        self.interface.display_message(guest.first_name, guest.last_name)

        self.interface.display_message(resources.strings.ENTER_APPOINTMENT_ID)
        app_id = self.interface.prompt_int()

        appointment = next(x for x in appointments if x.id == app_id)
        now = datetime.datetime.now()
        if (now - appointment.created_at).total_seconds() < self._SECONDS_IN_TEN_MINUTES or \
                (appointment.date_time - now).total_seconds() > self._SECONDS_IN_NINETY_MINUTES:
            self.database.void_appointment(app_id)
            print(resources.strings.APPOINTMENT_VOIDED)
        else:
            if self.interface.prompt_continue(resources.strings.CHARGE_NOT_CLEARED):
                print()
                self.database.cancel_appointment(app_id)
                print(resources.strings.APPOINTMENT_CANCELLED)

    def _print_invoice(self):
        """ write out an invoice for a guest"""
        sys.stderr.write("printing invoice\n")

        guest_id = self.interface.prompt_guest_id()
        guest = self.database.get_guests(guest_id)[0]
        is_grouped = bool(guest.group_id)
        criteria = GroupCriteria(guest.group_id) if is_grouped else GuestCriteria(guest.id)
        appointments = self.database.get_all_appointments(criteria)

        self.interface.display_message(
            resources.strings.GROUP if is_grouped else "" + resources.strings.INVOICE,
            "-",
            guest.first_name,
            guest.last_name)

        self.interface.display_appointments(appointments)

        total_price = sum([self.database.get_service_price(appointment.service_id) * appointment.service_time
                           if appointment.status != "VOIDED" else 0
                           for appointment in appointments])

        self.interface.display_message(resources.strings.TOTAL_CHARGED, total_price)

    def _list_availability(self):
        """ list available for a service on a specific date """
        sys.stderr.write("searching for service availability")
        appointment_date = self.interface.prompt_date()
        service = self._get_service_input()
        appointments = self.database.get_all_appointments((appointment_date, service))

        if appointments:
            self.interface.display_appointments([x for x in appointments if x.status == "RESERVED"])
        else:
            print(resources.strings.NO_APPOINTMENTS)

    def _manage_groups(self):
        """ submenu to manage groups """
        self._menu(resources.strings.GROUP_MENU, self._manage_group_functions)

    def _manage_appointments(self):
        """ submenu to manage appointments """
        self._menu(resources.strings.APPOINTMENT_MENU, self._manage_appointment_functions)

    def _manage_database(self):
        """ submenu to manage database """
        self._menu(resources.strings.DATABASE_MENU, self._manage_database_functions)

    def _add_guest_to_group(self):
        """ add a guest to an existing group """
        groups = self.database.list_groups()
        self.interface.display_groups(groups)

        self.interface.display_message(resources.strings.ENTER_GROUP_ID)

        group_id = self.interface.prompt_int()
        group = self.database.get_group(group_id)

        owner_id = group.owner_id
        owner = self.database.get_guests(owner_id)[0]

        first_name, last_name = self.interface.prompt_guest_name()

        guest = Guest(
            None,
            first_name,
            last_name,
            None,
            None,
            group.id
        )

        guest.vacation_start = owner.vacation_start
        guest.vacation_end = owner.vacation_end

        self.core.register_guest(guest)

    def _create_group(self):
        """ create a group """
        first_name, last_name = self.interface.prompt_guest_name()
        vacation_start = self.interface.prompt_date()
        vacation_end = self.interface.prompt_date()

        guest = Guest(
            None,
            first_name,
            last_name,
            datetime_to_unix(vacation_start),
            datetime_to_unix(vacation_end),
            None
        )

        guest.id = self.core.register_guest(guest)
        description = " ".join([guest.first_name, guest.last_name])

        group = Group(None, description, guest.id)
        group.id = self.core.register_group(group)

        sys.stderr.write("{}\n".format(guest))

        self.core.add_guest_to_group(guest, group)
        self.interface.display_message(resources.strings.GROUP_CREATED)
        self.interface.display_groups([group])

    def _list_groups(self):
        """ list all the groups """
        groups = self.database.list_groups()
        self.interface.display_groups(groups)

        self.interface.display_message(resources.strings.ENTER_GROUP_ID)
        group_id = self.interface.prompt_int()

        group = groups[group_id - 1]
        guests = self.database.get_guests(group)

        self.interface.display_guests(guests)

    def _list_weekly_services(self):
        """ submenu to list service periods """
       
        enter_date= self.interface.prompt_date()
        lower_limit = datetime_to_unix(enter_date)
        upper_limit = lower_limit+ 7*24*60*60

        criteria = TimeSpanCriteria(lower_limit, upper_limit)
        service_id = self._get_service_input()
        appointments= self.database.get_all_appointments(criteria)
        appointments= [appointment for appointment in appointments if appointment.service_id == service_id]

        self.interface.display_appointments(appointments)

    def _create_account(self):
        """ create a new account """
        username = self.interface.prompt_text(resources.ENTER_NEW_USERNAME)
        password = self.interface.prompt_text(resources.ENTER_NEW_PASSWORD, True)
        password_2 = self.interface.prompt_text(resources.ENTER_NEW_PASSWORD_AGAIN, True)

        if password != password_2:
            raise RuntimeError(resources.strings.PASSWORD_DO_NOT_MATCH)

        admin_rights = self.interface.prompt_bool(resources.strings.ENTER_ADMIN_RIGHTS)

        self.core.register_credentials(username, password, admin_rights)





