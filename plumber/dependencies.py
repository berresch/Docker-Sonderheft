import sys
import re
import os.path

# https://code.google.com/p/python-graph/source/browse/trunk/core/pygraph/classes/digraph.py
from pygraph.classes.digraph import digraph
# https://code.google.com/p/python-graph/source/browse/trunk/core/pygraph/algorithms/searching.py
from pygraph.algorithms.searching import depth_first_search
# https://code.google.com/p/python-graph/source/browse/trunk/core/pygraph/algorithms/cycles.py
from pygraph.algorithms.cycles import find_cycle

from service import Service


DOMAIN = 'centerdevice/'


def build_graph(services, root=None):
    graph = digraph()

    for name, service in services.iteritems():
        dockerfile = "%s/Dockerfile" % service.dockerfile()

        if not os.path.isfile(dockerfile):
            sys.exit("%s does not exist" % dockerfile)

        baseimage = None
        with open(dockerfile, 'r') as file:
            for line in file:
                stripped = line.strip()
                if stripped.startswith('#'): continue

                if re.match("^\s*FROM\s+", stripped):
                    if baseimage: sys.exit("'%s' has more than 1 FROM instruction" % dockerfile)

                    tokens = stripped.split()
                    if len(tokens) < 2: sys.exit("'%s' has invalid FROM instruction" % dockerfile)

                    baseimage = tokens[1]

        _add_node_if_not_exists(graph, name)

        if baseimage.startswith(DOMAIN):
            parent = baseimage[len(DOMAIN):]
            _add_node_if_not_exists(graph, parent)
            graph.add_edge((parent, name))

    if root and not graph.has_node(root):
        sys.exit("Found no root in graph")

    cycles = find_cycle(graph)
    if cycles: sys.exit("Following services %s build a cycle. Please fix it!" % cycles)

    return _topological_sorting(graph, root)


def _add_node_if_not_exists(graph, node):
    if not graph.has_node(node):
        graph.add_node(node)


def _topological_sorting(graph, root):
    order = depth_first_search(graph, root=root)[2]
    order.reverse()
    return order
