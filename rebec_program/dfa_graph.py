from utils.utils import tuple_to_string


class dfa_graph_gen():
    def __init__(self, dfa_obj, backwards):
        self.states = dfa_obj['states']
        self.transitions = dfa_obj['transitions']
        self.input_symbols = dfa_obj['input_symbols']
        self.final_states = dfa_obj['final_states']
        self.initial_state = dfa_obj['initial_state']

        self.backwards = backwards
        self.vio_paths = self.get_vio_paths()
        self.vio_paths_reveresed = self.get_vio_paths_reversed()

        print('backwards', self.backwards)
        print('vio_paths', self.vio_paths)
        print('vio_paths_reveresed', self.vio_paths_reveresed)

        self.get_input_edges_to_state_cache = dict({self.initial_state: {}})
        self.enriched_transitions = self.get_all_enriched_transitions()
        self.get_all_input_edges_to_state()

    def get_all_enriched_transitions(self):
        transitions = []
        for s in self.states:
            for sym in self.transitions[s]:
                transitions.append((s, sym, self.transitions[s][sym]))

        return transitions

    def get_rebec_transitions(self, rebec):
        transitions = []

        for et in self.enriched_transitions:
            msg = et[1]
            if rebec == msg[:msg.find('-')]:
                transitions.append(et)
        # print(self.enriched_transitions, transitions, rebec)
        return transitions

    def get_pre_transitions(self, transition):
        qstart, msg, qend = transition
        if not self.is_backward(transition):
            return self.get_input_edges_to_state(qstart)
        else:
            input_transitions = self.get_input_edges_to_state(qstart)
            pre_vio = self.vio_paths_reveresed[tuple_to_string(transition)]
            # print(transition, input_transitions, pre_vio)
            return [p for p in pre_vio if p in input_transitions]

    def is_final_path(self, transition):
        return transition[2] in self.final_states

    def get_input_edges_to_state(self, state):
        if state in self.get_input_edges_to_state_cache:
            return self.get_input_edges_to_state_cache[state]

        ans = set()
        for s in self.states:
            for sym in self.transitions[s]:
                if self.transitions[s][sym] == state:
                    ans.add((s, sym, state))

        self.get_input_edges_to_state_cache[state] = ans
        return ans

    def get_all_input_edges_to_state(self):
        for s in self.states:
            for sym in self.transitions[s]:
                dest = self.transitions[s][sym]
                p = (s, sym, dest)
                if self.is_backward(p):
                    continue
                if dest in self.get_input_edges_to_state_cache:
                    self.get_input_edges_to_state_cache[dest].add(p)
                else:
                    self.get_input_edges_to_state_cache[dest] = set([p])

    def get_vio_transition(self, pre_repr):
        # pre_repr = repr(pre_path)
        # print('pre,vio', pre_repr, self.vio_paths)
        if pre_repr in self.vio_paths:
            return list(self.vio_paths[pre_repr])
        return []

    def is_backward(self, _t):
        t = tuple_to_string(_t)
        # print(t, self.vio_paths_reveresed, t in self.vio_paths_reveresed)
        return t in self.vio_paths_reveresed

    def get_vio_paths_reversed(self):
        vio_paths_reveresed = dict()
        # print(self.vio_paths)
        for pre in self.vio_paths:
            vio = self.vio_paths[pre]
            for dest in vio:
                if dest in vio_paths_reveresed:
                    vio_paths_reveresed[dest].add(pre)
                else:
                    vio_paths_reveresed[dest] = set([pre])

        # print(vio_paths_reveresed)
        return vio_paths_reveresed

    def get_vio_paths(self):
        vio_paths = dict()

        for b in self.backwards:
            paths = self.find_all_paths(b[2], b[0])
            # print('bac', b, paths)
            for p in paths:
                for t in p:
                    if t in vio_paths:
                        vio_paths[t].add(tuple_to_string(b))
                    else:
                        vio_paths[t] = set([tuple_to_string(b)])

        return vio_paths

    def get_direct_link(self, start, end):
        for sym in self.transitions[start]:
            if end in self.transitions[start][sym]:
                return sym

        return False

    def find_all_paths(self, start, end, path=[]):
        path = path + [start]

        sym = self.get_direct_link(start, end)
        if sym:
            return [[(start, sym, end)]]
        if not start in self.states:
            return []
        res = []
        for sym in self.transitions[start]:
            node = self.transitions[start][sym]
            if node not in path:
                newRes = self.find_all_paths(node, end, path)
                for r in newRes:
                    res.append([(start, sym, node)] + r)
        return res
