from utils.utils import tuple_to_string
import csv
import os


class table_gen():
    def __init__(self, rebecas_graph, dfa_graph, folder):
        self.folder = folder
        self.rebecas = rebecas_graph.get_nodes()
        self.dfa_graph = dfa_graph
        self.states = dfa_graph.states
        self.transitions = dfa_graph.transitions
        self.input_symbols = dfa_graph.input_symbols
        self.final_states = dfa_graph.final_states
        self.initial_state = dfa_graph.initial_state
        # self.table = []
        # print('vio_paths', vio_paths)
        # print()

    def export_table(self):
        for r in self.rebecas:
            self.export_table_rebec(r)

    def export_table_rebec(self, rebec):
        table = self.get_table(rebec)
        csv_columns = ['pre', 'transition', 'vio', 'final']
        dict_data = table
        csv_file = "{}/table-{}.csv".format(self.folder, rebec)
        try:
            with open(csv_file, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in dict_data:
                    # print(data)
                    writer.writerow(data)
                csvfile.seek(-2, os.SEEK_END) # <---- 2 : len('\r\n')
                csvfile.truncate()
        except IOError:
            print("I/O error")

    def get_table(self, rebec):
        all_transitions = self.dfa_graph.get_rebec_transitions(rebec)
        table = []
        # print(all_transitions)
        for t in all_transitions:
            pre = self.dfa_graph.get_pre_transitions(t)
            if len(pre) == 0:
                table.append({
                    'pre':
                    "",
                    'transition':
                    tuple_to_string(rename_rebec_to_instance_t(t)),
                    'vio': [],
                    'final':
                    self.dfa_graph.is_final_path(t)
                })
            for p in pre:
                table.append({
                    'pre':
                    tuple_to_string(rename_rebec_to_instance_t(p)),
                    'transition':
                    tuple_to_string(rename_rebec_to_instance_t(t)),
                    'vio': [] if self.dfa_graph.is_backward(t) else [
                        rename_rebec_to_instance_in_vio(u)
                        for u in self.dfa_graph.get_vio_transition(p)
                    ],
                    'final':
                    self.dfa_graph.is_final_path(t)
                })

        # self.iterate_state(self.initial_state, [])
        return table


def rename_rebec_to_instance_t(transition):
    qs, msg, qe = transition
    return (qs, rename_rebec_to_instance_msg(msg), qe)


def rename_rebec_to_instance_msg(msg):
    first_dash_index = msg.index('-')
    first_rebec = msg[0:first_dash_index]
    sec_dash_index = msg.index('-', first_dash_index + 1)
    second_rebec = msg[sec_dash_index + 1:]
    method = msg[first_dash_index + 1:sec_dash_index]

    return 'instance{}-{}-instance{}'.format(first_rebec, method, second_rebec)


def rename_rebec_to_instance_in_vio(vio):
    first_dash_index = vio.index(',')
    sec_dash_index = vio.index(',', first_dash_index + 1)

    return vio[0:first_dash_index + 1] + rename_rebec_to_instance_msg(
        vio[first_dash_index + 1:sec_dash_index]) + vio[sec_dash_index:]
