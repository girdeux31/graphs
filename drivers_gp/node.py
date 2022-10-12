import copy
import random
import math

from auxiliar_gp import error, type_checker
import drivers_gp


class Node:

    # @type_checker((), str, x=(int, float), y=(int, float), size=(int, float),
    #                                      face_color=str, border_color=str, style=str,
    #                                      id_color=str, id_size=(int, float), id_font=str)
    def __init__(self, graph, id, x=float(), y=float(), size=300.0,
                                  face_color='#68aeba', border_color='#534641', style='o',
                                  id_color='#f0d543', id_size=10.0, id_font='sans-serif'):
        """
        PURPOSE:

         Initialize node

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         graph       Graph                Graph object to add node to
         id          str                  Node ID

        OPTIONAL ARGUMENTS:

         Parameter       Type                 Default        Definition
         =============== ==================== ============== ===========================================================================
         x               int, float           float()        X possition, random if empty
         y               int, float           float()        Y possition, random if empty
         size            int, float           300.0          Node size
         face_color      str                  '#68aeba'      Node face color
         border_color    str                  '#534641'      Node border color
         style           str                  'o'            Node shape
         id_color        str                  '#f0d543'      Node ID color
         id_size         int, float           10.0           Node ID size
         id_font         str                  'sans-serif'   Node ID font
        """
        if isinstance(graph, (drivers_gp.Undigraph, drivers_gp.Digraph)):
            self.graph = graph
        else:
            error(f'Cannot backreference object of type {type(graph).__name__}')

        if isinstance(id, str):
            self.id = id
        else:
            error(f'ID must be of type str but it is {type(id).__name__}')

        self.edges = list()

        # attributes for graph representation
        self.x = x
        self.y = y
        self.size = size
        self.face_color = face_color
        self.border_color = border_color
        self.style = style
        self.id_color = id_color
        self.id_size = id_size
        self.id_font = id_font

        if not self.x:
            self.x = int(1000*random.random())

        if not self.y:
            self.y = int(1000*random.random())

        # add node to graph
        self.graph.add_node(self)

    @property
    def adjacent_nodes(self):
        """
        PURPOSE:

         Get list of adjacent nodes

        """
        nodes = list()

        for edge in self.edges:

            if edge.node_from != self and edge.node_to != self:
                error(f'Edge {edge} is not connected to node {self}')

            if edge.node_from == self:
                nodes.append(edge.node_to)
            elif edge.node_to == self:
                nodes.append(edge.node_from)

        return nodes

    @property
    def is_isolated(self):
        """
        PURPOSE:

         True if node is not connected to any other node

        """
        return len(self.adjacent_nodes) == 0

    @property
    def is_pendant(self):
        """
        PURPOSE:

         True if node is connected to one node only

        """
        return len(self.adjacent_nodes) == 1

    @property
    def has_loop(self):
        """
        PURPOSE:

         True if node is connected to itself

        """
        return self.id in [node.id for node in self.adjacent_nodes]

    @property
    def has_bilateral_connection(self):
        """
        PURPOSE:

         True if node is connected to other node in both directions

        """
        return True if [node for node in self.adjacent_nodes if node.has_adjacent_node(self)] else False

    @property
    def degree(self):

        if self.graph.is_directed:
            error('For directed graphs use either outdegree() or indegree() method')
        else:
            return len(self.edges) + (1 if self.has_loop else 0)

    @property
    def outdegree(self): # todo what about loops

        if not self.graph.is_directed:
            error('For undirected graphs use degree() method')
        else:
            return len(self.edges)

    @property
    def indegree(self): # todo what about loops

        if not self.graph.is_directed:
            error('For undirected graphs use degree() method')
        else:
            return len([edge for node in self.graph.nodes for edge in node.edges if edge.node_to == self])

    @property
    def is_cut_node(self):
        """
        PURPOSE:

         True if the graph is disconnected when the node (and its edges) are removed (i.e. the connected components
        increases), the node is called articulation point

        """
        n0 = len(self.graph.connected_components)  # todo only works with undirected graphs
        graph = copy.deepcopy(self.graph)
        graph.remove_node(self.id)
        n1 = len(graph.connected_components)

        return True if n1 > n0 else False

    def __str__(self):

        return f'{self.id}: {{{str([str(edge) for edge in self.edges]).replace("[", "").replace("]", "")}}}'

    def __eq__(self, node):
        """
        PURPOSE:

         Define equivalence operator. True if both nodes have the same id and same edges

        """
        if type(node) is drivers_gp.Node:

            if self.id == node.id:

                for edge in self.edges:
                    if edge not in node.edges:
                        return False

                for edge in node.edges:
                    if edge not in self.edges:
                        return False

            else:
                return False

            return True

        else:
            error(f'Cannot compare node with object of type {type(node).__name__}')

    def add_edge(self, edge):
        """
        PURPOSE:

         Add edge to node

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         edge        Edge                 Edge object to add
        """
        if type(edge) is drivers_gp.Edge:

            if edge not in self.edges:
                self.edges.append(edge)
            else:
                error(f'Edge {edge} is already in node {self}')

        else:
            error(f'Cannot add edge of type {type(edge).__name__}')

    def has_edge(self, edge):
        """
        PURPOSE:

         True if node has edge

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         edge        Edge                 Edge object to check
        """
        if type(edge) is drivers_gp.Edge:
            return edge in self.edges  # checks inverted edge for undirected graphs
        else:
            error(f'Cannot check edge of type {type(edge).__name__}')

    def has_edge_with_node(self, node_to, s=1):
        """
        PURPOSE:

         True if node has connection to given node

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         node_to     Node                 Node object to check

        OPTIONAL ARGUMENTS:

         Parameter       Type                 Default        Definition
         =============== ==================== ============== ===========================================================================
         s               int                  1              Edge index for multigraphs
        """
        if type(node_to) is drivers_gp.Node:
            return len([edge for edge in self.edges if edge.s == s and (edge.node_to == node_to or edge.node_from == node_to)]) > 0
        else:
            error(f'Cannot check node of type {type(node_to).__name__}')

    @type_checker(str, s=int)
    def has_edge_by_id(self, id, s=1):
        """
        PURPOSE:

         True if node has edge with ID

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         id          str                  ID to check

        OPTIONAL ARGUMENTS:

         Parameter       Type                 Default        Definition
         =============== ==================== ============== ===========================================================================
         s               int                  1              Edge index for multigraphs
        """
        if self.graph.is_directed:
            output =  id.strip() in [edge.id for edge in self.edges if edge.s == s]
        else:
            output_direct = id.strip() in [edge.id for edge in self.edges if edge.s == s]
            output_reversed = id.strip() in [edge.id_reversed for edge in self.edges if edge.s == s]
            output = output_direct or output_reversed

        return output

    @type_checker(str, s=int)
    def get_edge_by_id(self, id, s=1):
        """
        PURPOSE:

         Returns edge object if node has edge with ID

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         id          str                  ID to check

        OPTIONAL ARGUMENTS:

         Parameter       Type                 Default        Definition
         =============== ==================== ============== ===========================================================================
         s               int                  1              Edge index for multigraphs
        """
        id = id.strip()

        if self.has_edge_by_id(id, s=s):

            if self.graph.is_directed:
                return [edge for edge in self.edges if edge.s == s and edge.id == id][0]
            else:
                return [edge for edge in self.edges if edge.s == s and (edge.id == id or edge.id_reversed == id)][0]

        else:
            error(f'Edge {id} is not in node {self}')

    def get_edge_with_node(self, node_to, s=1):
        """
        PURPOSE:

         Returns edge object if node is connected with given node

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         node_to     Node                 Node object to check

        OPTIONAL ARGUMENTS:

         Parameter       Type                 Default        Definition
         =============== ==================== ============== ===========================================================================
         s               int                  1              Edge index for multigraphs
        """
        if type(node_to) is drivers_gp.Node:

            if self.has_adjacent_node(node_to):

                for edge in self.edges:

                    if self.graph.is_directed:

                        if edge.s == s and edge.node_to == node_to:
                            return edge

                    else:

                        if edge.s == s and edge.node_from in [self, node_to] and edge.node_to in [self, node_to]:
                            return edge

            else:
                error(f'Node {self} is not adjacent to node {node_to}')

        else:
            error(f'Cannot check node of type {type(node_to).__name__}')

    def _remove_edge(self, edge):
        """
        PURPOSE:

         Remove given edge from self node, but not the adjacent nodes

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         edge        Edge                 Edge object to remove
        """
        if type(edge) is drivers_gp.Edge:

            if edge in self.edges:
                self.edges.remove(edge)
            else:
                error(f'Edge {edge} is not in node {self}')

        else:
            error(f'Cannot remove edge of type {type(edge).__name__}')

    def has_adjacent_node(self, node_to):
        """
        PURPOSE:

         True if given node is in adjacent nodes of self node

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         node_to     Node                 Node object to check
        """
        if type(node_to) is drivers_gp.Node:
            return node_to in self.adjacent_nodes
        else:
            error(f'Cannot check node of type {type(node_to).__name__}')

    def get_adjacent_node(self, node_to):
        """
        PURPOSE:

         Returns node object if given node is in adjacent nodes of self node

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         node_to     Node                 Node object to check
        """
        if type(node_to) is drivers_gp.Node:

            if self.has_adjacent_node(node_to):
                return [other_node for other_node in self.adjacent_nodes if node_to == other_node][0]
            else:
                error(f'Node {node_to} is not adjacent to node {self}')

        else:
            error(f'Cannot add node of type {type(node_to).__name__}')

    @type_checker(str)
    def is_bilateraly_connected_with(self, other_node_id):
        """
        PURPOSE:

         True if given node is connected to self node and self node is connected to given node

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         id          str                  ID to check
        """
        other_node = self.graph.get_node_by_id(other_node_id)
        return True if other_node != self and self.has_adjacent_node(other_node) and other_node.has_adjacent_node(self) else False

    @type_checker(str)
    def is_strongly_connected_with(self, other_node_id):
        """
        PURPOSE:

         True if there is a path from self node to given node and from given node to self node

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         id          str                  ID to check
        """
        if self.graph.is_directed:

            other_node = self.graph.get_node_by_id(other_node_id)

            power = 0
            output_positive = set([self.id])
            output_negative = set([self.id])

            for _ in self.graph.nodes:

                power += 1
                output_positive.update(self.graph.adjacency_function(self.id, power=power))    #nodes self reaches
                output_negative.update(self.graph.adjacency_function(self.id, power=-1*power)) #nodes self is reached from

                if other_node.id in output_positive and other_node.id in output_negative:
                    return True

            return False

        else:
            error('Method is_strongly_connected_with() can only be used with directed graphs')

    def to_xml(self, f):
        """
        PURPOSE:

         Save node as xml to import in https://graphonline.ru/en/

        OPTIONAL ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         f           handler              File handler to write to
        """
        f.write(f'\t\t<node positionX="{self.x}" '
                f'positionY="{1000-self.y}" '
                f'id="{self.id}" '
                f'mainText="{self.id}" '
                f'upText="" '
                f'size="{self.size/10.0}" ></node>\n')

    def get_angle_to(self, node_to):
        """
        PURPOSE:

         Returns angle between self node and given node

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         node_to     Node                 Node object to calculate angle with
        """
        if type(node_to) is drivers_gp.Node:

            radius = math.sqrt(node_to.size/math.pi)
            #radius = math.sqrt(node_to.size) / 4
            alpha = math.atan2(node_to.y - self.y, node_to.x - self.x)
            dx = radius * math.cos(alpha)
            dy = radius * math.sin(alpha)
            # print(self.id, node_to.id, radius, math.degrees(alpha), dx, dy)

            return (dx, dy)

        else:
            error(f'Cannot check node of type {type(node_to).__name__}')
