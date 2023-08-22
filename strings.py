### THIS FILE CONTAINS ALL THE PRINTED STRINGS TO THE SOFTWARE
### PLEASE KEEP THE VARIABLE NAMES IN ALPHABETICAL ORDER

APPOINTMENT_CANCELLED = "Appointment cancelled"
APPOINTMENT_DATA = "All appointment data"
APPOINTMENT_MENU = ["{}. {}".format(index + 1, value) for index, value in enumerate([
    "Register Appointment",
    "Cancel Appointment",
    "List Availability"
    ])
] + ["E. EXIT"]
APPOINTMENT_NOT_AVAILABLE = "This reservation is not available, please pick another time slot"
APPOINTMENT_TABLE_HEADER = ["ID", "RESERVED AT", "CREATED AT", "SERVICE", "DURATION", "PRICE", "STATUS"]
APPOINTMENT_VOIDED = "Appointment voided"
CHARGE_NOT_CLEARED = "The appointment will still be charged."
CONTINUE = "Continue? (Y/N)"
CREDENTIAL_TABLE_HEADER = [
    "USERNAME",
    "HAS ADMIN RIGHTS",
]
DATABASE_MENU = ["{}. {}".format(index + 1, value) for index, value in enumerate([
    "List Services",
    "List Appointments",
    "List Guests",
    "List Groups",
    "List Credentials",
    "Create new Account",
    "Reset Database",
    ])
] + ["E. EXIT"]
DURATION_OF_STAY = "During of stay"
ENTER_APPOINTMENT_ID = "Please enter appointment id"
ENTER_GROUP_ID = "Please enter group id"
ENTER_GUEST_INFORMATION = "Please enter guest name, e.g 'Robin Byrd'"
ENTER_GUEST_ID = "Please enter guest id"
ENTER_DATE = "Please enter date (YYYY-MM-DD)"
ENTER_PASSWORD_PROMPT = "Now enter your password: "
ENTER_NEW_USERNAME = "Type in new Username"
ENTER_NEW_PASSWORD = "Type in new Password"
ENTER_NEW_PASSWORD_AGAIN = "Type in new Password again"
ENTER_ADMIN_RIGHTS = "Does new account have admin rights? Y/N"
ENTER_TIME = "Please enter time (HH-MM)"
ENTER_SERVICE = "Please enter service"
ENTER_SERVICE_TIME = "Please enter desired service time"
ENTER_SERVICE_TYPE = "Please enter service type"
ENTER_USERNAME = "Welcome to MiYE! Please type in your Username: "
EXIT = "Good bye!"
FLAVOR_TEXT = "'Give a man a program, frustrate him for a day. Teach a man to program, frustrate him for a lifetime.'"
FLAVOR_TEXTS = [
    "Make software, not war",
    "If it ain't broken, add more features",
    "Embrace mistakes for what they are - value life lessons. Unless it's a fatal mistake",
    "Give a man a program, frustrate him for a day. Teach a man to program, frustrate him for a lifetime",
    "Buffalo buffalo Buffalo buffalo buffalo buffalo Buffalo buffalo",
    "It’s not a bug – it’s an undocumented feature",
    "Why do pythons live on land? It's above C-level",
    "import antigravity",
    "Errors should never pass silently. Unless explicitly silenced.",
    "128.0.0.1 Sweet 128.0.0.1",
    "Wingardium Leviosa is the Hello World of the wizarding world",
    "I entered ten puns into a pun contest hoping one would win -- but no pun in ten did.",
    "What do you call a fake noodle? An Im-Pasta",
    "BOGO Sort: shuffle until sorted",
    "Never BYTE off more than you can QUEUE",
    "A journalist asks a programmer what makes code bad? No comment",
    "// the following code works. don't touch it",
    "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.",
    "This flavor text no longer exists. Press OK to continue",
    "Sometimes the road less traveled is less traveled for a reason.",
]
GROUP = "Group"
GROUP_MENU = ["{}. {}".format(index + 1, value) for index, value in enumerate([
    "Create Group",
    "Add Guest to Group",
    "List Guests in Group",
    ])
] + ["E. EXIT"]
GROUP_CREATED = "Group created"
GROUP_TABLE_HEADER = [ "ID", "DESCRIPTION", "OWNER ID"]
GUEST_HAS_OVERLAPPING_APPOINTMENT = "Guest has overlapping appointment"
GUEST_NOT_STAYING = "Guest is not staying at the spa during the date entered."
GUEST_TABLE_HEADER = ["ID", "FIRST NAME", "LAST NAME", "VACATION START", "VACATION END", "GROUP"]
HELLO_WORLD = "HELLO WORLD!"
INVALID_SELECTION = "Invalid selection. Please try again."
INVALID_GROUP_ID = "Invalid group id"
LOGIN_ADMIN = "You are logged in as an admin"
LOGIN_CLERK = "You are logged in as a clerk"
LOGIN_PROMPT = "Congrats, you're now logged in as"
INVOICE = "Invoice"
MENU = ["{}. {}".format(index + 1, value) for index, value in enumerate([
    "Register guest",
    "Manage Appointments",
    "Manage Groups",
    "Print Invoice",
    "Weekly Summary",
    "Manage Database",
    ])
] + ["E. EXIT"]
MENU_CLERK = ["{}. {}".format(index + 1, value) for index, value in enumerate([
    "List Services",
    "Print Invoice",
    "Manage Appointments"
    ])
] + ["E. EXIT"]
MINUTES = "Minutes"
NO_APPOINTMENTS = "No appointments"
OUTSIDE_SERVICE_HOURS = "The time specified is outside of regular service hours"
PASSWORD_DO_NOT_MATCH = "Passwords do not match"
SERVICE_TABLE_HEADER = ["SERVICE", "DURATION (MINUTES)", "COST"]
SERVICE_OVERLAP = "This service is already booked"
TOTAL_CHARGED = "Total Amount Charged"
UNKNOWN_ERROR = "Unknown error."
UNKNOWN_SELECTION = "Unknown selection. Please try again."
WELCOME_TO_MIYE = "############################################################################################################\n" \
                  "##  Welcome to MiYE (Mud in Your Eye). MiYE is a spa appointment scheduling system.                       ##\n" \
                  "##                                                                                        ver 2.0         ##\n"\
                  "############################################################################################################"
WRONG_LOGIN = "Sorry wrong password or username, try again"
