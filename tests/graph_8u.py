from drivers_gp import Undigraph

# https://youtu.be/LcL-tO2TMlY?t=277

structure = {'1': ['2', '5'],
             '2': ['1', '3', '4', '5'],
             '3': ['2', '4', '6'],
             '4': ['2', '3', '5', '6'],
             '5': ['1', '2', '4'],
             '6': ['3', '4']}

g8u = Undigraph(structure)

g8u_node1 = g8u.get_node_by_id('1')
g8u_node2 = g8u.get_node_by_id('2')
g8u_node3 = g8u.get_node_by_id('3')
g8u_node4 = g8u.get_node_by_id('4')
g8u_node5 = g8u.get_node_by_id('5')
g8u_node6 = g8u.get_node_by_id('6')

g8u_edge12 = g8u_node1.get_edge_by_id('1-2')
g8u_edge15 = g8u_node1.get_edge_by_id('1-5')
g8u_edge23 = g8u_node2.get_edge_by_id('2-3')
g8u_edge24 = g8u_node2.get_edge_by_id('2-4')
g8u_edge25 = g8u_node2.get_edge_by_id('2-5')
g8u_edge34 = g8u_node3.get_edge_by_id('3-4')
g8u_edge36 = g8u_node3.get_edge_by_id('3-6')
g8u_edge45 = g8u_node4.get_edge_by_id('4-5')
g8u_edge46 = g8u_node4.get_edge_by_id('4-6')
