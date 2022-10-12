import copy

from auxiliar_gp import error, type_checker
import drivers_gp


class Undigraph(drivers_gp.Graph):

    @type_checker(dict, weights=dict)
    def __init__(self, structure, weights=dict()):
        """
        PURPOSE:

         Initialize graph

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         structure   dict                 Dictionary whose keys are the nodes and values are list of adjacent nodes

        OPTIONAL ARGUMENTS:

         Parameter       Type                 Default        Definition
         =============== ==================== ============== ===========================================================================
         weights         dict                 dict()         Dictionary whose keys are the edges and values are weights
        """
        super().__init__(False)

        # call methods
        self._check_structure(structure)
        self._remove_opposite_connections(structure)
        self._construct(structure, weights)

    @type_checker(dict)
    def _check_structure(self, structure):
        """
        PURPOSE:

         Check structure for undigraphs

        """
        super()._check_structure(structure)

        for id_from, id_tos in structure.items():
            for id_to in id_tos:

                # check that each connection is also listed as opposite connection
                # for example {1: ['2'], 2: ['1']}

                if id_from not in structure[id_to]:

                    error(f'For undirected graphs, all edges must be set in both directions, node '
                          f'{id_from} is connected to {id_to} but {id_to} is not connected to {id_from}')

                # chack that each multi-connection is also listed the same number of times in the opposite way
                # for example {1: ['2', '2'], 2: ['1', '1']}

                connections = id_tos.count(id_to)
                opposite_connections = structure[id_to].count(id_from)

                if connections != opposite_connections:

                    error(f'For undirected graphs, all multi-edges must be set in both directions, nodes '
                          f'{id_from} and {id_to} are connected {connections} time(s), but nodes '
                          f'{id_to} and {id_from} are connected {opposite_connections} time(s)')

    @type_checker(dict)
    def _remove_opposite_connections(self, structure):
        """
        PURPOSE:

         Remove opposite connections so only one edge is created

        """
        for id_from, id_tos in structure.items():
            for id_to in id_tos:

                if id_from != id_to:
                    structure[id_to].remove(id_from)

    @property
    def is_simple(self):
        """
        PURPOSE:

         True if there are no loops or multiple edges

        """
        return False if [node for node in self.nodes if node.has_loop] else True

    @property
    def is_regular(self):
        """
        PURPOSE:

         True if each node has the same number of neighbors (i.e. every node has the same degree)

        """
        degree = self.nodes[0].degree
        return self.is_k_regular(degree)

    @type_checker(int)
    def is_k_regular(self, k):
        """
        PURPOSE:

         True if each node has 'k' neighbors (i.e. every node has degree 'k')

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         k           int                  Degree
        """
        return True if all([node.degree == k for node in self.nodes]) else False

    @property
    def connected_components(self):
        """
        PURPOSE:

         Induced subgraph in which any two nodes are connected to each other by paths, and which is not connected to
        additional vertices in the rest of the graph

        """
        output = set()

        for node in self.nodes:
            output.add(tuple(sorted(self._connected_component_of(node.id))))

        return list(output)

    @property
    def is_connected(self):
        """
        PURPOSE:

         True if every node is reachable from every other node (i.e. there is only one connected component)

        """
        return len(self.connected_components) == 1

    @property
    def is_tree(self):
        """
        PURPOSE:

         True if any two nodes are connected by exactly one path

        """
        return True if self.is_connected and not self.has_cycle else False

    @property
    def is_eulerian(self):
        """
        PURPOSE:

         True if all nodes have even degree

        """
        return all([node.degree % 2 == 0 for node in self.nodes])

    @property
    def has_eulerian_trail(self):
        """
        PURPOSE:

         True if all nodes have even degree except 2

        """
        return True if [node.degree % 2 != 0 for node in self.nodes].count(True) == 2 else False

    @property
    def is_bipartite(self):
        """
        PURPOSE:

         True if nodes can be divided into two disjoint and independent sets such that every edge connects a node
        from one to the other set

         See algorithm in https://www.baeldung.com/cs/graphs-bipartite

        """
        # todo what about directed graphs
        # check https://stackoverflow.com/questions/33857758/how-to-test-for-bipartite-in-directed-graph
        if self.is_connected:

            set1 = set()
            set2 = set()
            r = [node for node in self.nodes]

            while r:
                n1 = r.pop()

                for n2 in n1.adjacent_nodes:
                    if n2.id not in set1 and n2.id not in set2:

                        if n1.id in set1:
                            set2.update([n2.id])
                        else:
                            set1.update([n2.id])
                            r.append(n2)

            if set1.intersection(set2):
                return False
            else:
                return True

        else:
            return False

    @type_checker()
    def get_bipartite_components(self):
        """
        PURPOSE:

         Returns two disjoint and independent sets into which a bipartite graph can be divided

        """
        if self.is_bipartite:

            set1 = set()
            set2 = set()
            r = [node for node in self.nodes]

            while r:
                n1 = r.pop()

                for n2 in n1.adjacent_nodes:
                    if n2.id not in set1 and n2.id not in set2:

                        if n1.id in set1:
                            set2.update([n2.id])
                        else:
                            set1.update([n2.id])
                            r.append(n2)

            return set1, set2

        else:
            error('Method get_bipartite_components() can only be used in bipartite graphs')

    @type_checker()
    def get_complementary_graph(self):
        """
        PURPOSE:

         Returns an undirected graph in which two vertices are connected only if they are not connected in the original graph

        """
        structure = dict()

        for node in self.nodes:

            structure[node.id] = list()

            for other_node in self.nodes:
                if node != other_node and other_node not in node.adjacent_nodes:

                    structure[node.id].append(other_node.id)

        return Undigraph(structure)

    @type_checker()
    def get_closure(self):
        """
        PURPOSE:

         Returns an undirected graph obtained from G by repeatedly adding edges joining pairs of nonadjacent vertices with degree sum at least the number of nodes until no such pair remains.

        """
        graph = copy.deepcopy(self)
        nodes = len(graph.nodes)

        for node_from in graph.nodes:
            for node_to in graph.nodes:

                if node_from != node_to and node_to not in node_from.adjacent_nodes:

                    if node_from.degree + node_to.degree >= nodes:
                        graph.connect_nodes(node_from.id, node_to.id)

        return graph

    @type_checker()
    def apply_dirac_theorem(self):
        """
        PURPOSE:

         The graph IS hamiltonian if the diract theorem is true
         If the diract theorem is false, the graph could be hamiltonian or not

        """
        delta = min([node.degree for node in self.nodes])

        return delta >= len(self.nodes)/2

    @type_checker()
    def apply_ore_theorem(self):
        """
        PURPOSE:

         The graph IS hamiltonian if the ore theorem is true
         If the ore theorem is false, the graph could be hamiltonian or not

        """
        degrees = [node.degree for node in self.nodes]
        delta_0 = min(degrees)
        degrees.remove(delta_0)
        delta_1 = min(degrees)

        return delta_0 + delta_1 >= len(self.nodes)

    @type_checker()
    def get_minimum_spanning_tree(self):  # todo can be used with direct graphs?
        """
        PURPOSE:

         Returns an undirected graph which is a tree (is connected and has no cycles) and has the minimum sum of edge weights

        """
        if not self.is_connected:
            error('Graph is not connected')

        if not self.is_weighted:
            error('One or more edges have no weight')

        graph = copy.deepcopy(self)  # deep copy of graph
        graph.remove_all_edges()

        min_weight = self.minimum_weight - 1  # -1 to satisfy first time while condition
        total_weight = 0.0

        while min_weight < self.maximum_weight:

            min_weight = self._get_minimum_weight_but_grater_than(min_weight)
            min_edges = self._get_edges_with_weight(min_weight)

            for min_edge in min_edges:

                graph.connect_nodes(min_edge.node_from.id, min_edge.node_to.id)
                node_from = graph.get_node_by_id(min_edge.node_from.id)
                node_to = graph.get_node_by_id(min_edge.node_to.id)
                edge = node_from.get_edge_with_node(node_to)
                edge._set_weight(min_weight)

                if graph.has_cycle:
                    graph.remove_edge(edge.id)
                    continue

                total_weight += min_weight

                if graph.is_tree:
                    break

        return graph, total_weight

    @type_checker()
    def get_maximum_spanning_tree(self):  # todo can be used with direct graphs?
        """
        PURPOSE:

         Returns an undirected graph which is a tree (is connected and has no cycles) and has the maximum sum of edge weights

        """
        if not self.is_connected:
            error('Graph is not connected')

        if not self.is_weighted:
            error('One or more edges have no weight')

        graph = copy.deepcopy(self)  # deep copy of graph
        graph.remove_all_edges()

        max_weight = self.maximum_weight + 1  # +1 to satisfy first time while condition
        total_weight = 0.0

        while max_weight > self.minimum_weight:

            max_weight = self._get_maximum_weight_but_smaller_than(max_weight)
            max_edges = self._get_edges_with_weight(max_weight)

            for max_edge in max_edges:

                graph.connect_nodes(max_edge.node_from.id, max_edge.node_to.id)
                node_from = graph.get_node_by_id(max_edge.node_from.id)
                node_to = graph.get_node_by_id(max_edge.node_to.id)
                edge = node_from.get_edge_with_node(node_to)
                edge._set_weight(max_weight)

                if graph.has_cycle:
                    graph.remove_edge(edge.id)
                    continue

                total_weight += max_weight

                if graph.is_tree:
                    break

        return graph, total_weight

    @type_checker()
    def get_extremes_of_eulerian_trail(self):
        """
        PURPOSE:

         Return the extremes of the eulerian trail, nodes with odd degree

        """
        if self.has_eulerian_trail:
            return [node.id for node in self.nodes if node.degree % 2 != 0]
        else:
            error('Graph has no eulerian trail')