class GroupCriteria:
    def __init__(self, group_id):
        self.group_id = group_id


class TimeSpanCriteria:
    def __init__(self, min_date, max_date):
        self.min = min_date
        self.max = max_date


class GuestCriteria:
    def __init__(self, guest_id):
        self.guest_id = guest_id