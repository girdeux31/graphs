from drivers_gp import Digraph


structure = {'0': ['1', '2'],
             '1': ['2'],
             '2': []}

g1d = Digraph(structure)

g1d_node0 = g1d.get_node_by_id('0')
g1d_node1 = g1d.get_node_by_id('1')
g1d_node2 = g1d.get_node_by_id('2')

g1d_edge01 = g1d_node0.get_edge_by_id('0->1')
g1d_edge02 = g1d_node0.get_edge_by_id('0->2')
g1d_edge12 = g1d_node1.get_edge_by_id('1->2')
