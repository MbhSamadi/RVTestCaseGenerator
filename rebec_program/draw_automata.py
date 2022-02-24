import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab


class draw_automata():
    def __init__(self, dfa_obj, folder):
        self.dfa_obj = dfa_obj
        self.states = dfa_obj['states']
        self.transitions = dfa_obj['transitions']
        self.input_symbols = dfa_obj['input_symbols']
        self.final_states = dfa_obj['final_states']
        self.initial_state = dfa_obj['initial_state']
        self.folder = folder

        print()
        print()

        self.edges = self.enrich_edges()
        self.draw()

    def enrich_edges(self):
        edges = dict()
        for s in self.states:
            for sym in self.transitions[s]:
                dest = self.transitions[s][sym]
                edge = (s, dest)

                if edge in edges:
                    edges[edge] = '{},{}'.format(edges[edge], sym)
                else:
                    edges[edge] = sym

        return edges

    def draw(self):
        G = nx.DiGraph()

        edges = list(self.edges.keys())
        print(edges)
        G.add_edges_from(edges)
        # G.add_edges_from(
        #     [('D', 'A'), ('D', 'E'), ('B', 'D'), ('D', 'E')])
        # G.add_edges_from([('B', 'C'), ('E', 'F')])
        # G.add_edges_from([('C', 'F')])

        # val_map = {'A': 1.0,
        #            'D': 0.5714285714285714,
        #            'H': 0.0}

        # values = [val_map.get(node, 0.45) for node in G.nodes()]
        edge_labels = self.edges
        print(edge_labels)
        # red_edges = [('C', 'D'), ('D', 'A')]
        # edge_colors = [
        #     'black' if not edge in red_edges else 'red' for edge in G.edges()]

        pos = nx.spring_layout(G)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        node_labels = {node: node for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels=node_labels)
        nx.draw(G, pos, node_size=250, edge_cmap=plt.cm.Reds)

        pylab.savefig('{}/dfa.png'.format(self.folder), dpi=400)
        # pylab.show()
