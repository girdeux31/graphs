from drivers_gp import Undigraph

# https://youtu.be/GYknoMYjxBE?t=141

structure = {'ll': ['lr', 'ul', 'ur'],
             'lr': ['ll', 'ul', 'ur'],
             'ul': ['ll', 'lr', 'ur', 'uu'],
             'ur': ['ll', 'lr', 'ul', 'uu'],
             'uu': ['ul', 'ur']}

g7u = Undigraph(structure)

g7u_node_ll = g7u.get_node_by_id('ll')
g7u_node_lr = g7u.get_node_by_id('lr')
g7u_node_ul = g7u.get_node_by_id('ul')
g7u_node_ur = g7u.get_node_by_id('ur')
g7u_node_uu = g7u.get_node_by_id('uu')

g7u_edge_ll_lr = g7u_node_ll.get_edge_by_id('ll-lr')
g7u_edge_ll_ul = g7u_node_ll.get_edge_by_id('ll-ul')
g7u_edge_ll_ur = g7u_node_ll.get_edge_by_id('ll-ur')
g7u_edge_lr_ur = g7u_node_lr.get_edge_by_id('lr-ur')
g7u_edge_lr_ul = g7u_node_lr.get_edge_by_id('lr-ul')
g7u_edge_ul_ur = g7u_node_ul.get_edge_by_id('ul-ur')
g7u_edge_ul_uu = g7u_node_ul.get_edge_by_id('ul-uu')
g7u_edge_ur_uu = g7u_node_ur.get_edge_by_id('ur-uu')
