from utils.graph import graph
from utils.utils import flatten_list
from utils.name_gen import name_gen
import random
import copy

probablitiy_of_adding_additional_msg_calls = 0.75


class msgserver_call_graph_gen():
    def __init__(self, configuration, rebeca_msgservers):
        self.configuration = configuration
        self.rebeca_msgservers = rebeca_msgservers
        self.rebecs_graph = graph(configuration.connections)

        # print(self.rebecs_graph, self.rebeca_msgservers)
        # print()

        self.all_rebeca_pairs_cache = []
        self.reinit()

    def reinit(self):
        self.msgservers_graph = graph(
            {m: [] for m in flatten_list(list(self.rebeca_msgservers.values()))})

    def generate_graph(self):
        while self.msgservers_graph.max_path_length() < self.configuration.max_msgservers_seq:
            self.reinit()
            self.generate_all_rebeca_pairs()
            should_add_msgserver_call = self.msgservers_graph.max_path_length(
            ) < self.configuration.max_msgservers_seq
            # print(self.all_rebeca_pairs, should_add_msgserver_call)
            while should_add_msgserver_call and len(self.all_rebeca_pairs) > 0:
                self.add_msgserver_call()
                # print(self.msgservers_graph.max_path_length())
                # (not self.msgservers_graph.max_path_length() == -1) and
                should_add_msgserver_call = True if self.msgservers_graph.max_path_length() <= self.configuration.max_msgservers_seq else random.random(
                ) > probablitiy_of_adding_additional_msg_calls

            # print('--++++--', self.msgservers_graph)
            # print()
        new_rebecs_graph = dict()
        for i in self.rebecs_graph.get_nodes():
            new_rebecs_graph[name_gen.get_rebeca_name(i)] = [name_gen.get_rebeca_name(
                j) for j in self.rebecs_graph.edges(i)]
        self.remove_extra_calls(self.configuration.maximum_method_calls)
        return (self.msgservers_graph, graph(new_rebecs_graph))

    def remove_extra_calls(self,max_call_count):
        search_graph = copy.deepcopy(self.msgservers_graph)
        gates = search_graph.nodes_with_in_degree(0)
        search_graph.add_node("gc") # global constructor
        remove_list = []
        for gate in gates:
            search_graph.connect("gc",gate)
        # print(search_graph)
        call_count_dict = {"gc" : 1}
        max_path_length = {"gc" : 0}
        queue = search_graph.topological_sort()[1:]
        while len(queue) != 0:
            q = queue.pop(0)
            for node in search_graph.nodes_that_connect_to(q):
                call_count_dict[q] = call_count_dict.get(q,0) + call_count_dict[node]
                max_path_length[q] = max(max_path_length.get(q, 0), max_path_length[node] + 1)
            if call_count_dict[q] > max_call_count:
                descending_path_length_neighbors = [(n, call_count_dict[n], max_path_length[n]) for n in search_graph.nodes_that_connect_to(q)]
                descending_path_length_neighbors.sort(key=lambda x : (x[2], x[1]), reverse=False)
                for node, count, _ in descending_path_length_neighbors:
                    if call_count_dict[q] > max_call_count:
                        call_count_dict[q] -= count
                        remove_list.append((node,q))
                    else:
                        break
            if call_count_dict[q] == 0:
                max_path_length[q] = 0
        for i,j in remove_list:
            self.msgservers_graph.remove_edge(i,j)
        # print("here ========> "+str(remove_list))
        # print("here ========> "+str(call_count_dict))
        
    def add_msgserver_call(self):
        start_rebec_msgserver, end_rebec_msgserver = self.choose_random_rebeca_msgservers()

        self.msgservers_graph.connect(
            start_rebec_msgserver, end_rebec_msgserver)

        max_path_length = self.msgservers_graph.max_path_length()
        # print(self.msgservers_graph, max_path_length, start_rebec_msgserver, end_rebec_msgserver)
        if (max_path_length == -1) or (max_path_length > self.configuration.max_msgservers_seq):
            self.msgservers_graph.remove_edge(
                start_rebec_msgserver, end_rebec_msgserver)

    def choose_random_rebeca_msgservers(self):
        pair = random.choice(self.all_rebeca_pairs)
        # print('--------', pair)
        self.all_rebeca_pairs.remove(pair)
        return pair

    def generate_all_rebeca_pairs(self):
        if (len(self.all_rebeca_pairs_cache) > 0):
            self.all_rebeca_pairs = self.all_rebeca_pairs_cache[:]
            # print('--------', self.all_rebeca_pairs)
            return
        self.all_rebeca_pairs = []
        # print(self.rebeca_msgservers, self.rebecs_graph)
        for r1 in self.rebeca_msgservers:
            for m1 in self.rebeca_msgservers[r1]:
                for r2 in self.rebecs_graph.edges(r1):
                    for m2 in self.rebeca_msgservers[r2]:
                        self.all_rebeca_pairs.append((m1, m2))
        self.all_rebeca_pairs_cache = self.all_rebeca_pairs[:]
        # print('---------------------------', self.all_rebeca_pairs)
