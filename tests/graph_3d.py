from drivers_gp import Digraph


structure = {'1': ['4', '6'],
             '2': ['1', '3'],
             '3': ['4'],
             '4': ['2', '5', '8'],
             '5': ['8'],
             '6': ['7'],
             '7': ['5'],
             '8': ['7']}

g3d = Digraph(structure)

g3d_node1 = g3d.get_node_by_id('1')
g3d_node2 = g3d.get_node_by_id('2')
g3d_node3 = g3d.get_node_by_id('3')
g3d_node4 = g3d.get_node_by_id('4')
g3d_node5 = g3d.get_node_by_id('5')
g3d_node6 = g3d.get_node_by_id('6')
g3d_node7 = g3d.get_node_by_id('7')
g3d_node8 = g3d.get_node_by_id('8')

g3d_edge14 = g3d_node1.get_edge_by_id('1->4')
g3d_edge16 = g3d_node1.get_edge_by_id('1->6')
g3d_edge21 = g3d_node2.get_edge_by_id('2->1')
g3d_edge23 = g3d_node2.get_edge_by_id('2->3')
g3d_edge34 = g3d_node3.get_edge_by_id('3->4')
g3d_edge42 = g3d_node4.get_edge_by_id('4->2')
g3d_edge45 = g3d_node4.get_edge_by_id('4->5')
g3d_edge48 = g3d_node4.get_edge_by_id('4->8')
g3d_edge58 = g3d_node5.get_edge_by_id('5->8')
g3d_edge67 = g3d_node6.get_edge_by_id('6->7')
g3d_edge75 = g3d_node7.get_edge_by_id('7->5')
g3d_edge87 = g3d_node8.get_edge_by_id('8->7')
