from utils.graph import graph
from utils.name_gen import name_gen
import random


class rebeca_ast_gen():
    def __init__(self, rebecas_graph, msgservers_graph):
        self.rebecas_graph = rebecas_graph
        self.msgservers_graph = msgservers_graph
        self.rebeca_insts = {r: [] for r in self.rebecas_graph.get_nodes()}
        # print(self.rebecas_graph)
        # print(self.msgservers_graph)
        # print(self.rebeca_insts)

    def generate_ast(self):
        self.generate_one_instance(0)
        self.set_known_rebecas()
        # print(self.rebeca_insts)
        return self.rebeca_insts

    def generate_one_instance(self, instance_count):
        rebecas = list(self.rebecas_graph.get_nodes())
        for r in rebecas:
            self.rebeca_insts[r].append({
                'rebec': r,
                'inst_name': name_gen.get_instance_name(r, instance_count),
                'known_rebecs': []
            })

    def set_known_rebecas(self):
        for rebec in list(self.rebeca_insts.keys()):
            self.set_known_rebecas_of_rebeca(rebec)

    def set_known_rebecas_of_rebeca(self, rebec):
        for inst in self.rebeca_insts[rebec]:
            connected_rebecas = self.rebecas_graph.edges(inst['rebec'])
            for c_rebec in connected_rebecas:
                inst['known_rebecs'].append(
                    self.get_instance_of_rebeca(c_rebec))

    def get_instance_of_rebeca(self, rebec):
        random_instance = random.choice(self.rebeca_insts[rebec])
        return random_instance['inst_name']
