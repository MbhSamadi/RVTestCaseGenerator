from utils.writer import writer
from ast_decl.assignment_decl import assignment_decleration
from utils.utils import random_value_of_type
from ast_decl.send_msg_decl import send_message_decleration
from utils.name_gen import name_gen
import random


class constructor_decl():
    def __init__(self, rebeca, state_vars):
        self.rebeca = rebeca
        self.state_vars = state_vars
        self.body = [assignment_decleration(
            sv.var_name, random_value_of_type(sv.var_type)) for sv in self.state_vars]

    def random_body_statement(self):
        r = random.random()
        if r > 0.7:
            self.body.append(self.generate_random_assignment())

    def generate_random_assignment(self):
        sv = random.choice(self.state_vars)
        return assignment_decleration(
            sv.var_name, random_value_of_type(sv.var_type))

    def add_call_msgserver_in_constructor(self, msgserver_decl):
        self.random_body_statement()
        self.body.append(send_message_decleration(
            self.rebeca, name_gen.get_known_rebeca_name_of_rebeca(self.rebeca), msgserver_decl.msgserver_name))
        self.random_body_statement()

    def write(self):
        writer.write('{}() {{'.format(self.rebeca), 1)
        self.write_body()
        writer.write('}', 1)

    def write_body(self):
        for sentence in self.body:
            sentence.write()
