from utils.writer import writer


class condition_decleration():
    def __repr__(self):
        return 'condition: if({})'.format(self.c_var)

    def __init__(self, c_var):
        self.c_var = c_var

    def write(self):
        writer.write('if ({})'.format(self.c_var), 2)
