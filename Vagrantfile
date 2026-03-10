# set up the default terminal
ENV["TERM"]="linux"

# set minimum version for Vagrant
Vagrant.require_version ">= 2.2.10"
Vagrant.configure("2") do |config|
  config.vm.provision "shell", inline: <<-SHELL
    # Update and install dependencies
    zypper --non-interactive install curl apparmor-parser

    # Install k3s (Kubernetes)
    curl -sfL https://get.k3s.io | sh -
    
    # Allow the vagrant user to use kubectl without sudo
    mkdir -p /home/vagrant/.kube
    cp /etc/rancher/k3s/k3s.yaml /home/vagrant/.kube/config
    chown vagrant:vagrant /home/vagrant/.kube/config

    # Install ArgoCD
    export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
    kubectl create namespace argocd
    kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
  SHELL
  
  # Set the image for the vagrant box
  config.vm.box = "opensuse/Leap-15.2.x86_64"
  # Set the image version
  config.vm.box_version = "15.2.31.632"

  # Forward the ports from the guest VM to the local host machine
  # Forward more ports, as needed
  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.network "forwarded_port", guest: 6111, host: 6111
  config.vm.network "forwarded_port", guest: 6112, host: 6112

  # Set the static IP for the vagrant box
  config.vm.network "private_network", ip: "192.168.50.4"
  
  # Configure the parameters for VirtualBox provider
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
    vb.cpus = 4
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
  end
end
