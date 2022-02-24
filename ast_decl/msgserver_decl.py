from utils.utils import random_value_of_type
from utils.writer import writer
from ast_decl.send_msg_decl import send_message_decleration
from ast_decl.assignment_decl import assignment_decleration
from ast_decl.condition_decl import condition_decleration
from utils.name_gen import name_gen
import random

MAX_BODY_COUNT = 5

class msgserver_decleration:
    def __repr__(self):
        return '\nmsgserver_decleration<name: {} msgervers_to_call: {}>'.format(self.msgserver_name, repr(self.msgervers_to_call))

    def __init__(self, source_rebeca, msgserver_name, msgservers_to_call, state_vars):
        self.source_rebeca = source_rebeca
        self.msgserver_name = msgserver_name
        self.state_vars = state_vars
        self.msgervers_to_call = [send_message_decleration(self.source_rebeca, name_gen.get_known_rebeca_name_of_rebeca(
            name_gen.get_rebeca_name_of_msgserver(msgs)), msgs) for msgs in msgservers_to_call]
        self.body = []
        self.generate_body()

    def generate_body(self):
        self.random_body_statement(True)
        for msgscall in self.msgervers_to_call:
            self.random_body_statement()
            if random.random() > 0.6:
                self.random_condition_statement()
            self.body.append(msgscall)
            self.random_body_statement()

    def random_condition_statement(self):
        if len(self.body) > MAX_BODY_COUNT:
            return
        boolean_vars = [s for s in self.state_vars if s.var_type == 'boolean']
        if len(boolean_vars) == 0:
            return False
        state_var = random.choice(boolean_vars)
        self.body.append(condition_decleration(state_var.var_name))

    def random_body_statement(self, force=False):
        if len(self.body) > MAX_BODY_COUNT:
            return
        r = random.random()
        if force or r > 0.7:
            if r > 0.85:
                self.random_condition_statement()
            self.body.append(self.generate_random_assignment())

    def generate_random_assignment(self):
        sv = random.choice(self.state_vars)
        return assignment_decleration(
            sv.var_name, random_value_of_type(sv.var_type))

    def write(self):
        writer.write('msgsrv {}() {{'.format(self.msgserver_name), 1)
        self.write_msgserver_body()
        writer.write('}', 1)

    def write_msgserver_body(self):
        for sentence in self.body:
            sentence.write()
