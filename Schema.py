import sys


class Schema:
    def __init__(self, name, fields):
        sys.stderr.write("initializing new schema\n")
        sys.stderr.write("name: %s\n" % (name,))
        sys.stderr.write("fields: %s\n" % (fields,))
        self.name = name
        self.fields = fields

    def __str__(self):
        return "(%s)" % (
            ",".join(["%s %s" % (x[0], x[1]) for x in self.fields])
        )

    def editable_fields(self):
        return "(%s)" % (
            ",".join(["%s" % (x[0],) for x in self.fields if "AUTOINCREMENT" not in x[1]])
        )
