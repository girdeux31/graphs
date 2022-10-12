from drivers_gp import Digraph, Undigraph


structure_a = {'A': ['B', 'C', 'E'],
               'B': ['A', 'D'],
               'C': ['A', 'D', 'E'],
               'D': ['B', 'C', 'E'],
               'E': ['A', 'C', 'D']}

g10a_u = Undigraph(structure_a)

g10a_u.apply_ore_theorem()