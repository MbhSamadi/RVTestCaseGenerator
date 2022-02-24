import random


class graph():
    def __repr__(self):
        return 'Graph: {}'.format(repr(self.nodes))

    def __init__(self, graph={}):
        self.nodes = graph
        self.vertices_count = len(list(graph.keys()))
        self.all_paths_cache = None

    def add_node(self, node):
        if not node in list(self.nodes.keys()):
            self.all_paths_cache = None
            self.nodes[node] = []
            self.vertices_count += 1

    def connect(self, start, end):
        if not start in self.nodes:
            return

        if end in self.nodes[start]:
            return

        self.nodes[start].append(end)
        self.all_paths_cache = None

    def connect_if_doesnt_make_loop(self, start, end):
        if self.has_path(end, start):
            return

        self.connect(start, end)
        self.all_paths_cache = None

    def remove_edge(self, start, end):
        if not start in self.nodes:
            return

        if not end in self.nodes[start]:
            return

        self.nodes[start].remove(end)
        self.all_paths_cache = None

    # getters
    def get_nodes(self):
        return list(self.nodes.keys())

    def edges(self, node):
        return self.nodes[node]

    def random_connected_node(self, node):
        edges = self.edges(node)
        return None if len(edges) == 0 else random.choice(edges)

    def nodes_that_connect_to(self, node):
        return [n for n in self.get_nodes() if (not n == node) and node in self.edges(n)]

    def nodes_with_out_degree(self, degree):
        return [n for n in self.get_nodes() if len(self.edges(n)) == degree]

    def nodes_with_in_degree(self, degree):
        return [n for n in self.get_nodes() if len(self.nodes_that_connect_to(n)) == degree]

    def get_leaves(self):
        return self.nodes_with_in_degree(0)

    # tools
    def all_paths(self):
        if self.all_paths_cache:
            return self.all_paths_cache

        all_paths = [p for ps in [self.dfs_all_paths(
            n) for n in set(self.nodes)] for p in ps]

        self.all_paths_cache = all_paths
        return all_paths

    def all_paths_with_length_more_equal(self, length):
        all_paths = self.all_paths()
        return [p for p in all_paths if len(p) >= length]
    
    def all_paths_with_length_in_range(self, less,more):
        if more - less <= 1:
            return []
        all_paths = self.all_paths()
        return [p for p in all_paths if len(p) < less and len(p) > more]

    def get_paths_with_length_between_range(self, less, more):
        all_paths = self.all_paths()
        return [p for p in all_paths if len(p) > less and len(p) <= more]

    def all_paths_with_length(self, length):
        all_paths = self.all_paths()
        return [p for p in all_paths if len(p) == length]

    def max_path_length(self):   # counts edges
        if self.isCyclic():
            return -1
        all_paths = self.all_paths()
        # print(all_paths)
        if len(all_paths) == 0:
            return 0
        max_len = max(len(p) for p in all_paths)
        return max_len - 1

    def isCyclicUtil(self, v, visited, recStack):

        # Mark current node as visited and
        # adds to recursion stack
        visited[v] = True
        recStack[v] = True

        # Recur for all neighbours
        # if any neighbour is visited and in
        # recStack then graph is cyclic
        # print(self.nodes, v)
        for neighbour in self.nodes[v]:
            if visited[neighbour] == False:
                if self.isCyclicUtil(neighbour, visited, recStack) == True:
                    return True
            elif recStack[neighbour] == True:
                return True

        # The node needs to be poped from
        # recursion stack before function ends
        recStack[v] = False
        return False

    # Returns true if graph is cyclic else false
    def isCyclic(self):
        visited = {v: False for v in self.nodes}
        recStack = {v: False for v in self.nodes}
        for node in self.nodes:
            if visited[node] == False:
                if self.isCyclicUtil(node, visited, recStack) == True:
                    return True
        return False

    def dfs_all_paths(self, v, seen=None, path=None):
        if seen is None:
            seen = []
        if path is None:
            path = [v]

        seen.append(v)

        paths = []
        for t in self.nodes[v]:
            if t not in seen:
                t_path = path + [t]
                paths.append(tuple(t_path))
                paths.extend(self.dfs_all_paths(t, seen[:], t_path))
        return paths

    def has_path(self, start, end):
        if self.find_path(start, end) == None:
            return False
        return True

    def find_path(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not start in self.nodes:
            return None
        for node in self.nodes[start]:
            if node not in path:
                newpath = self.find_path(node, end, path)
                if newpath:
                    return newpath
        return None

    def generate_edges(self):
        edges = []
        for node in self.nodes:
            for neighbour in self.nodes[node]:
                edges.append((node, neighbour))

        return edges

    def get_isolated_nodes(self):
        isolated = []
        for node in self.nodes:
            if not self.nodes[node]:
                isolated += node
        return isolated

    def find_all_paths(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if not self.nodes.has_key(start):
            return []
        paths = []
        for node in self.nodes[start]:
            if node not in path:
                newpaths = self.find_all_paths(self.nodes, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def __topological_sort_util(self,v,visited,stack):
        visited[v] = True
        for neighbor in self.nodes[v]:
            if visited[neighbor] == False:
                self.__topological_sort_util(neighbor,visited,stack)
        stack.insert(0,v)
    
    def topological_sort(self):
        visited = {e:False for e in self.nodes}
        stack = []
        for node in self.nodes:
            if visited[node] == False:
                self.__topological_sort_util(node,visited,stack)
        return stack

