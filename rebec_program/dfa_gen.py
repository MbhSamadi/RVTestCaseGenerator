from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from utils.utils import tuple_to_string
import random


class dfa_gen():
    def __init__(self, property_set, configuration):
        self.backwards_count = configuration.backwards_count
        self.property_set = property_set
        self.states = set()
        self.input_symbols = set()
        self.transitions = dict()
        self.final_states = set()
        self.state_counter = 0
        self.initial_state = self.create_state()
        self.backwards = set()

    def create_state(self):
        new_state = 'q{}'.format(self.state_counter)
        self.states.add(new_state)
        self.transitions[new_state] = dict()
        self.state_counter += 1
        return new_state

    def get_dfa(self):
        # print(self.property_set)
        self.generate_dfa()

        nfa = NFA(
            states=self.states,
            input_symbols=self.input_symbols,
            transitions=self.transitions,
            initial_state=self.initial_state,
            final_states=self.final_states
        )

        # self.print_automata(nfa)

        # print('minifying DFA...')
        dfa = DFA.from_nfa(nfa)
        dfa = dfa.minify()
        # self.print_automata(dfa)

        dfa_obj = self.remove_additional_transitions(dfa)
        # self.print_automata_obj(dfa_obj)
        # print(self.vio_paths)
        dfa_obj = dfa_state_beautifier(dfa_obj).beautify_state_names()
        # self.print_automata_obj(dfa_obj)

        self.states = dfa_obj['states']
        self.transitions = dfa_obj['transitions']
        self.input_symbols = dfa_obj['input_symbols']
        self.final_states = dfa_obj['final_states']
        self.initial_state = dfa_obj['initial_state']

        self.generate_backwards()
        # print(self.vio_paths)

        return dfa_obj

    def remove_additional_transitions(self, dfa):
        trap_state = '{}'
        states = dfa.states
        transitions = dfa.transitions
        input_symbols = dfa.input_symbols

        for s in states:
            if s == trap_state:
                del transitions[trap_state]
                continue
            for sym in input_symbols:
                if transitions[s][sym] == trap_state:
                    del transitions[s][sym]
        states.remove(trap_state)

        return {
            'states': states,
            'input_symbols': input_symbols,
            'transitions': transitions,
            'initial_state': dfa.initial_state,
            'final_states': dfa.final_states
        }

    def generate_dfa(self):
        for prprty in self.property_set:
            current_state = self.initial_state
            for _p in prprty:
                p = '-'.join(_p)
                self.input_symbols.add(p)

                if not p in self.transitions[current_state]:
                    _state = self.create_state()
                    self.transitions[current_state][p] = set([_state])

                current_state = next(iter(self.transitions[current_state][p]))

            # if len(self.final_states) == 0:
            self.final_states.add(current_state)
            # else:
            #     self.transitions[current_state]

    def generate_backwards(self):
        _i_while_index_ = 0
        while _i_while_index_ < self.backwards_count:
            current_state = self.initial_state
            prprty = random.choice(self.property_set)
            # print(prprty)
            end_state_index = 0 if len(prprty) == 2 else random.randint(0, len(prprty) - 2)
            start_state_index = random.randint(end_state_index + 1, len(prprty) - 1)
            start_state = None
            end_state = None

            # pre_paths_with_this_backtrack_in_vio = []
            for i, _p in enumerate(prprty):
                # print(i, start_state_index, end_state_index)
                p = '-'.join(_p)
                # print(p, self.transitions[current_state])
                if i == end_state_index:
                    end_state = current_state
                if i == start_state_index:
                    start_state = current_state

                next_state = self.transitions[current_state][p]

                current_state = next_state

            if start_state == None:
                start_state = current_state

            # print(end_state, self.final_states)
            if end_state in self.final_states:
                continue

            # print(start_state, end_state, self.transitions)
            random_input_symbol = random.choice(
                [sym for sym in self.input_symbols if not sym in list(self.transitions[start_state].keys())])
            
            # print(random_input_symbol, self.transitions[end_state])
            if random_input_symbol in self.transitions[end_state] and self.transitions[end_state][random_input_symbol] == start_state:
                continue

            self.transitions[start_state][random_input_symbol] = end_state

            backward = (start_state, random_input_symbol, end_state)
            self.backwards.add(backward)
            _i_while_index_ += 1

    def fill_transitions(self):
        for state in self.states:
            for sym in self.input_symbols:
                if sym in self.transitions[state]:
                    continue
                self.transitions[state][sym] = set([state])

    def print_automata(self, g):
        # print()
        print(g.states)
        print(g.initial_state)
        print(g.input_symbols)
        print(g.transitions)
        print(g.final_states)
        print()

    def print_automata_obj(self, g):
        # print()
        print('states', g['states'])
        print('initial_state', g['initial_state'])
        # print('input_symbols', g['input_symbols'])
        print('transitions', g['transitions'])
        print('final_states', g['final_states'])
        print()

    def write_automata_obj(self, json_output_file, dfa_obj):

        json_output_file.write('"states": {},\n'.format(
            repr(list(dfa_obj['states'])).replace('\'', '"')))
        json_output_file.write(
            '"initial_state": "{}",\n'.format(dfa_obj['initial_state']))
        json_output_file.write('"transitions": {},\n'.format(
            repr(dfa_obj['transitions']).replace('\'', '"').replace(",", ",\n    ")))
        json_output_file.write(
            '"final_states": {},\n'.format(repr(list(dfa_obj['final_states'])).replace('\'', '"')))
        json_output_file.write('"backwards": {},\n'.format(
            repr(['{{"{}": {{"{}":"{}"}} }}'.format(x[0], x[1], x[2]) for x in self.backwards]).replace('\'', '')))
        

class dfa_state_beautifier():
    def __init__(self, dfa_obj):
        self.state_counter = 0
        self.good_bad_state_map = dict()
        self.states = dfa_obj['states']
        self.transitions = dfa_obj['transitions']
        self.input_symbols = dfa_obj['input_symbols']
        self.final_states = dfa_obj['final_states']
        self.initial_state = dfa_obj['initial_state']
        self.new_states = set()
        self.new_transitions = dict()
        self.visited = set()
        # self.vio_paths = vio_paths
        # self.new_vio_paths = dict()

    def beautify_state_names(self):

        self.recursive_beautify(self.initial_state)

        new_final_states = set()
        for old_s in self.final_states:
            new_final_states.add(self.good_state_name(old_s))

        # print(self.vio_paths)
        # for pre in self.vio_paths:
        #     new_pre = self.good_transition_name(pre)
        #     self.new_vio_paths[repr(new_pre)] = {tuple_to_string(
        #         self.good_transition_name(vio)) for vio in self.vio_paths[pre]}

        return {
            'states': self.new_states,
            'input_symbols': self.input_symbols,
            'transitions': self.new_transitions,
            'initial_state': self.good_state_name(self.initial_state),
            'final_states': new_final_states
        }

    def recursive_beautify(self, old_s):
        if old_s in self.visited:
            return
        self.visited.add(old_s)
        new_s = self.good_state_name(old_s)
        if not new_s in self.new_transitions:
            self.new_transitions[new_s] = dict()

        syms = list(self.transitions[old_s].keys())
        # print(syms, self.transitions[old_s])

        for sym in syms:
            old_dest = self.transitions[old_s][sym]
            new_dest = self.good_state_name(old_dest)
            # self.new_transitions[old_s][sym] = new_dest

            self.new_transitions[new_s][sym] = new_dest
            # print(self.new_transitions)
            del self.transitions[old_s][sym]
            self.recursive_beautify(old_dest)

    def good_state_name(self, _state):
        if _state in self.good_bad_state_map:
            return self.good_bad_state_map[_state]
        new_state = 'q{}'.format(self.state_counter)
        self.good_bad_state_map[_state] = new_state
        self.new_states.add(new_state)
        self.state_counter += 1
        return new_state

    def good_transition_name(self, transition):
        return (self.good_state_name(transition[0]), transition[1], self.good_state_name(transition[2]))
