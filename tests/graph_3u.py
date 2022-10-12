from drivers_gp import Undigraph


structure = {'1': ['2', '3'],
             '2': ['1', '3'],
             '3': ['1', '2']}

g3u = Undigraph(structure)

g3u_node1 = g3u.get_node_by_id('1')
g3u_node2 = g3u.get_node_by_id('2')
g3u_node3 = g3u.get_node_by_id('3')

g3u_edge12 = g3u_node1.get_edge_by_id('1-2')
g3u_edge13 = g3u_node1.get_edge_by_id('1-3')
g3u_edge23 = g3u_node2.get_edge_by_id('2-3')
