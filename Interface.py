import os
import sys
import datetime
import getpass
import random
from . import resources
from .Constants import *
from .SpaDatabase import SpaDatabase

from prettytable import PrettyTable


class Interface:
    """ Interact with the user """
    _DATABASE = SpaDatabase(DATABASE_PATH)

    def __init__(self):
        sys.stderr.write("initializing interface\n")
        pass

    @classmethod
    def prompt_continue(cls, msg=None):
        print(msg if msg else "", resources.strings.CONTINUE)
        return True if input().upper().startswith("Y") else False

    @classmethod
    def prompt_bool(cls, msg=None):
        print()
        print(msg if msg else "")
        return True if input().upper().startswith("Y") else False

    @classmethod
    def prompt_date(cls):
        print()
        print(resources.strings.ENTER_DATE)
        date = tuple([int(x) for x in input().split('-')])
        sys.stderr.write("date entered {}\n".format(date))
        date = datetime.datetime(*date)
        return date

    @classmethod
    def prompt_text(cls, message=None, secret=False):
        print()
        if message:
            print(message)
        return input() if not secret else getpass.getpass()

    @classmethod
    def prompt_guest_id(cls):
        print(resources.strings.ENTER_GUEST_ID)
        return int(input())

    @classmethod
    def prompt_guest_name(cls):
        print(resources.strings.ENTER_GUEST_INFORMATION)
        guest = input()
        guest_info = guest.split(' ')
        if len(guest_info) < 2:
            raise RuntimeError

        return guest_info[:2]

    @classmethod
    def prompt_int(cls, message=None):
        if message:
            print(message)
        return int(input())

    @classmethod
    def prompt_time(cls):
        print()
        print(resources.strings.ENTER_TIME)
        time_entered = tuple([int(x) for x in input().split('-')])
        sys.stderr.write("time entered {}\n".format(time_entered))
        return datetime.time(time_entered[0], time_entered[1])

    @classmethod
    def clear_screen(cls, admin_rights=None):
        if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
            # For Linux/OS X
            os.system('clear')
        elif sys.platform == "win32":
            # For Windows
            os.system('cls')

        random_text = random.randint(0, len(resources.strings.FLAVOR_TEXTS) - 1)
        print(resources.strings.WELCOME_TO_MIYE)
        print(resources.strings.FLAVOR_TEXTS[random_text])

        cls.display_user(admin_rights)

    @classmethod
    def prompt_selection(cls, choices):
        for index, i in enumerate(choices):
            print("{0} - {1}".format(str(index + 1), i[0]))

        selection = int(input())
        return selection, choices[selection - 1]

    @classmethod
    def display_message(cls, *message):
        print()
        print(*message)

    @classmethod
    def display_user(cls, admin_rights):
        if admin_rights is not None:
            print()
            if admin_rights:
                print(resources.strings.LOGIN_ADMIN)
            else:
                print(resources.strings.LOGIN_CLERK)
        print()

    @classmethod
    def display_appointments(cls, appointments):
        appointments_table = PrettyTable(resources.strings.APPOINTMENT_TABLE_HEADER)
        for appointment in appointments:
            price = cls._DATABASE.get_service_price(appointment.service_id) * appointment.service_time \
                if appointment.status != "VOIDED" \
                else 0
            service_name = cls._DATABASE.get_service_name(appointment.service_id, appointment.service_type)[0].replace(
                "\"", "")
            appointments_table.add_row([
                appointment.id,
                str(appointment.date_time),
                str(appointment.created_at),
                service_name,
                appointment.service_time,
                price,
                appointment.status
            ])

        appointments_table.sortby = resources.strings.APPOINTMENT_TABLE_HEADER[1]
        print(appointments_table)

    @classmethod
    def display_services(cls, services):
        service_table = PrettyTable(resources.strings.SERVICE_TABLE_HEADER)
        for service in services:
            service_table.add_row([
                " ".join([service.type_name, service.id_name]),
                service.duration,
                service.price * service.duration
            ])

        print(service_table)

    @classmethod
    def display_guests(cls, guests):
        guest_table = PrettyTable(resources.strings.GUEST_TABLE_HEADER)
        for guest in guests:
            guest_table.add_row([
                guest.id,
                guest.first_name,
                guest.last_name,
                str(guest.vacation_start.date()),
                str(guest.vacation_end.date()),
                guest.group_id
            ])

        guest_table.sortby = resources.strings.GUEST_TABLE_HEADER[2]
        print(guest_table)

    @classmethod
    def display_groups(cls, groups):
        group_table = PrettyTable(resources.strings.GROUP_TABLE_HEADER)
        for group in groups:
            group_table.add_row([
                group.id,
                group.description,
                group.owner_id
            ])

        print(group_table)

    @classmethod
    def display_credentials(cls, credentials):
        credential_table = PrettyTable(resources.strings.CREDENTIAL_TABLE_HEADER)
        for credential in credentials:
            credential_table.add_row([
                credential[0],
                credential[1]
            ])

        print(credential_table)