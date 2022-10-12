from drivers_gp import Digraph

# https://youtu.be/GYknoMYjxBE?t=473

structure = {'1': ['3'],
             '2': ['1', '1', '4'],
             '3': ['2', '4'],
             '4': ['2', '3']}

g7d = Digraph(structure)

g7d_node_1 = g7d.get_node_by_id('1')
g7d_node_2 = g7d.get_node_by_id('2')
g7d_node_3 = g7d.get_node_by_id('3')
g7d_node_4 = g7d.get_node_by_id('4')

g7d_edge_13 = g7d_node_1.get_edge_by_id('1->3')
g7d_edge_21 = g7d_node_2.get_edge_by_id('2->1', s=1)
g7d_edge_21b = g7d_node_2.get_edge_by_id('2->1', s=2)
g7d_edge_24 = g7d_node_2.get_edge_by_id('2->4')
g7d_edge_32 = g7d_node_3.get_edge_by_id('3->2')
g7d_edge_34 = g7d_node_3.get_edge_by_id('3->4')
g7d_edge_42 = g7d_node_4.get_edge_by_id('4->2')
g7d_edge_43 = g7d_node_4.get_edge_by_id('4->3')
