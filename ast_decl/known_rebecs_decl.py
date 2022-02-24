from utils.writer import writer


class known_rebeca_decleration:
    def __repr__(self):
        return 'KnownRebeca<{}>'.format(repr({'rebeca': self.rebeca, 'name': self.name}))

    def __init__(self, rebeca, name):
        self.rebeca = rebeca
        self.name = name

    def write(self):
        writer.write('{} {};'.format(self.rebeca, self.name), 2)
