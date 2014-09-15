from __future__ import print_function

import sys
import re
import json
import subprocess

import docker as api
from docker.errors import APIError

from progress_stream import stream_output, StreamOutputError


class DockerClient:

    def __init__(self):
        self.client = api.Client(base_url='unix://var/run/docker.sock', version='1.14', timeout=10)


    def ps(self, all=True):
        return self.client.containers(all=all)


    def rm(self, container):
        def cmd():
            output = self.client.remove_container(container, force=True)
            #print(output)

        self.ignore404(cmd)


    def rmi(self, image):
        def rm_containers(uid, repo_tags):
            containers = self.ps()
            for c in filter(lambda c: uid.startswith(c['Image']) or c['Image'] in repo_tags, containers):
                self.rm(c['Id'])

        info = self.inspect_image(image)
        if info:
            uid = info['Id']
            repo_tags = list()
            for i in self.client.images():
                if i['Id'] == uid:
                    repo_tags = i['RepoTags']
                if i['ParentId'] == uid:
                    sys.exit('Conflict, cannot remove image "%s" because it is a parent image.' % image)

            rm_containers(uid, repo_tags)
            for repo_tag in repo_tags:
                self.client.remove_image(repo_tag)


    def inspect_container(self, container):
        def cmd():
            return self.client.inspect_container(container)

        return self.ignore404(cmd)


    def inspect_image(self, image):
        def cmd():
            return self.client.inspect_image(image)

        return self.ignore404(cmd)


    def ip(self, container):
        info = inspect_container(container)
        return info['NetworkSettings']['IPAddress'] if info else None


    def pid(self, container):
        info = inspect_container(container)
        return info['State']['Pid'] if info else None


    def build(self, dockerfile, repository, tag):
        output = self.client.build(dockerfile, tag='%s:%s' % (repository, tag), stream=True, quiet=False, rm=True)

        try:
            events = stream_output(output, sys.stdout)
        except StreamOutputError, e:
            raise e

        image = None
        for event in events:
            if 'stream' in event:
                match = re.search(r'Successfully built ([0-9a-f]+)', event.get('stream', ''))
                if match:
                    image = match.group(1)

        if image is None:
            sys.exit('Could not build image %s' % repository)

        self.client.tag('%s:%s' % (repository, tag), repository, tag="latest")

        return image


    def run(self, image, name, ip=None, command=None, volumes=None, ports=None):
        def cmd():
            return self.client.create_container(image, detach=True, name=name, hostname=name, volumes=volumes, command=command)

        def set_ip(container):
            proc = subprocess.Popen(['sudo', 'pipework', 'docker0', container, '%s/16' % ip], stderr=subprocess.PIPE)
            stderr = proc.communicate()[1]
            if proc.returncode != 0:
                print("Could not set ip address because:\n%s" % stderr)

        created = self.ignore404(cmd)
        if created:
            container = created['Id']
            # 409 Conflict
            self.client.start(container, dns="8.8.8.8", port_bindings=ports)
            if ip:
              set_ip(container)
            return container


    def ignore404(self, cmd):
        try:
            return cmd()
        except APIError, e:
            if e.response.status_code == 404:
                print(e.explanation)
            else:
                raise
