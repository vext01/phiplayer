class Broadcast(object):

    def __init__(self, pid, title, descr, categs):
        self.pid = pid
        self.title = title
        self.descr = descr
        self.categs = categs

    @staticmethod
    def from_line(line):
        colon = line.index(":")

        pid = line[:colon].strip()
        line = line[colon + 1:]

        hyph = line.index("-")
        title = line[:hyph].strip()
        line = line[hyph + 1:]

        comma = line.index(",")
        descr = line[:comma].strip()
        line = line[comma + 1:]

        categs = [ x.strip() for x in line.split(",") ]

        return Broadcast(pid, title, descr, categs)

    def __str__(self):
        cats = ", ".join(self.categs)
        return "%s:%s - %s, %s" % (self.pid, self.title, self.descr, cats)
