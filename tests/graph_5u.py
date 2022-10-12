from drivers_gp import Undigraph


structure = {'1': ['4'],
             '2': ['4'],
             '3': ['4'],
             '4': ['1', '2', '3', '5'],
             '5': ['4', '6'],
             '6': ['5']}

g5u = Undigraph(structure)

g5u_node1 = g5u.get_node_by_id('1')
g5u_node2 = g5u.get_node_by_id('2')
g5u_node3 = g5u.get_node_by_id('3')
g5u_node4 = g5u.get_node_by_id('4')
g5u_node5 = g5u.get_node_by_id('5')
g5u_node6 = g5u.get_node_by_id('6')

g5u_edge14 = g5u_node1.get_edge_by_id('1-4')
g5u_edge24 = g5u_node2.get_edge_by_id('2-4')
g5u_edge34 = g5u_node3.get_edge_by_id('3-4')
g5u_edge45 = g5u_node4.get_edge_by_id('4-5')
g5u_edge56 = g5u_node5.get_edge_by_id('5-6')
