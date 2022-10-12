from drivers_gp import Undigraph


structure = {'1': ['1', '2'],
             '2': ['1', '3', '4'],
             '3': ['2', '4'],
             '4': ['2', '3'],
             '5': [],
             '6': ['7'],
             '7': ['6', '8'],
             '8': ['7']}

g2u = Undigraph(structure)

g2u_node1 = g2u.get_node_by_id('1')
g2u_node2 = g2u.get_node_by_id('2')
g2u_node3 = g2u.get_node_by_id('3')
g2u_node4 = g2u.get_node_by_id('4')
g2u_node5 = g2u.get_node_by_id('5')
g2u_node6 = g2u.get_node_by_id('6')
g2u_node7 = g2u.get_node_by_id('7')
g2u_node8 = g2u.get_node_by_id('8')

g2u_edge11 = g2u_node1.get_edge_by_id('1-1')
g2u_edge12 = g2u_node1.get_edge_by_id('1-2')
g2u_edge23 = g2u_node2.get_edge_by_id('2-3')
g2u_edge24 = g2u_node2.get_edge_by_id('2-4')
g2u_edge34 = g2u_node3.get_edge_by_id('3-4')
g2u_edge67 = g2u_node6.get_edge_by_id('6-7')
g2u_edge78 = g2u_node7.get_edge_by_id('7-8')
