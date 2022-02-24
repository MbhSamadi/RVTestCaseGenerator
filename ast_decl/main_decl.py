from utils.writer import writer


class main_decleration():
    def __init__(self, class_decleration):
        self.class_decleration = class_decleration
        self.rebeca_instances = [{
            'rebeca':
            cd.rebeca_name,
            'known_rebeca':
            ['instance{}'.format(kr.rebeca) for kr in cd.known_rebecas]
        } for cd in class_decleration]

    def write(self):
        writer.write('main {')
        self.write_rebeca_instances()
        writer.write('}')

    def write_rebeca_instances(self):
        for r in self.rebeca_instances:
            writer.write(
                '{} instance{}({}):();'.format(r['rebeca'], r['rebeca'],
                                               ', '.join(r['known_rebeca'])),
                1)
