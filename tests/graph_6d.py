from drivers_gp import Digraph

# https://www.youtube.com/watch?v=kUy4L1P49jA&list=PL200623BEA27C775F&index=13

structure = {'5': ['4', '2', '1'],
             '4': ['8'],
             '2': [],
             '1': ['6'],
             '8': ['3'],
             '6': [],
             '3': []}

g6d = Digraph(structure)

g6d_node1 = g6d.get_node_by_id('1')
g6d_node2 = g6d.get_node_by_id('2')
g6d_node3 = g6d.get_node_by_id('3')
g6d_node4 = g6d.get_node_by_id('4')
g6d_node5 = g6d.get_node_by_id('5')
g6d_node6 = g6d.get_node_by_id('6')
g6d_node8 = g6d.get_node_by_id('8')

g6d_edge54 = g6d_node5.get_edge_by_id('5->4')
g6d_edge52 = g6d_node5.get_edge_by_id('5->2')
g6d_edge51 = g6d_node5.get_edge_by_id('5->1')
g6d_edge48 = g6d_node4.get_edge_by_id('4->8')
g6d_edge16 = g6d_node1.get_edge_by_id('1->6')
g6d_edge83 = g6d_node8.get_edge_by_id('8->3')
