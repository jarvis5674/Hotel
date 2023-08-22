class Group:
    """ represents a guest group at the spa"""

    def __init__(self, *args):
        self.id = args[0]
        self.description = args[1]
        self.owner_id = args[2]

    def __str__(self):
        return """(%s,'%s', %s)""" % (
            self.id if self.id is not None else 'NULL',
            self.description.replace('\'', '\'\''),
            self.owner_id or 'NULL'
        )