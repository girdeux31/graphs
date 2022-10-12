from drivers_gp import Undigraph

# https://youtu.be/IIcwc09PmXU?t=129

structure_a = {'A': ['B', 'C', 'E'],
               'B': ['A', 'D'],
               'C': ['A', 'D', 'E'],
               'D': ['B', 'C', 'E'],
               'E': ['A', 'C', 'D']}

g10a_u = Undigraph(structure_a)

# https://youtu.be/IIcwc09PmXU?t=215

structure_b = {'A': ['B', 'C'],
               'B': ['A', 'D'],
               'C': ['A', 'E'],
               'D': ['B', 'E'],
               'E': ['C', 'D']}

g10b_u = Undigraph(structure_b)