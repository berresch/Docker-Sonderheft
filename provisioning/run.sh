#!/bin/bash

ln -s /vagrant/plumb /usr/local/bin/plumb

echo "Installing pip, pygraph, and docker-py"
apt-get install -y python-pygraph python-pip
pip install docker-py

echo "Installing pipework"
curl -LO https://raw.github.com/lukaspustina/pipework/master/pipework &> /dev/null
mv pipework /usr/local/bin/pipework
chmod +x /usr/local/bin/pipework

echo "Configuring docker"
cp -v /vagrant/provisioning/rc.local /etc/rc.local
cp -v /vagrant/provisioning/docker /etc/default/docker
