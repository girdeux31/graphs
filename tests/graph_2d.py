from drivers_gp import Digraph


structure = {'1': ['1', '4'],
             '2': ['1', '3', '4'],
             '3': [],
             '4': ['1', '3']}

g2d = Digraph(structure)

g2d_node1 = g2d.get_node_by_id('1')
g2d_node2 = g2d.get_node_by_id('2')
g2d_node3 = g2d.get_node_by_id('3')
g2d_node4 = g2d.get_node_by_id('4')

g2d_edge11 = g2d_node1.get_edge_by_id('1->1')
g2d_edge14 = g2d_node1.get_edge_by_id('1->4')
g2d_edge21 = g2d_node2.get_edge_by_id('2->1')
g2d_edge23 = g2d_node2.get_edge_by_id('2->3')
g2d_edge24 = g2d_node2.get_edge_by_id('2->4')
g2d_edge41 = g2d_node4.get_edge_by_id('4->1')
g2d_edge43 = g2d_node4.get_edge_by_id('4->3')
