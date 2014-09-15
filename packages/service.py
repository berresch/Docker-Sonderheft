from .docker_client import DockerClient

class Service(object):

  def __init__(self, name, config):
      self.name = name
      self.config = config
      self.client = DockerClient()

  def __repr__(self):
      return '<Service: %s>' % self.name

  def name(self):
      return self.name

  def version(self):
      return str(self.config['version'])

  def dockerfile(self):
      return self.config['build']['dockerfile']

  def build(self):
      self.client.build(self.dockerfile(), 'centerdevice/%s' % self.name, self.version())

  def rmi(self):
      self.client.rmi("centerdevice/%s" % self.name)

  def run(self):
      if self.config.has_key("runtime"):
          ip = self.config["runtime"]["ip"]
          self.client.run("centerdevice/%s" % self.name, self.name, ip=ip)
