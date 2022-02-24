from utils.writer import writer


class state_var_decleration():
    def __init__(self, var_name, var_type):
        self.var_name = var_name
        self.var_type = var_type

    def write(self):
        writer.write('{} {};'.format(self.var_type, self.var_name), 2)
