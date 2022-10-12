import os
import copy
import pytest

from tests import *


def test_graph_is_simple():

    assert not g1u.is_simple

    assert g1d.is_simple
    assert not g2d.is_simple

def test_graph_is_comple():

    assert not g1u.is_complete
    assert g3u.is_complete

def test_graph_is_regular():

    assert g3u.is_regular
    assert not g4u.is_regular

def test_graph_is_k_regular():

    assert g3u.is_k_regular(2)
    assert not g3u.is_k_regular(3)

def test_graph_is_bipartite():

    assert g4u.is_bipartite
    assert not g2u.is_bipartite

def test_graph_is_walk():

    assert g2u.is_walk(['1', '2', '3', '4', '3'])
    assert not g2u.is_walk(['1', '2', '5', '4', '3'])

def test_graph_is_close_walk():

    assert g2u.is_closed_walk(['1', '2', '3', '2', '1'])
    assert not g2u.is_closed_walk(['1', '2', '3', '4', '3'])

def test_graph_is_trail():

    assert g2u.is_trail(['1', '2', '3', '4'])
    assert not g2u.is_trail(['1', '2', '3', '4', '3'])

def test_graph_is_circuit():

    assert g1u.is_circuit(['0', '1', '2', '0'])

def test_graph_is_tree():

    assert not g3u.is_tree
    assert g5u.is_tree
    assert not g3d.is_tree
    assert g5d.is_tree

def test_graph_is_path():

    assert g1u.is_path(['0', '1', '2'])
    assert not g1u.is_path(['0', '1', '2', '0'])

def test_graph_is_cycle():

    assert g1u.is_cycle(['0', '1', '2', '0'])

def test_graph_is_connected():

    assert not g2u.is_connected
    assert g1u.is_connected

def test_graph_is_cut_node():

    assert g2u_node7.is_cut_node
    assert not g2u_node4.is_cut_node

def test_graph_get_node_by_id():

    assert g1u.get_node_by_id('A').id == 'A'

def test_graph_get_bipartite_components():

    assert g4u.get_bipartite_components() == ({'U1', 'U2', 'U3', 'U4', 'U5'}, {'V1', 'V2', 'V3', 'V4'})

def test_graph_has_node():

    assert g1u.has_node(g1u_nodeA)
    assert not g1u.has_node(g1d_node0)

def test_graph_has_node_by_id():

    assert g1u.has_node_by_id(g1u_nodeA.id)
    assert g1u.has_node_by_id(g1d_node0.id)  # watch out directed

def test_graph_has_cycle():

    assert g1u.has_cycle
    assert g2u.has_cycle

    assert not g1d.has_cycle
    assert not g2d.has_cycle

def test_undigraph_adjacency_matrix():

    assert g1u.adjacency_matrix == [[1, 1, 1, 1, 0],
                                    [1, 0, 1, 0, 1],
                                    [1, 1, 0, 0, 0],
                                    [1, 0, 0, 0, 0],
                                    [0, 1, 0, 0, 0]]

    assert g4u.adjacency_matrix == [[0, 0, 0, 0, 0, 1, 0, 0, 1],
                                    [0, 0, 0, 0, 0, 0, 0, 1, 0],
                                    [0, 0, 0, 0, 0, 1, 1, 0, 0],
                                    [0, 0, 0, 0, 0, 0, 0, 1, 1],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 1],
                                    [1, 0, 1, 0, 0, 0, 0, 0, 0],
                                    [0, 0, 1, 0, 0, 0, 0, 0, 0],
                                    [0, 1, 0, 1, 0, 0, 0, 0, 0],
                                    [1, 0, 0, 1, 1, 0, 0, 0, 0]]

def test_digraph_adjacency_matrix():

    assert g1d.adjacency_matrix == [[0, 1, 1],
                                    [0, 0, 1],
                                    [0, 0, 0]]

def test_undigraph_adjacency_function():
    assert sorted(g1u.adjacency_function('1', power=+1)) == ['0', '2', 'A']
    assert sorted(g1u.adjacency_function('1', power=-1)) == ['0', '2', 'A']
    assert sorted(g1u.adjacency_function('A', power=+2)) == ['0', '2', 'A']
    assert sorted(g1u.adjacency_function('A', power=-2)) == ['0', '2', 'A']
    assert sorted(g1u.adjacency_function('A', power=+3)) == ['0', '1', '2', '3']

def test_digraph_adjacency_function():
    assert sorted(g1d.adjacency_function('1', power=+1)) == ['2']
    assert sorted(g1d.adjacency_function('1', power=-1)) == ['0']
    assert sorted(g1d.adjacency_function('1', power=+2)) == []
    assert sorted(g1d.adjacency_function('1', power=-2)) == []
    assert sorted(g2d.adjacency_function('4', power=+3)) == ['1', '3', '4']
    assert sorted(g2d.adjacency_function('1', power=+1)) == ['1', '4']
    assert sorted(g2d.adjacency_function('1', power=+1, _skip_loops=True, _skip_bilaterals=True)) == []
    assert sorted(g2d.adjacency_function('1', power=-1, _skip_loops=True, _skip_bilaterals=True)) == ['2']


def test_graph_connected_components():

    assert sorted(g2u.connected_components) == [('1', '2', '3', '4'), ('5',), ('6', '7', '8')]

def test_graph_cut_nodes():

    assert sorted(g2u.cut_nodes) == ['2', '7']

def test_graph_cut_edges():

    assert sorted(g2u.cut_edges) == ['1-2', '6-7', '7-8']

def test_graph_chromatic_number():

    assert g3u.chromatic_number == 3
    assert g4u.chromatic_number == 4

def test_graph_is_strongly_connected():

    assert not g3d.is_strongly_connected

def test_graph_is_weakly_connected():

    assert g3d.is_weakly_connected

def test_graph_strong_connected_components():

    assert sorted(g3d._strong_connected_component_of('1')) == ['1', '2', '3', '4']
    assert sorted(g3d.strong_connected_components) == [('1', '2', '3', '4'), ('5', '7', '8'), ('6',)]

def test_graph_get_undigraph():

    graph = g3d.get_undigraph()

    assert graph.get_node_by_id('7').has_edge_by_id('7-8')
    assert graph.get_node_by_id('4').has_edge_by_id('4-3')
    assert graph.get_node_by_id('1').has_edge_by_id('1-6')

def test_graph_get_complementary_graph():

    graph = g1u.get_complementary_graph()

    assert graph.get_node_by_id('1').has_edge_by_id('1-3')
    assert graph.get_node_by_id('A').has_edge_by_id('A-3')
    assert not graph.get_node_by_id('A').has_edge_by_id('A-1')
    assert not graph.get_node_by_id('3').has_edge_by_id('3-0')

def test_graph_remove_node():

    graph = copy.deepcopy(g1u)
    graph.remove_node('1')

    assert not graph.has_node_by_id('1')

def test_graph_remove_edge():

    graph = copy.deepcopy(g1u)
    graph.remove_edge('1-0')

    assert not graph.get_node_by_id('1').has_edge_by_id('1-0')

def test_graph_remove_all_edges():

    graph = copy.deepcopy(g1u)
    graph.remove_all_edges()

    assert graph.is_k_regular(0)

def test_undigraph_save():

    path = 'img'
    name = 'undigraph.jpg'
    file = os.path.join(path, name)

    if not os.path.isdir(path):
        os.mkdir(path)

    if os.path.isfile(file):
        os.remove(file)

    g1u.save(file)

    assert os.path.isfile(file)

def test_digraph_save():

    path = 'img'
    name = 'digraph.jpg'
    file = os.path.join(path, name)

    if not os.path.isdir(path):
        os.mkdir(path)

    if os.path.isfile(file):
        os.remove(file)

    g1d.save(file)

    assert os.path.isfile(file)

def test_undigraph_to_xml():
    path = 'img'
    name = 'undigraph.graphtml'
    file = os.path.join(path, name)

    if not os.path.isdir(path):
        os.mkdir(path)

    if os.path.isfile(file):
        os.remove(file)

    g1u.to_xml(file)

    assert os.path.isfile(file)

def test_digraph_to_xml():
    path = 'img'
    name = 'digraph.graphtml'
    file = os.path.join(path, name)

    if not os.path.isdir(path):
        os.mkdir(path)

    if os.path.isfile(file):
        os.remove(file)

    g1d.to_xml(file)

    assert os.path.isfile(file)

def test_graph_get_minimum_weight_but_grater_than():

    assert g6u._get_minimum_weight_but_grater_than(3.5) == 4

def test_graph_get_maximum_weight_but_smaller_than():

    assert g6u._get_maximum_weight_but_smaller_than(3.5) == 3

def test_graph_get_edges_with_minimum_weight():

    assert sorted([edge.id for edge in g6u._get_edges_with_minimum_weight()]) == ['b-d']
    assert sorted([edge.weight for edge in g6u._get_edges_with_minimum_weight()]) == [1]

def test_graph_get_edges_with_maximum_weight():

    assert sorted([edge.id for edge in g6u._get_edges_with_maximum_weight()]) == ['b-c']
    assert sorted([edge.weight for edge in g6u._get_edges_with_maximum_weight()]) == [7]

def test_graph_get_minimum_spanning_tree():

    graph, weight = g6u.get_minimum_spanning_tree()

    assert weight == 13
    assert not graph.get_node_by_id('b').has_edge_by_id('b-c')
    assert graph.get_node_by_id('e').has_edge_by_id('b-e')

def test_graph_get_maximum_spanning_tree():

    graph, weight = g6u.get_maximum_spanning_tree()

    assert weight == 24
    assert not graph.get_node_by_id('a').has_edge_by_id('a-d')
    assert graph.get_node_by_id('c').has_edge_by_id('c-b')
    assert graph.get_node_by_id('c').has_edge_by_id('c-d')
    assert graph.get_node_by_id('c').has_edge_by_id('c-e')
    assert graph.get_node_by_id('a').has_edge_by_id('a-b')

def test_graph_is_rooted_tree():

    assert g6d.is_rooted_tree

def test_undigraph_is_eulerian():

    assert not g7u.is_eulerian

def test_undigraph_has_eulerian_trail():

    assert g7u.has_eulerian_trail

def test_undigraph_get_extremes_of_eulerian_trail():

    node_id_0, node_id_1 = g7u.get_extremes_of_eulerian_trail()

    assert node_id_0 == 'll'
    assert node_id_1 == 'lr'

def test_digraph_is_eulerian():

    assert not g7d.is_eulerian

def test_digraph_has_eulerian_trail():

    assert g7d.has_eulerian_trail

def test_digraph_get_extremes_of_eulerian_trail():

    node_id_0, node_id_1 = g7d.get_extremes_of_eulerian_trail()

    assert node_id_0 == '1'
    assert node_id_1 == '2'

def test_undigraph_get_closure():

    graph = g8u.get_closure()

    assert all([node.degree == len(graph.nodes)-1 for node in graph.nodes])

def test_undigraph_dirac_theorem():

    assert g9a_u.apply_dirac_theorem()
    assert not g9b_u.apply_dirac_theorem()
    assert not g9c_u.apply_dirac_theorem()

def test_undigraph_ore_theorem():

    assert g10a_u.apply_ore_theorem()
    assert not g10b_u.apply_ore_theorem()

def test_graph_error_1():

    with pytest.raises(Exception) as e_info:
        g5u._get_edges_with_weight(2)

    assert e_info.value.args[0] == 'Fatal error'

def test_graph_error_2():

    with pytest.raises(Exception) as e_info:
        g2u.is_walk(['1'])

    assert e_info.value.args[0] == 'Fatal error'

def test_graph_error_3():

    with pytest.raises(Exception) as e_info:
        structure = {'a': ['b'], 'b': ['a']}
        weights = {'a-b': 5, 'a-z': 5}
        Undigraph(structure, weights=weights)

    assert e_info.value.args[0] == 'Fatal error'

def test_graph_error_4():

    with pytest.raises(Exception) as e_info:
        structure = {'a': ['z'], 'b': ['a']}
        Undigraph(structure)

    assert e_info.value.args[0] == 'Fatal error'

def test_graph_error_5():

    with pytest.raises(Exception) as e_info:
        structure = {'a': ['b'], 'b': []}
        Undigraph(structure)

    assert e_info.value.args[0] == 'Fatal error'

def test_graph_error_6():

    with pytest.raises(Exception) as e_info:
        structure = {'a': ['b', 'b'], 'b': ['a']}
        Undigraph(structure)

    assert e_info.value.args[0] == 'Fatal error'
