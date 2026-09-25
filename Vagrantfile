Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-22.04"
  config.vm.define "servidorRest"
  config.vm.hostname = "servidorRest"
  config.vm.network "private_network", ip: "192.168.60.3"
  config.vm.synced_folder ".", "/vagrant", disabled: true
  config.vm.provision "file", source: ".", destination: "/home/vagrant/practica-rest-equipo"
  config.vm.provision "shell", path: "scripts/provision.sh"
end
