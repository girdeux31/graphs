import copy
import pytest

from tests import *
import drivers_gp


def test_node_initialize():

    node = drivers_gp.Node(g1u, '1')

    assert node.id == '1'

def test_node_equality():

    node = copy.deepcopy(g1u_node0)

    assert (g1u_node0 == g1u_node0)
    assert not (g1u_node0 == g1u_node1)
    assert (g1u_node0 == node)

def test_node_is_strongly_connected_with():

    assert g3d_node1.is_strongly_connected_with('3')
    assert not g3d_node1.is_strongly_connected_with('6')
    assert g3d_node6.is_strongly_connected_with('6')

def test_node_has_adjacent_node():

    assert g2u_node4.has_adjacent_node(g2u_node3)
    assert not g2u_node4.has_adjacent_node(g2u_node1)
    assert g2d_node1.has_adjacent_node(g2d_node4)
    assert not g2d_node1.has_adjacent_node(g2d_node2)

def test_node_has_edge():

    assert g1u_nodeA.has_edge(g1u_edge1A)
    assert g1u_node1.has_edge(g1u_edge1A)
    assert not g1u_node0.has_edge(g1d_edge01)

def test_node_has_edge_by_id():

    assert g1u_nodeA.has_edge_by_id('1-A')
    assert g1u_nodeA.has_edge_by_id('A-1')
    assert g1u_node1.has_edge_by_id('1-A')
    assert g1u_node1.has_edge_by_id('A-1')
    assert not g1u_node2.has_edge_by_id('2-3')

def test_node_has_edge_with_node():

    assert g1u_node1.has_edge_with_node(g1u_nodeA)
    assert g1u_nodeA.has_edge_with_node(g1u_node1)
    assert not g1u_node2.has_edge_with_node(g1u_node3)

    assert g1d_node0.has_edge_with_node(g1d_node1)
    assert not g1d_node1.has_edge_with_node(g1d_node0)

def test_node_has_loop():

    assert g1u_node0.has_loop
    assert not g1u_node1.has_loop

def test_node_has_bilateral_connection():

    assert g2d_node1.has_bilateral_connection

def test_node_get_edge_by_id():

    assert g1u_node1.get_edge_by_id('1-A').id == '1-A'

def test_node_get_edge_with_node():

    assert g2u_node4.get_edge_with_node(g2u_node3).id == '3-4'
    assert g2d_node1.get_edge_with_node(g2d_node4).id == '1->4'
    assert g2d_node4.get_edge_with_node(g2d_node1).id == '4->1'
    assert g2d_node2.get_edge_with_node(g2d_node3).id == '2->3'

def test_node_is_bilateraly_connected_with():

    assert g2d_node1.is_bilateraly_connected_with('4')
    assert not g2d_node1.is_bilateraly_connected_with('2')
    assert not g2d_node1.is_bilateraly_connected_with('1')
    assert not g2d_node1.is_bilateraly_connected_with('3')

def test_node_degree():

    assert g1u_node0.degree == 5

def test_node_indegree():

    assert g1d_node0.indegree == 0
    assert g7d_node_1.indegree == 2

def test_node_outdegree():

    assert g1d_node0.outdegree == 2
    assert g7d_node_2.outdegree == 3

def test_node_error_1():

    with pytest.raises(Exception) as e_info:
        drivers_gp.Node('dummy', 'dummy')

    assert e_info.value.args[0] == 'Fatal error'

def test_node_error_2():

    with pytest.raises(Exception) as e_info:
        g1u_node0 == 'dummy'

    assert e_info.value.args[0] == 'Fatal error'

    with pytest.raises(Exception) as e_info:
        'dummy' == g1u_node0

    assert e_info.value.args[0] == 'Fatal error'

def test_node_error_3():

    with pytest.raises(Exception) as e_info:
        g1u_node0.add_edge('dummy')

    assert e_info.value.args[0] == 'Fatal error'

def test_node_error_7():

    with pytest.raises(Exception) as e_info:
        g1u_node0._remove_edge('dummy')

    assert e_info.value.args[0] == 'Fatal error'

    with pytest.raises(Exception) as e_info:
        g1u_node0._remove_edge(g1u_edge1A)

    assert e_info.value.args[0] == 'Fatal error'

def test_node_error_9():

    with pytest.raises(Exception) as e_info:
        g1u_node0.has_adjacent_node('dummy')

    assert e_info.value.args[0] == 'Fatal error'

def test_node_error_10():

    with pytest.raises(Exception) as e_info:
        g1u_node0.outdegree

    assert e_info.value.args[0] == 'Fatal error'

    with pytest.raises(Exception) as e_info:
        g1u_node0.indegree

    assert e_info.value.args[0] == 'Fatal error'

    with pytest.raises(Exception) as e_info:
        g1d_node0.degree

    assert e_info.value.args[0] == 'Fatal error'

def test_node_error_11():

    with pytest.raises(Exception) as e_info:
        g1u_node1.get_edge_with_node(g1u_node3)

    assert e_info.value.args[0] == 'Fatal error'
