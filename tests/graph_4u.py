from drivers_gp import Undigraph


structure = {'U1': ['V1', 'V4'],
             'U2': ['V3'],
             'U3': ['V1', 'V2'],
             'U4': ['V3', 'V4'],
             'U5': ['V4'],
             'V1': ['U1', 'U3'],
             'V2': ['U3'],
             'V3': ['U2', 'U4'],
             'V4': ['U1', 'U4', 'U5']}

g4u = Undigraph(structure)

g4u_nodeU1 = g4u.get_node_by_id('U1')
g4u_nodeU2 = g4u.get_node_by_id('U2')
g4u_nodeU3 = g4u.get_node_by_id('U3')
g4u_nodeU4 = g4u.get_node_by_id('U4')
g4u_nodeU5 = g4u.get_node_by_id('U5')
g4u_nodeV1 = g4u.get_node_by_id('V1')
g4u_nodeV2 = g4u.get_node_by_id('V2')
g4u_nodeV3 = g4u.get_node_by_id('V3')
g4u_nodeV4 = g4u.get_node_by_id('V4')

g4u_edgeU1V1 = g4u_nodeU1.get_edge_by_id('U1-V1')
g4u_edgeU1V4 = g4u_nodeU1.get_edge_by_id('U1-V4')
g4u_edgeU2V3 = g4u_nodeU2.get_edge_by_id('U2-V3')
g4u_edgeU3V1 = g4u_nodeU3.get_edge_by_id('U3-V1')
g4u_edgeU3V2 = g4u_nodeU3.get_edge_by_id('U3-V2')
g4u_edgeU4V3 = g4u_nodeU4.get_edge_by_id('U4-V3')
g4u_edgeU4V4 = g4u_nodeU4.get_edge_by_id('U4-V4')
g4u_edgeU5V4 = g4u_nodeU5.get_edge_by_id('U5-V4')
