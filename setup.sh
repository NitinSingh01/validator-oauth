#! /bin/sh


#First we retrieves information about what packages can be installed, including what updates to currently installed packages packages are available, from Internet sources
sudo apt-get update &&
#Use the following command to install pip for Python. We require this to install swagger-py-codegen 
sudo apt-get install python-pip -y &&
#Now we will Swagger Py Codegen which is a Python web framework generator, which can help you generate a Python web framework automatically based on a given Swagger Specification doc.
sudo pip install swagger-py-codegen &&
#Make sure you have the necessary packages to allow the use of Docker’s repository
sudo apt install apt-transport-https ca-certificates curl software-properties-common  -y &&
#Add Docker’s GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -  &&
#Add the stable Docker repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"  &&
#Update your package index and install Docker CE
sudo apt update &&
curl -O https://download.docker.com/linux/debian/dists/buster/pool/stable/amd64/containerd.io_1.4.3-1_amd64.deb  &&
sudo apt install ./containerd.io_1.4.3-1_amd64.deb  &&
sudo apt install docker-ce  -y  &&
sudo curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose  &&
sudo chmod +x /usr/local/bin/docker-compose  &&
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
#now we are done with installation and we will write a welcome message
echo "Welcome Master we are all set to begin this journey !!!"
