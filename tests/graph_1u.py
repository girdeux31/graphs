from drivers_gp import Undigraph


structure = {'0': ['0', '1', '2', '3'],
             '1': ['0', '2', 'A'],
             '2': ['0', '1'],
             '3': ['0'],
             'A': ['1']}

g1u = Undigraph(structure)

g1u_node0 = g1u.get_node_by_id('0')
g1u_node1 = g1u.get_node_by_id('1')
g1u_node2 = g1u.get_node_by_id('2')
g1u_node3 = g1u.get_node_by_id('3')
g1u_nodeA = g1u.get_node_by_id('A')

g1u_edge00 = g1u_node0.get_edge_by_id('0-0')
g1u_edge01 = g1u_node0.get_edge_by_id('0-1')
g1u_edge02 = g1u_node0.get_edge_by_id('0-2')
g1u_edge03 = g1u_node0.get_edge_by_id('0-3')
g1u_edge10 = g1u_node1.get_edge_by_id('1-0')
g1u_edge12 = g1u_node1.get_edge_by_id('1-2')
g1u_edge1A = g1u_node1.get_edge_by_id('1-A')
