from utils.writer import writer
from utils.name_gen import name_gen
from ast_decl.known_rebecs_decl import known_rebeca_decleration
from ast_decl.constructor_decl import constructor_decl


class class_decleration:
    def __repr__(self):
        return '\nclass_decleration< \n\
                    rebeca_name: {} \n\
                    known_rebecas: {} \n\
                    state_vars: {} \n\
                    msgservers: {} \n>\n'.format(self.rebeca_name, repr(self.known_rebecas), repr(self.state_vars), repr(self.msgservers))

    def __init__(self, rebeca_name, buffer_size, known_rebecas, state_vars):
        self.rebeca_name = rebeca_name
        self.buffer_size = buffer_size
        self.state_vars = state_vars
        self.known_rebecas = [known_rebeca_decleration(kr, name_gen.get_known_rebeca_name_of_rebeca(
            kr)) for kr in known_rebecas]
        self.msgservers = []
        self.constructor = constructor_decl(rebeca_name, self.state_vars)

    def add_msgserver(self, msgserver_decl):
        self.msgservers.append(msgserver_decl)

    def add_call_msgserver_in_constructor(self, msgserver_decl):
        self.constructor.add_call_msgserver_in_constructor(msgserver_decl)

    def write(self):
        writer.write('reactiveclass {}({}) {{'.format(
            self.rebeca_name, self.buffer_size))
        self.write_known_rebecas()
        self.write_state_vars()
        self.write_constructor()
        self.write_msgservers()
        writer.write('}')
        writer.write('')

    def write_state_vars(self):
        writer.write('statevars {{'.format(), 1)
        for sv in self.state_vars:
            sv.write()
        writer.write('}', 1)

    def write_known_rebecas(self):
        writer.write('knownrebecs {{'.format(), 1)
        for kr in self.known_rebecas:
            kr.write()
        writer.write('}', 1)

    def write_constructor(self):
        self.constructor.write()

    def write_msgservers(self):
        for msgs in self.msgservers:
            msgs.write()
