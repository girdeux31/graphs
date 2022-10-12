from auxiliar_gp import error, type_checker
import drivers_gp


class Digraph(drivers_gp.Graph):

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
        super().__init__(True)

        # call methods
        self._check_structure(structure)
        self._construct(structure, weights)

    @property
    def is_simple(self):
        """
        PURPOSE:

         True if there are no loops or multiple edges

        """
        return False if [node for node in self.nodes if node.has_loop or node.has_bilateral_connection] else True

    @property
    def is_regular(self):
        """
        PURPOSE:

         True if each node has the same number of neighbors (i.e. every node has the same outdegree)

        """
        degree = self.nodes[0].degree
        return self.is_k_regular(degree)

    @type_checker(int)
    def is_k_regular(self, k):
        """
        PURPOSE:

         True if each node has 'k' neighbors (i.e. every node has outdegree 'k')

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         k           int                  Outdegree
        """
        return True if all([node.outdegree == k for node in self.nodes]) else False

    @property
    def is_tree(self):
        """
        PURPOSE:

         True if the underlying undirected graph is a tree

        """
        undigraph = self.get_undigraph()
        return True if undigraph.is_tree else False

    @property
    def is_rooted_tree(self):
        """
        PURPOSE:

         True if only one node has indegree 0 and all other nodes have outdegree 1 (thus, the underlying undirected graph is a tree)

        """
        root_node = [node for node in self.nodes if node.indegree == 0]
        other_nodes = [node for node in self.nodes if node not in root_node and node.indegree == 1]

        return True if len(root_node) == 1 and len(other_nodes) == len(self.nodes)-1 and not self.has_cycle else False

    @property
    def strong_connected_components(self):
        """
        PURPOSE:

         Return a partition of the original graph into subgraphs that are themselves strongly connected

        """
        output = set()

        for node in self.nodes:

            output.add(tuple(sorted(self._strong_connected_component_of(node.id))))

        return list(output)

    @property
    def is_strongly_connected(self):
        """
        PURPOSE:

         True if every node is reachable from every other node

        """
        return len(self.strong_connected_components) == 1

    @property
    def is_weakly_connected(self):
        """
        PURPOSE:

         True if does not exist a path between any two pairs of nodes

        """
        undigraph = self.get_undigraph()
        return True if undigraph.is_connected else False

    @property
    def is_eulerian(self):
        """
        PURPOSE:

         True if all nodes have indegree == outdegree

        """
        return all([node.indegree == node.outdegree for node in self.nodes])

    @property
    def has_eulerian_trail(self):
        """
        PURPOSE:

         True if all nodes have indegree == outdegree except two with:
         indegree(u) == outdegree(u)+1, and
         outdegree(v) == indegree(v)+1

        """
        nodes = [node for node in self.nodes if node.indegree != node.outdegree]

        if len(nodes) == 2:

            if nodes[0].indegree == nodes[0].outdegree+1 and nodes[1].outdegree == nodes[1].indegree+1 or \
               nodes[1].indegree == nodes[1].outdegree+1 and nodes[0].outdegree == nodes[0].indegree+1:
                return True

        return False

    @type_checker()
    def get_extremes_of_eulerian_trail(self):
        """
        PURPOSE:

         Return the extremes of the eulerian trail, see has_eulerian_trail

        """
        if self.has_eulerian_trail:
            return [node.id for node in self.nodes if node.indegree != node.outdegree]
        else:
            error('Graph has no eulerian trail')

    @type_checker()
    def get_undigraph(self):
        """
        PURPOSE:

         Returns the underlying undirected graph (arrows are converted into edges)

        """
        structure = dict()

        for node in self.nodes:
            structure[node.id] = [other_node.id for other_node in node.adjacent_nodes]

        # add inverse connections or edges
        for key, values in structure.items():
            for node_id in values:
                if key not in structure[node_id]:
                    structure[node_id].append(key)

        return drivers_gp.Undigraph(structure)
