import random
from utils.utils import weighted_random_choices, flatten_list, pairwise, weighted_random_choice, remove_duplicates_array, tuple_to_string
from utils.name_gen import name_gen
from termcolor import colored
import itertools


class property_gen():
    def __init__(self, msgservers_graph, configuration):
        self.msgservers_graph = msgservers_graph
        self.causality_count = configuration.causality_count
        self.non_causality_count = configuration.non_causality_count
        self.property_length = configuration.property_length

        self.causality_set = list()
        self.non_causality_set = list()

        property_set = self.choose_property_set()

        self.property_set = property_set

    def get_property_set(self):
        return self.property_set

    def choose_property_set(self):
        def fix_format(arr):
            return [self.convert_edge_to_property_seq(edge) for edge in arr]

        causality_set = self.choose_causality_property_set()
        causality_set = [fix_format(p) for p in causality_set]
        causality_set = remove_duplicates_array(causality_set)
        # print('causality_set', causality_set)

        non_causality_set = self.choose_non_causality_property_set()
        non_causality_set = [fix_format(p) for p in non_causality_set]
        non_causality_set = remove_duplicates_array(non_causality_set)
        # print('non_causality_set', non_causality_set)

        self.causality_set = causality_set
        self.non_causality_set = non_causality_set

        return causality_set + non_causality_set

    def choose_non_causality_property_set(self):
        non_causal_paths = list()
        wrong_paths_limit = 30
        repeated_paths_count, none_count = 0, 0
        while len(non_causal_paths) < self.non_causality_count:
            new_path = self.generate_non_causal_path(self.property_length)
            if new_path is None:
                none_count += 1
                if none_count == wrong_paths_limit:
                    assert False, "Algorithm cannot find any non causal path with length " + str(self.property_length) + ". Maybe graph doesn't have enough edges or it's completely causal."
                else:
                    continue
            if new_path not in non_causal_paths:
                non_causal_paths.append(new_path)
                none_count = 0
            else: repeated_paths_count += 1
            if repeated_paths_count == wrong_paths_limit: # sets a maximum limit to repeated paths (when it occurs, it means that the algorithm can't genreate a new path)
                assert False, "Maximum number of non causal paths is " + str(len(non_causal_paths)) + ", but required is " + str(self.non_causality_count)

        print("Non causal properties", non_causal_paths)
        return non_causal_paths

    def generate_non_causal_path(self, path_length):
        new_path = []
        max_length = self.msgservers_graph.max_path_length()
        for i in range(max_length):
            paths = self.remove_duplicates(
                        self.get_weighted_paths_helper_shorter(
                            self.msgservers_graph.get_paths_with_length_between_range(i, max_length)))
            random.shuffle(paths)
            while len(paths) != 0:
                path = paths.pop()
                for edge in path[0]:
                    if edge in new_path or (len(new_path) > 0 and (self.is_in_same_path(new_path[-1], edge) or new_path[-1][0] == edge[0])): continue
                    else:
                        new_path.append(edge)
                        break
                if len(new_path) == path_length:
                    return new_path
        # print("selected path(doesn't have enough edges):", new_path)
        return None

    def is_in_same_path(self, first_edge, second_edge):
        return (self.msgservers_graph.has_path(first_edge[1], second_edge[0]) 
            or self.msgservers_graph.has_path(second_edge[1], first_edge[0]))

    def choose_causality_property_set(self):
        causality_count = self.causality_count
        selected_paths = []
        round = 0
        while causality_count != 0:
            if self.property_length == round:
                assert False, 'It has generated {} causal properties. Maybe property_length or causality_count values are too big for this graph.'.format(len(selected_paths))
            weighted_paths = [(self.add_edges_to_complete(p, self.property_length), w) for p, w in
                                self.remove_duplicates(self.get_weighted_paths(self.property_length - round + 1))]
            weighted_paths = [(p, w) for p, w in weighted_paths if len(p) == self.property_length]
            if len(weighted_paths) == 0:
                round += 1
                continue
            if len(weighted_paths) >= causality_count:
                if round == 0:
                    return weighted_random_choices(weighted_paths, causality_count)
                else:
                    selected_paths.extend([p for p in weighted_random_choices(weighted_paths, causality_count) if p not in selected_paths])
                    print(colored("There wasn't enough edge to generate complete causal properties, so causal properties contain some non causal edges.", 'yellow'))
                    return selected_paths
            else:
                new_paths = [p for p, w in weighted_paths if p not in selected_paths]
                selected_paths.extend(new_paths)
                causality_count -= len(new_paths)
            round += 1
        print(colored("There wasn't enough edge to generate complete causal properties, so causal properties contain some non causal edges.", 'yellow'))
        return selected_paths

    def add_edges_to_complete(self, path, total_length):
        if len(path) == total_length:
            return path
        all_edges = self.msgservers_graph.all_paths_with_length(2)
        for i in range(total_length - len(path)):
            random.shuffle(all_edges)
            for edge in all_edges:
                if edge in path or self.is_in_same_path(path[-1], edge) or path[-1][0] == edge[0]: continue
                path.append(edge)
                break
        return path

    def remove_duplicates(self, weighted_paths):
        def sortSecond(val):
            return val[1]

        weighted_paths.sort(key=sortSecond, reverse=True)
        # print('sorted', weighted_paths)
        seen = set()

        def seen_cond(_x):
            x = tuple(_x)
            return not (x in seen or seen.add(x))

        return [(a, b) for a, b in weighted_paths if seen_cond(a)]

    def get_weighted_paths(self, path_length_needed):
        equal_or_longer_paths = self.msgservers_graph.all_paths_with_length_more_equal(
            path_length_needed)
        # print('equal_or_longer_paths', equal_or_longer_paths)

        shorter_paths = self.msgservers_graph.all_paths_with_length_in_range(path_length_needed, 2)
        
        res_shorter = self.get_weighted_paths_helper_shorter(shorter_paths)
        res = self.get_weighted_paths_helper(equal_or_longer_paths, path_length_needed)

        # print('res', res)
        # print('res_shorter', res_shorter)
        return res + res_shorter

    def get_weighted_paths_helper(self, equal_or_longer_paths, path_length_needed):
        # Generates paths with length == path_length_needed
        # output is [([subpath], length_of_path)]
        # if path_length_needed = 2,
        # output of [1,2,3] is [([1,2], 3), ([1,3], 3), ([2,3], 3)]
        # output of [1,2] is [([1,2], 2)]
        res = flatten_list([[(cp, len(p)) for cp in [
            list(x) for x in list(
                itertools.combinations(pairwise(p), path_length_needed - 1))
        ]] for p in equal_or_longer_paths])

        return res

    def get_weighted_paths_helper_shorter(self, shorter_paths):
        res = [(pairwise(p), len(p)) for p in shorter_paths]

        return res

    def convert_edge_to_property_seq(self, edge):
        return (name_gen.get_rebeca_name_of_msgserver(edge[0]), edge[1],
                name_gen.get_rebeca_name_of_msgserver(edge[1]))

    

    def write_in_json(self, json_output_file):
        # print()
        # print('self.causality_set',self.causality_set)
        # print(self.non_causality_set)
        # print()

        json_output_file.write('"casuality sequences": {},\n'.format(
            repr([['"{}"'.format(tuple_to_string(p)) for p in x] for x in self.causality_set]).replace('\'', '')))


        json_output_file.write('"Non casuality sequences": {},\n'.format(
            repr([['"{}"'.format(tuple_to_string(p)) for p in x] for x in self.non_causality_set]).replace('\'', '')))


