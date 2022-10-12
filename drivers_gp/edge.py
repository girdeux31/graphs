import copy

from auxiliar_gp import error, warning, type_checker
import drivers_gp


class Edge:

    @type_checker(drivers_gp.Node, drivers_gp.Node, color=str, style=str, width=(int, float), weight=(int, float, type(None)),
                                                    weight_color=str, weight_size=(int, float), weight_font=str,
                                                    shape_size=(int, float), shape_face_color=str, shape_border_color=str, shape_style=str)
    def __init__(self, node_from, node_to, color='#c7b7c7', style='-', width=2.0, weight=None,
                                           weight_color='#f0d543', weight_size=10.0, weight_font='sans-serif',
                                           shape_size=300.0, shape_face_color='#68aeba', shape_border_color='#534641', shape_style='s'):
        """
        PURPOSE:

         Initialize node

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         node_from   Node                 Node object to connect from
         node_to     Node                 Node object to connect to

        OPTIONAL ARGUMENTS:

         Parameter       Type                 Default        Definition
         =============== ==================== ============== ===========================================================================
         color           str                  '#c7b7c7'      Edge color
         style           str                  '-'            Edge style
         width           int, float           2.0            Edge width
         weight          int, float, None     None           Edge weight, use None for no weight
         weight_color    str                  '#f0d543'      Weight color
         weight_size     int, float           10.0           Weight size
         weight_font     str                  'sans-serif'   Weight font
         shape_size      int, float           300.0          Shape size
         shape_face_color   str               '#68aeba'      Shape face color
         shape_border_color str               '#534641'      Shape border color
         shape_style     str                  's'            Shape
        """
        if type(node_from) is drivers_gp.Node:
            self.node_from = node_from
        else:
            error(f'Cannot backreference object of type {type(node_from).__name__}')

        if type(node_to) is drivers_gp.Node:
            self.node_to = node_to
        else:
            error(f'Cannot backreference object of type {type(node_to).__name__}')

        self.is_directed = self.node_from.graph.is_directed

        # attributes for graph representation
        self.color = color
        self.style = style
        self.width = width
        self.weight = weight
        self.weight_color = weight_color
        self.weight_size = weight_size
        self.weight_font = weight_font
        self.shape_size = shape_size
        self.shape_face_color = shape_face_color
        self.shape_border_color = shape_border_color
        self.shape_style = shape_style

        self.dx = self.node_to.x - self.node_from.x
        self.dy = self.node_to.y - self.node_from.y

        self.weight_x = (self.node_to.x + self.node_from.x) / 2
        self.weight_y = (self.node_to.y + self.node_from.y) / 2

        # call methods
        self._set_s()
        self._set_id()

        # add edge to node_from
        if not self.node_from.has_edge(self):
            self.node_from.add_edge(self)

        # add edge to node_to for undirected graphs
        if not self.node_to.has_edge(self) and not self.is_directed:
            self.node_to.add_edge(self)

    @property
    def is_loop(self):
        """
        PURPOSE:

         True if edge connects a node to itself

        """
        return self.node_from == self.node_to

    @property
    def is_cut_edge(self):
        """
        PURPOSE:

         True if the graph is disconnected when the edge is removed (i.e. the connected components increases), also
        called bridge edge

        """
        n0 = len(self.node_from.graph.connected_components)  # todo only work with undirected graphs
        graph = copy.deepcopy(self.node_from.graph)
        graph.remove_edge(self.id)
        n1 = len(graph.connected_components)

        return True if n1 > n0 else False

    @property
    def is_bridge(self):
        """
        PURPOSE:

         True if the graph is disconnected when the edge is removed (i.e. the connected components increases), also
        called cut edge

        """
        return self.is_cut_edge

    @property
    def has_weight(self):
        """
        PURPOSE:

         True if edge has weight

        """
        return True if self.weight else False

    def __str__(self):

        return self.id + (' (s={:d})'.format(self.s) if self.s > 1 else '')

    def __eq__(self, edge):
        """
        PURPOSE:

         Define equivalence operator. True if both
            - edges are directed/undirected
            - weights are equal
            - s indexes are equal
            - ids are equal
            - nodes on both ends of both edges have the same id
        """
        if type(edge) is drivers_gp.Edge:

            if edge.is_directed == self.is_directed and \
               edge.weight == self.weight and \
               edge.s == self.s:

                if self.is_directed:

                    if edge.id == self.id and \
                        self.node_from.id == edge.node_from.id and \
                        self.node_to.id == edge.node_to.id:
                        return True
                    else:
                        return False

                else:

                    if (edge.id == self.id or edge.id_reversed == self.id) and \
                        self.node_from.id in [edge.node_from.id, edge.node_to.id] and \
                        self.node_to.id in [edge.node_from.id, edge.node_to.id]:
                        return True
                    else:
                        return False

            else:
                return False

        else:
            error(f'Cannot compare edge with object of type {type(edge).__name__}')

    @type_checker()
    def _set_s(self):
        """
        PURPOSE:

         Set s for multigraphs, s is the index in repeated edges

        """
        self.s = self.node_from.adjacent_nodes.count(self.node_to) + 1  # TODO wrong if s>2 because adjacent nodes returns unique nodes

    @type_checker()
    def _set_id(self):
        """
        PURPOSE:

         Set edge ID, connection is '-' for undirected edges and '->' for directed edges

        """
        connection = '->' if self.is_directed else '-'

        self.id = self.node_from.id + connection + self.node_to.id
        self.id_reversed = self.node_to.id + connection + self.node_from.id

    @type_checker((int, float))
    def _set_weight(self, weight):
        """
        PURPOSE:

         Set weight to edge

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         weight      int, float           Edge weight
        """
        self.weight = weight

    @type_checker()
    def reverse(self):
        """
        PURPOSE:

         Reverse edge direction, only for directed edges

        """
        if self.is_directed:

            # remove edge from node to/from
            if self.node_from.has_edge(self):
                self.node_from._remove_edge(self)
            else:
                self.node_to._remove_edge(self)

            # create reversed edge
            reversed_edge = Edge(self.node_to, self.node_from, weight=self.weight)

            # assign all attributes of reversed edge to self
            self.__dict__.update(reversed_edge.__dict__)  #

        else:
            warning(f'Method reverse() only make sense in directed graphs')

    def to_xml(self, f):
        """
        PURPOSE:

         Save edge as xml to import in https://graphonline.ru/en/

        MANDATORY ARGUMENTS:

         Parameter   Type                 Definition
         =========== ==================== ==========================================================================================
         f           handler              File handler to write to
        """
        # todo check edge weight
        f.write(f'\t\t<edge source="{self.node_from.id}" '
                f'target="{self.node_to.id}" '
                f'isDirect="{str(self.is_directed).lower()}" '
                f'weight="{str(self.weight)}" '
                f'useWeight="{str(self.has_weight).lower()}" '
                f'id="{self.id}" '
                f'text="" '
                f'upText="" '
                f'arrayStyleStart="" '
                f'arrayStyleFinish="" '
                f'model_width="{2*self.width}" '
                f'model_type="0" '
                f'model_curvedValue="0.1" ></edge>\n')
