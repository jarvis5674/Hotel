class Service:
    """ represents a service at the spa"""
    def __init__(self, *args):
        self.type = args[0]
        self.id = args[1]
        self.type_name = args[2]
        self.id_name = args[3]
        self.price = args[4]
        self.duration = args[5]

    def __str__(self):
        return """({})""".format(",".join([self.type, self.id, self.type_name, self.id_name, self.price, self.duration]))