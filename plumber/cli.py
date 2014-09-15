from __future__ import print_function

from docker_client import DockerClient
from dependencies import build_graph
from service import Service

import yaml
import sys

def main(argv):
    root = None
    if len(argv) > 0:
        root = argv[0]

    services = dict()
    config = yaml.safe_load(open('/vagrant/services/config.yml'))

    for name, config in list(config.items()):
        service = Service(name, config)
        services[name] = service

    graph = build_graph(services, root)

    for name in reversed(graph):
        service = services[name]
        print("REMOVE %s ..." % name)
        service.rmi()

    for name in graph:
        service = services[name]
        print("BUILD %s ..." % name)
        service.build()
        print("RUN %s ..." % name)
        service.run()
