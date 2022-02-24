# from PyInquirer import prompt
from rebec_program.rebec_program_conf import rebec_program_conf
import random


class input_getter_class():
    def __init__(self):
        self.connections = {}
        self.rebecs = []
        self.minimum_max_msgservers_count = 0

    def __repr__(self):
        return "self.rebec_count: {}, self.max_msgservers_count: {}, self.max_msgservers_seq: {}".format(
            self.rebec_count, self.max_msgservers_count,
            self.max_msgservers_seq)

    def get_configuration(self):
        self.minimum_max_msgservers_count = 0
        self.get_rebecs_count()
        self.get_max_msgservers_seq()
        self.get_max_msgservers_count()
        # self.get_rebecs_graph()
        self.get_property_length()
        self.get_non_casuality_count()
        self.get_causality_count()
        self.get_backwards_count()

        print()
        print('###############-----------------------###############')
        print()

        return rebec_program_conf(self.rebec_count, self.max_msgservers_count,
                                  self.max_msgservers_seq,
                                  self.property_length,
                                  self.non_causality_count,
                                  self.causality_count, self.backwards_count)

    def get_rebecs_count(self):
        self.rebec_count = int(input('Number of Rebecas: '))
        if self.rebec_count <= 0:
            print('should be more than 0')
            self.get_rebecs_count()

    def get_max_msgservers_count(self):
        self.max_msgservers_count = int(
            input('Maximum number of message servers: (Minimum: {}) '.format(
                self.minimum_max_msgservers_count)))
        if self.max_msgservers_count < self.minimum_max_msgservers_count:
            print('should be more than {}'.format(
                self.minimum_max_msgservers_count))
            self.get_max_msgservers_count()

    def get_max_msgservers_seq(self):
        self.max_msgservers_seq = int(
            input('Maximum message server call sequence: '))
        if self.max_msgservers_seq < 0 or self.max_msgservers_seq > 100:
            print('should be 0>= and <= 100')
            self.get_max_msgservers_seq()
        else:
            self.minimum_max_msgservers_count = (self.max_msgservers_seq + 1 +
                                                 self.rebec_count -
                                                 1) // self.rebec_count

    # def get_rebecs_graph(self):
    #     self.rebecs = [i for i in range(0, self.rebec_count)]
    #     self.connections = {i: [] for i in range(0, self.rebec_count)}

    #     for rebec in self.rebecs:
    #         self.get_connections_of_rebec(rebec)

    #     if self.no_rebecs_are_connected() and self.rebec_count >= 2:
    #         self.connections[self.rebecs[0]] = [self.rebecs[1]]

    # def no_rebecs_are_connected(self):
    #     for r in self.rebecs:
    #         if len(self.connections[r]) > 0:
    #             return False
    #     return True

    # def get_connections_of_rebec(self, rebec):
    #     # self.get_connections_of_rebec_input(rebec)
    #     self.get_connections_of_rebec_random(rebec)

    # def get_connections_of_rebec_random(self, rebec):
    #     random_rebec_count = random.randint(1, self.rebec_count)
    #     connected_rebecs = random.sample(self.rebecs, random_rebec_count)
    #     if rebec in connected_rebecs:
    #         connected_rebecs.remove(rebec)
    #     self.connections[rebec] = connected_rebecs

    # def get_connections_of_rebec_input(self, rebec):
    #     questions = [
    #         {
    #             'type': 'checkbox',
    #             'qmark': '<->',
    #             'message': 'Which rebecs are connected to rebec_{}'.format(rebec),
    #             'name': 'connections',
    #             'choices': [{'name': 'rebec_{}'.format(r), 'value': r} for r in range(self.rebec_count) if r != rebec],
    #         }
    #     ]

    #     answers = prompt(questions)
    #     self.connections[rebec] = answers['connections']

    def get_property_length(self):
        self.property_length = int(input('Property length: '))
        if self.property_length < 2 or self.property_length > self.max_msgservers_seq:
            print('should be 2>= and <= {}'.format(self.max_msgservers_seq))
            self.get_property_length()

    def get_non_casuality_count(self):
        self.non_causality_count = int(
            input(
                'Number of relations without causality in the property set: '))
        if self.non_causality_count < 0:
            print('should be 0>=')
            self.get_non_casuality_count()

    def get_causality_count(self):
        self.causality_count = int(
            input('Number of relations with causality in the property set: '))
        if self.causality_count < 0:
            print('should be 0>= and <= {}'.format(self.property_length))
            self.get_causality_count()

    def get_backwards_count(self):
        self.backwards_count = int(input('Number of backwards: '))
        if self.backwards_count < 0:
            print('should be 0>=')
            self.get_backwards_count()


input_getter = input_getter_class()
