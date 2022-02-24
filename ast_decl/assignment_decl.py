from utils.writer import writer


class assignment_decleration():
    def __repr__(self):
        return 'assignment: {} = {}'.format(self.assign_to_var, self.value)

    def __init__(self, assign_to_var, value):
        self.assign_to_var = assign_to_var
        self.value = value

    def write(self):
        writer.write('{} = {};'.format(self.assign_to_var, self.value), 2)
