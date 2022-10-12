from drivers_gp import Undigraph

# https://www.youtube.com/watch?v=JyFG_z7iMyo&ab_channel=JuanAntonioGomez

structure = {'a': ['b', 'd'],
             'b': ['a', 'd', 'c', 'e'],
             'c': ['b', 'd', 'e'],
             'd': ['a', 'b', 'c', 'e'],
             'e': ['b', 'c', 'd']}

weights = {'a-b': 5,
           'a-d': 4,
           'b-c': 7,
           'b-d': 1,
           'b-e': 2,
           'c-d': 6,
           'c-e': 6,
           'd-e': 3}

g6u = Undigraph(structure, weights=weights)

g6u_node_a = g6u.get_node_by_id('a')
g6u_node_b = g6u.get_node_by_id('b')
g6u_node_c = g6u.get_node_by_id('c')
g6u_node_d = g6u.get_node_by_id('d')
g6u_node_e = g6u.get_node_by_id('e')

g6u_edge_ab = g6u_node_a.get_edge_by_id('a-b')
g6u_edge_ad = g6u_node_a.get_edge_by_id('a-d')
g6u_edge_bc = g6u_node_b.get_edge_by_id('b-c')
g6u_edge_bd = g6u_node_b.get_edge_by_id('b-d')
g6u_edge_be = g6u_node_b.get_edge_by_id('b-e')
g6u_edge_cd = g6u_node_c.get_edge_by_id('c-d')
g6u_edge_ce = g6u_node_c.get_edge_by_id('c-e')
g6u_edge_de = g6u_node_d.get_edge_by_id('d-e')
