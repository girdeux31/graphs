import math
import matplotlib.pyplot as plt

from auxiliar_gp import error, type_checker
import drivers_gp


class Graph:

    @type_checker(bool)
    def __init__(self, directed):
        """
        PURPOSE:

         Initialize graph

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         directed    bool                 True for directed graphs, False for undirected
        """
        self.is_directed = directed
        self.nodes = list()

    @property
    def is_weighted(self):

        for node in self.nodes:
            for edge in node.edges:
                if not edge.has_weight:
                    return False

        return True

    @property
    def is_complete(self):
        """
        PURPOSE:

         True if graph is simple and every node is connected to all other nodes

        """
        if self.is_simple:

            for node in self.nodes:
                for other_node in self.nodes:
                    if node != other_node:
                        if not node.has_adjacent_node(other_node):
                            return False

            return True

        else:
            return False

    @property
    def has_cycle(self):
        """
        PURPOSE:

         True if it is possible to walk from any node and end in the same node

        """
        import itertools

        node_ids = [node.id for node in self.nodes]

        for length in range(3, len(self.nodes)+1):            # to have a walk you need at least 3 nodes
            for walk in itertools.permutations(node_ids, length):

                if self.is_closed_walk(walk + (walk[0],)):  # add first node
                    return True

        return False

    @property
    def adjacency_matrix(self):
        """
        PURPOSE:

         Square matrix whose elements indicate whether pairs of nodes are connected (value 1) or not (value 0)

        """
        matrix = [[0 for _ in range(len(self.nodes))] for _ in range(len(self.nodes))]

        for i, node in enumerate(self.nodes):
            for j, other_node in enumerate(self.nodes):
                if other_node in node.adjacent_nodes:
                    edge = node.get_edge_with_node(other_node)
                    matrix[i][j] = edge.weight if edge.weight else 1

        return matrix

    @property
    def cut_nodes(self):
        """
        PURPOSE:

         Returns a list of all cut nodes (or articulated points)

        """
        return [node.id for node in self.nodes if node.is_cut_node]

    @property
    def cut_edges(self):
        """
        PURPOSE:

         Returns a list of all cut edges

        """
        return list(set([edge.id for node in self.nodes for edge in node.edges if edge.is_cut_edge]))

    @property
    def chromatic_number(self):  #todo check
        """
        PURPOSE:

         All nodes are assignment colors in such a way that no two adjacent nodes share the same color, the chromatic
        number is the minimal number of colors for which such an assignment is possible

        """
        def is_any_ajacent_node_colored_with(nodes, colors, idx):

            return any([True for node in nodes if node in colors[idx]])

        def are_all_colors_used_in_adjacent_nodes(nodes, colors):

            return True if len(
                [get_color_of_node(node, colors) for node in nodes if is_node_colored(node, colors)]) == len(
                colors) else False

        def is_node_colored(node, colors):

            return True if any([True for nodes in colors.values() if node in nodes]) else False

        def get_color_of_node(node, colors):

            return [idx for idx, nodes in colors.items() if node in nodes][0]

        def get_color_less_used(colors):

            return sorted([(len(nodes), idx) for idx, nodes in colors.items()])[0][1]

        def get_second_color_less_used(colors):

            return sorted([(len(nodes), idx) for idx, nodes in colors.items()])[1][1]

        colors = dict()
        node = self.nodes[0]
        color_idx = 0
        colors[color_idx] = [node]

        for node in self.nodes[1:]:

            if are_all_colors_used_in_adjacent_nodes(node.adjacent_nodes, colors):

                color_idx += 1
                colors[color_idx] = [node]

            else:

                color_idx = get_color_less_used(colors)
                if is_any_ajacent_node_colored_with(node.adjacent_nodes, colors, color_idx):

                    if len(colors) < 2:
                        color_idx += 1
                        colors[color_idx] = [node]
                    else:
                        color_idx = get_second_color_less_used(colors)
                        colors[color_idx].append(node)

                else:
                    colors[color_idx].append(node)

        return len(colors)

    @property
    def minimum_weight(self):
        """
        PURPOSE:

         Returns the minimum weight of graph

        """
        if not self.is_weighted:
            error('One or more edges have no weight')

        return min([edge.weight for node in self.nodes for edge in node.edges])

    @property
    def maximum_weight(self):
        """
        PURPOSE:

         Returns the maximum weight of graph

        """
        if not self.is_weighted:
            error('One or more edges have no weight')

        return max([edge.weight for node in self.nodes for edge in node.edges])

    def __str__(self):

        text = str()
        for node in self.nodes:
            text += str(node) + '\n'

        return text

    @type_checker(dict, dict)
    def _construct(self, structure, weights):
        """
        PURPOSE:

         Returns a Graph object according to the given structure

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         structure   dict                 Dictionary whose keys are the nodes and values are list of adjacent nodes
         weights     dict                 Dictionary whose keys are the edges and values are weights
        """
        for id in structure.keys():
            drivers_gp.Node(self, id)

        for id_from, id_tos in structure.items():
            for id_to in id_tos:

                node_from = self.get_node_by_id(id_from)
                node_to = self.get_node_by_id(id_to)

                self.connect_nodes(id_from, id_to)

        for edge_id, weight in weights.items():

            edge_found = False

            for node in self.nodes:

                if node.has_edge_by_id(edge_id):

                    edge_found = True
                    edge = node.get_edge_by_id(edge_id)
                    edge._set_weight(weight)
                    break

            if not edge_found:
                error(f'Edge {edge_id} not found in structure')

    @type_checker(dict)
    def _check_structure(self, structure):
        """
        PURPOSE:

         Check given structure

        """
        # checks that adjacent nodes (values) are listed as main nodes (keys)

        for id_tos in structure.values():
            for id_to in id_tos:

                if id_to not in structure.keys():
                    error(f'Node {id_to} not found as main node')

    @type_checker(drivers_gp.Node)
    def add_node(self, node):
        """
        PURPOSE:

         Add a node to the graph

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         node        Node                 Node object to add
        """
        if node not in self.nodes:
            self.nodes.append(node)
        else:
            error(f'Node {node} is already in graph')

    @type_checker(drivers_gp.Node)
    def has_node(self, node):
        """
        PURPOSE:

         True if graph has node

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         node        Node                 Node object to check
        """
        if type(node) is drivers_gp.Node:
            return node in self.nodes
        else:
            error(f'Cannot check node of type {type(node).__name__}')

    @type_checker(str)
    def has_node_by_id(self, id):
        """
        PURPOSE:

         True if graph has a node with ID

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         id          str                  ID to check
        """
        return id.strip() in [node.id for node in self.nodes]

    @type_checker(str)
    def get_node_by_id(self, id):
        """
        PURPOSE:

         Returns node object if graph has node with ID

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         id          str                  ID to check
        """
        id = id.strip()

        if self.has_node_by_id(id):
            return [node for node in self.nodes if node.id == id][0]
        else:
            error(f'Node {id} does not exist')


    @type_checker(drivers_gp.Node)
    def _remove_node(self, node):
        """
        PURPOSE:

         Remove given node from graph

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         node        Node                 Node object to remove
        """
        if type(node) is drivers_gp.Node:

            if node in self.nodes:
                self.nodes.remove(node)
            else:
                error(f'Node {node} is not in graph {self}')

        else:
            error(f'Cannot remove node of type {type(node).__name__}')

    @type_checker(str)
    def remove_node(self, node_id):
        """
        PURPOSE:

         Remove a node (and its edges) from the graph

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         node_id     str                  Node ID to remove
        """
        node = self.get_node_by_id(node_id)
        edge_ids = [edge.id for edge in node.edges]

        for edge_id in edge_ids:
            self.remove_edge(edge_id)

        self._remove_node(node)

    @type_checker(str)
    def remove_edge(self, edge_id):
        """
        PURPOSE:

         Remove an edge from the graph

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         edge_id     str                  Edge ID to remove
        """
        for node in self.nodes:
            if node.has_edge_by_id(edge_id):
                edge = node.get_edge_by_id(edge_id)
                node._remove_edge(edge)

    @type_checker()
    def remove_all_edges(self):
        """
        PURPOSE:

         Remove all edges in graph

        """
        edges = [edge for node in self.nodes for edge in node.edges]
        nodes = [node for node in self.nodes for _ in node.edges]

        for node, edge in zip(nodes, edges):
            node._remove_edge(edge)

    @type_checker(str, str, weight=(int, float))
    def connect_nodes(self, node_from_id, node_to_id, weight=None):
        """
        PURPOSE:

         Connect self node to given node (append to adjacent nodes and create edge)

        MANDATORY ARGUMENTS:

         Parameter    Type                 Definition
         ============ ==================== ==========================================================================================
         node_from_id str                  Node id to connect from
         node_to_id   str                  Node id to connect to

        OPTIONAL ARGUMENTS:

         Parameter       Type                 Default        Definition
         =============== ==================== ============== ===========================================================================
         weight          int, float, None     None           Edge weight, use None for no weight
        """
        node_from = self.get_node_by_id(node_from_id)
        node_to = self.get_node_by_id(node_to_id)

        drivers_gp.Edge(node_from, node_to, weight=weight)

    @type_checker((int, float))
    def _get_minimum_weight_but_grater_than(self, weight):
        """
        PURPOSE:

         Returns the minimum weight of graph but greater than weight

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         weight      int, float           Weight lower limit
        """
        if not self.is_weighted:
            error('One or more edges have no weight')

        return min([edge.weight for node in self.nodes for edge in node.edges if edge.weight > weight])

    @type_checker((int, float))
    def _get_maximum_weight_but_smaller_than(self, weight):
        """
        PURPOSE:

         Returns the maximum weight of graph but smaller than weight

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         weight      int, float           Weight upper limit
        """
        if not self.is_weighted:
            error('One or more edges have no weight')

        return max([edge.weight for node in self.nodes for edge in node.edges if edge.weight < weight])

    @type_checker((int, float))
    def _get_edges_with_weight(self, weight):
        """
        PURPOSE:

         Returns a list with edges with specified weight, list will have more than one item if there are several
        edges with the same weight

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         weight      int, float           Weight value
        """
        if not self.is_weighted:
            error('One or more edges have no weight')

        edge_list = list()

        for node in self.nodes:
            for edge in node.edges:
                if edge.weight == weight and edge not in edge_list:
                    edge_list.append(edge)

        return edge_list

    @type_checker()
    def _get_edges_with_maximum_weight(self):
        """
        PURPOSE:

         Returns a list with the edge with maximum weight, list will have more than one item if there are several
        edges with the same maximum weight

        """
        return self._get_edges_with_weight(self.maximum_weight)

    @type_checker()
    def _get_edges_with_minimum_weight(self):
        """
        PURPOSE:

         Returns a list with the edge with minimum weight, list will have more than one item if there are several
        edges with the same minimum weight

        """
        return self._get_edges_with_weight(self.minimum_weight)

    @type_checker(str, bool, bool)
    def _adjacency_function_single(self, node_id, _skip_loops, _skip_bilaterals):
        """
        PURPOSE:

         Returns the list of node IDs directly connected FROM a given main node ID

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         node_id     str                  Main node ID

        PRIVATE ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         _skip_loops bool                 Remove node from output list if it is connected to itself
         _skip_bilaterals bool            Remove node from output list if it is bilaterally connected to main node
        """
        if self.has_node_by_id(node_id):

            node = self.get_node_by_id(node_id)
            output = [adjacent_node.id for adjacent_node in node.adjacent_nodes]

            if _skip_loops and node.has_loop:
                output.remove(node.id)

            if _skip_bilaterals:
                for adjacent_node in node.adjacent_nodes:
                    if adjacent_node.is_bilateraly_connected_with(node.id):
                        output.remove(adjacent_node.id)

            return output

        else:
            error(f'Node {node_id} does not exist')

    @type_checker(str, bool, bool)
    def _inverse_adjacency_function_single(self, node_id, _skip_loops, _skip_bilaterals):
        """
        PURPOSE:

         Returns the list of node IDs directly connected TO a given main node ID

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         node_id     str                  Main node ID

        PRIVATE ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         _skip_loops bool                 Remove node from output list if it is connected to itself
         _skip_bilaterals bool            Remove node from output list if it is bilaterally connected to main node
        """
        if self.has_node_by_id(node_id):

            output = list()
            node = self.get_node_by_id(node_id)

            for other_node in self.nodes:
                for adjacent_node in other_node.adjacent_nodes:
                    if node_id == adjacent_node.id:
                        output.append(other_node.id)

                        if _skip_bilaterals and other_node.is_bilateraly_connected_with(node.id):
                            output.remove(other_node.id)

            if _skip_loops and node.has_loop:
                output.remove(node.id)

            return output

        else:
            error(f'Node {node_id} does not exist')

    @type_checker((list, str), bool, bool)
    def _adjacency_function_multiple(self, node_ids, _skip_loops, _skip_bilaterals):
        """
        PURPOSE:

         Returns the list of node IDs directly connected FROM a given list of node IDs

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         node_id     str                  Main node ID

        PRIVATE ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         _skip_loops bool                 Remove node from output list if it is connected to itself
         _skip_bilaterals bool            Remove node from output list if it is bilaterally connected to main node
        """
        output = list()
        node_ids = node_ids if type(node_ids) is list else [node_ids]

        for node_id in node_ids:
            output += self._adjacency_function_single(node_id, _skip_loops, _skip_bilaterals)

        return list(set(output))

    @type_checker((list, str), bool, bool)
    def _inverse_adjacency_function_multiple(self, node_ids, _skip_loops, _skip_bilaterals):
        """
        PURPOSE:

         Returns the list of node IDs directly connected TO a given list of node IDs

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         node_id     str                  Main node ID

        PRIVATE ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         _skip_loops bool                 Remove node from output list if it is connected to itself
         _skip_bilaterals bool            Remove node from output list if it is bilaterally connected to main node
        """
        output = list()
        node_ids = node_ids if type(node_ids) is list else [node_ids]

        for node_id in node_ids:
            output += self._inverse_adjacency_function_single(node_id, _skip_loops, _skip_bilaterals)

        return list(set(output))

    @type_checker((list, str), power=int, _skip_loops=bool, _skip_bilaterals=bool)
    def adjacency_function(self, node_ids, power=1, _skip_loops=False, _skip_bilaterals=False):
        """
         PURPOSE:

          Returns the list of node IDs directly connected FROM (positive power) or TO (negative power) a given list of node IDs

         MANDATORY ARGUMENTS:

          Parameter   Type                 Definition
          =========== ==================== ==========================================================================================
          node_id     str                  Main node ID

          Parameter   Type                 Default        Definition
          =========== ==================== ============== ===========================================================================
          power       int                  1              Steps of connected nodes, use direct function is positive, inverse if negative

         PRIVATE ARGUMENTS:

          Parameter   Type                 Default        Definition
          =========== ==================== ============== ===========================================================================
          _skip_loops bool                 False          Remove node from output list if it is connected to itself
          _skip_bilaterals bool            False          Remove node from output list if it is bilaterally connected to main node
         """
        if power == 0:

            error('Power in adjacency function cannot be zero')

        elif power == +1:

            return self._adjacency_function_multiple(node_ids, _skip_loops, _skip_bilaterals)

        elif power == -1:

            return self._inverse_adjacency_function_multiple(node_ids, _skip_loops, _skip_bilaterals)

        elif power > +1:

            output = self._adjacency_function_multiple(self.adjacency_function(node_ids, power=power-1), _skip_loops, _skip_bilaterals)
            return output

        elif power < -1:

            output = self._inverse_adjacency_function_multiple(self.adjacency_function(node_ids, power=power+1), _skip_loops, _skip_bilaterals)
            return output

    @type_checker(str)
    def _connected_component_of(self, node_id):

        output = set([node_id])

        for _ in self.nodes:
            gamma = self.adjacency_function(list(output), power=+1)
            output.update(gamma)

        return list(output)

    @type_checker(str)
    def _strong_connected_component_of(self, node_id):

        node = self.get_node_by_id(node_id)
        return list(set([other_node.id for other_node in self.nodes if node.is_strongly_connected_with(other_node.id)]))

    @type_checker((list, tuple))
    def is_walk(self, node_ids):
        """
        PURPOSE:

         True if a given node in the input list is connected to the next node of the list

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         node_ids    list                 List of node IDs
        """
        if len(node_ids) >= 2:
            nodes = [self.get_node_by_id(node_id) for node_id in node_ids]
            return True if all([node_from.has_adjacent_node(node_to) for node_from, node_to in zip(nodes[:-1], nodes[1:])]) else False
        else:
            error('A walk must have at least 2 nodes')

    @type_checker((list, tuple))
    def is_open_walk(self, node_ids):
        """
        PURPOSE:

         True if the list of node IDs forms a walk and the first and last node are different

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         node_ids    list                 List of node IDs
        """
        if self.is_walk(node_ids):

            if node_ids[0] != node_ids[-1]:
                return True
            else:
                return False

        else:
            return False

    @type_checker((list, tuple))
    def is_closed_walk(self, node_ids):
        """
        PURPOSE:

         True if the list of node IDs forms a walk and the first and last node are the same

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         node_ids    list                 List of node IDs
        """
        if self.is_walk(node_ids):

            if node_ids[0] == node_ids[-1]:
                return True
            else:
                return False

        else:
            return False

    @type_checker((list, tuple))
    def is_trail(self, node_ids):
        """
        PURPOSE:

         True if the list of node IDs forms an open walk and no edge is repeated

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         node_ids    list                 List of node IDs
        """
        if self.is_walk(node_ids):

            edges = list()
            nodes = [self.get_node_by_id(node_id) for node_id in node_ids]

            for node_from, node_to in zip(nodes[:-1], nodes[1:]):
                edge = node_from.get_edge_with_node(node_to)

                if edge in edges:
                    return False
                else:
                    edges.append(edge)

            return True

        else:
            return False

    @type_checker((list, tuple))
    def is_circuit(self, node_ids):
        """
        PURPOSE:

         True if the list of node IDs forms a closed walk and a trail

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         node_ids    list                 List of node IDs
        """
        if self.is_walk(node_ids):
            return True if self.is_trail(node_ids) and self.is_closed_walk(node_ids) else False
        else:
            return False

    @type_checker((list, tuple))
    def is_path(self, node_ids):
        """
        PURPOSE:

         True if the list of node IDs form an open walk, a trail and no node is repeated

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         node_ids    list                 List of node IDs
        """
        if self.is_walk(node_ids):

            node_is_repeated = any([node_ids.count(node_id) > 1 for node_id in node_ids])
            return True if self.is_trail(node_ids) and not node_is_repeated else False

        else:
            return False

    @type_checker((list, tuple))
    def is_cycle(self, node_ids):
        """
        PURPOSE:

         True if the list of node IDs form a close walk, a trail and only first and last node is repeated

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         node_ids    list                 List of node IDs
        """
        if self.is_walk(node_ids):
            return True if self.is_path(node_ids[:-1]) and self.is_closed_walk(node_ids) else False
        else:
            return False

    @type_checker(_show=bool)
    def show(self, _show=True):
        """
        PURPOSE:

         Represents a graph

        PRIVATE ARGUMENTS:

         Parameter       Type                 Default        Definition
         =============== ==================== ============== ===========================================================================
         _show           bool                 True           True to show the result on screen
        """
        fig, ax = plt.subplots()
        plt.axis('off')

        for node in self.nodes:

            # add nodes
            ax.scatter(x=node.x,
                       y=node.y,
                       s=node.size,
                       color=node.face_color,
                       edgecolor=node.border_color,
                       marker=node.style,
                       zorder=2)

            # add node IDs
            ax.text(x=node.x,
                    y=node.y,
                    s=node.id,
                    color=node.id_color,
                    fontsize=node.id_size,
                    fontfamily=node.id_font,
                    transform=ax.transData,
                    zorder=3,
                    ha='center',
                    va='center')

            for node_to in node.adjacent_nodes:

                edge = node.get_edge_with_node(node_to)

                if self.is_directed:

                    d_rx, d_ry = node.get_angle_to(node_to)
                    # print(edge.dx, -1*math.copysign(d_rx, edge.dx))
                    # print(edge.dy, -1*math.copysign(d_ry, edge.dy))

                    # add arrows
                    # todo loops are not shown
                    ax.arrow(x=node.x,
                             y=node.y,
                             dx=edge.dx - math.copysign(d_rx, edge.dx),
                             dy=edge.dy - math.copysign(d_ry, edge.dy),
                             color=edge.color,
                             width=edge.width,
                             head_width=5*edge.width,
                             length_includes_head=True,
                             transform=ax.transData,
                             zorder=1)

                else:

                    # add edges
                    ax.plot([node.x, node_to.x],
                            [node.y, node_to.y],
                            color=edge.color,
                            linestyle=edge.style,
                            linewidth=edge.width,
                            zorder=1)

                if edge.has_weight:  # todo check weights

                    # add weight shape
                    ax.scatter(x=edge.weight_x,
                               y=edge.weight_y,
                               s=edge.shape_size,
                               color=edge.shape_face_color,
                               edgecolor=edge.shape_border_color,
                               marker=edge.shape_style,
                               zorder=2)

                    # add weight text
                    ax.text(x=edge.weight_x,
                            y=edge.weight_y,
                            s=str(edge.weight),
                            color=edge.weight_color,
                            fontsize=edge.weight_size,
                            fontfamily=edge.weight_font,
                            transform=ax.transData,
                            zorder=3,
                            ha='center',
                            va='center')

        if _show:
            plt.show()

    @type_checker(str)
    def save(self, file):
        """
        PURPOSE:

         Save representation as an image

        OPTIONAL ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         file        str                  File path or name
        """
        self.show(_show=False)

        plt.savefig(file, bbox_inches='tight')
        plt.close()

    @type_checker(str)
    def to_xml(self, file):
        """
        PURPOSE:

         Save graph as xml to import in https://graphonline.ru/en/

        OPTIONAL ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         file        str                  File path or name
        """
        if not file.endswith('.graphtml'):
            file += '.graphtml'

        with open(file, 'w') as f:

            edges = list()

            # write header
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n\n')
            f.write('<graphml>\n')
            f.write('\t<graph id="Graph" uidGraph="1" uidEdge="1">\n')

            # write nodes
            for node in self.nodes:
                node.to_xml(f)

            # write edges, but do not repeat
            for node in self.nodes:
                for edge in node.edges:

                    if edge not in edges:
                        edge.to_xml(f)

                    edges.append(edge)

            # write tail
            f.write('\t</graph>\n')
            f.write('</graphml>\n')
