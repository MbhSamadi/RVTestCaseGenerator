import random
from utils.name_gen import name_gen


class rebec_program_gen():
    def __init__(self, configuration):
        self.configuration = configuration
        self.some_rebecs_have_max_msgservers = False
        self.rebecas = [r for r in range(self.configuration.rebec_count)]
        self.rebec_msgservers = {r: [] for r in self.rebecas}

    def generate(self):
        min_connections_required = self.create_minimum_graph_required()
        self.complete_connections(min_connections_required)

        for r in self.rebecas:
            self.complete_rebec_msgservers(r, r)

        return self.rebec_msgservers

    def create_minimum_graph_required(self):
        min_connections_required = {r: [] for r in self.rebecas}

        rebec = random.choice(self.rebecas)
        for i in range(self.configuration.max_msgservers_seq + 1):
            self.add_msgserver(rebec)
            next_rebec = self.choose_random_rebec_except_one(rebec)
            # print(rebec, next_rebec)
            min_connections_required[rebec] = list(
                set(min_connections_required[rebec] + [next_rebec]))

            rebec = next_rebec

        # print(min_connections_required)
        return min_connections_required

    def complete_connections(self, min_connections_required):
        connections = min_connections_required
        for r in self.rebecas:
            connect_to_rebecs = list(
                set(self.rebecas) - set(connections[r]))
            if r in connect_to_rebecs:
                connect_to_rebecs.remove(r)
            # print('222', self.rebecas, r, connect_to_rebecs)
            if (len(connect_to_rebecs) == 0):
                continue

            random_rebec_count = random.randint(1, len(connect_to_rebecs))
            new_connected_rebecs = random.sample(
                connect_to_rebecs, random_rebec_count)

            connections[r] = list(
                set(connections[r] + new_connected_rebecs))

        # print('333', connections)
        self.configuration.set_connections(connections)

    def choose_random_rebec_except_one(self, rebec_except):
        return random.choice([r for r in self.rebecas if not r == rebec_except])

    def add_msgserver(self, rebec, count=1):
        self.rebec_msgservers[rebec] += [
            name_gen.get_rebeca_msgserver(rebec) for _ in range(count)]

    def complete_rebec_msgservers(self, rebec, index):
        msgserver_count = len(self.rebec_msgservers[rebec])
        if (msgserver_count >= self.configuration.max_msgservers_count):
            return

        msgserver_count = random.randint(
            msgserver_count, self.configuration.max_msgservers_count)

        if msgserver_count == self.configuration.max_msgservers_count:
            self.some_rebecs_have_max_msgservers = True
        elif (not self.some_rebecs_have_max_msgservers) and index == len(self.rebec_msgservers) - 1:
            msgserver_count = self.configuration.max_msgservers_count

        msgserver_count -= len(self.rebec_msgservers[rebec])

        self.add_msgserver(rebec, msgserver_count)
