from drivers_gp import Undigraph

# https://youtu.be/OGh5JKso0y4?t=79

structure_a = {'A': ['B', 'C', 'D'],
               'B': ['A', 'C', 'D'],
               'C': ['A', 'B', 'D'],
               'D': ['A', 'B', 'C']}

g9a_u = Undigraph(structure_a)

# https://youtu.be/OGh5JKso0y4?t=119

structure_b = {'A': ['B', 'C', 'E'],
               'B': ['A', 'D', 'E'],
               'C': ['A', 'E'],
               'D': ['B', 'E'],
               'E': ['A', 'B', 'C', 'D']}

g9b_u = Undigraph(structure_b)

# https://youtu.be/OGh5JKso0y4?t=167

structure_c = {'A': ['B', 'C'],
               'B': ['A', 'D'],
               'C': ['A', 'E'],
               'D': ['B', 'H'],
               'E': ['C', 'F'],
               'F': ['E', 'G'],
               'G': ['F', 'H'],
               'H': ['G', 'D']}

g9c_u = Undigraph(structure_c)