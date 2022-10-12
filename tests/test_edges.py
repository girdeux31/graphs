import pytest

from tests import *
import drivers_gp

def test_edge_initialize():

    edge = drivers_gp.Edge(g1u_nodeA, g1u_node1)

    assert edge.id == 'A-1'

def test_edge_equality():

    assert not (g1u_edge01 == g1u_edge12)
    assert (g1u_edge01 == g1u_edge01)
    assert (g1u_edge01 == g1u_edge10)

    assert not (g1d_edge01 == g1d_edge12)
    assert (g1d_edge01 == g1d_edge01)

def test_edge_is_loop():

    assert g1u_edge00.is_loop

def test_edge_is_cut_edge():

    assert g2u_edge12.is_cut_edge
    assert not g2u_edge23.is_cut_edge

def test_edge_is_bridge():

    assert g2u_edge12.is_bridge

def test_edge_reverse():

    assert g1d_node0.has_edge_by_id('0->1')
    assert not g1d_node1.has_edge_by_id('1->0')

    g1d_edge01.reverse()
    assert not g1d_node0.has_edge_by_id('0->1')
    assert g1d_node1.has_edge_by_id('1->0')

    g1d_edge01.reverse()
    assert g1d_node0.has_edge_by_id('0->1')
    assert not g1d_node1.has_edge_by_id('1->0')

def test_edge_error_1():

    with pytest.raises(Exception) as e_info:
        drivers_gp.Edge('dummy', g1u_node1)

    assert e_info.value.args[0] == 'Fatal error'

    with pytest.raises(Exception) as e_info:
        drivers_gp.Edge(g1u_node0, 'dummy')

    assert e_info.value.args[0] == 'Fatal error'

def test_edge_error_2():

    with pytest.raises(Exception) as e_info:
        g1u_edge01 == 'dummy'

    assert e_info.value.args[0] == 'Fatal error'

    with pytest.raises(Exception) as e_info:
        'dummy' == g1u_edge12

    assert e_info.value.args[0] == 'Fatal error'

if __name__ == '__main__':

    print(g1d_edge01)
    print(g1d_edge01.node_from)
    print(g1d_edge01.node_to)
    g1d_edge01.reverse()
    print(g1d_edge01)
    print(g1d_edge01.node_from)
    print(g1d_edge01.node_to)
    g1d_edge01.reverse()
    print(g1d_edge01)
    print(g1d_edge01.node_from)
    print(g1d_edge01.node_to)