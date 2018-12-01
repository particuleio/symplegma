terragrunt = {
  include {
    path = "${find_in_parent_folders()}"
  }

  terraform {
    source = "github.com/clusterfrak-dynamics/symplegma.git//contrib/openstack/terraform/modules/symplegma"
  }
}

//
// [provider]
//

//
// [kubernetes]
//
cluster_name = "symplegma"

network_name    = "internal_network"
subnet_cidr     = "10.0.0.0/24"
dns_nameservers = []
use_neutron     = "1"

number_of_k8s_masters         = "3"
number_of_k8s_masters_no_etcd = "0"
number_of_k8s_nodes           = "0"
floatingip_pool               = "ext-net"
number_of_bastions            = "0"
external_net                  = "ext-net-uuid"
router_id                     = ""

az_list                                      = ["nova"]
number_of_etcd                               = "0"
number_of_k8s_masters_no_floating_ip         = "0"
number_of_k8s_masters_no_floating_ip_no_etcd = "0"
number_of_k8s_nodes_no_floating_ip           = "0"
public_key_path                              = "~/.ssh/id_rsa.pub"
image                                        = "CoreOS 1068.9.0"
ssh_user                                     = "core"
flavor_k8s_master                            = "128829e3-117d-49da-ae58-981bb2c04b0e"
flavor_k8s_node                              = "128829e3-117d-49da-ae58-981bb2c04b0e"
flavor_etcd                                  = "128829e3-117d-49da-ae58-981bb2c04b0e"
flavor_bastion                               = "128829e3-117d-49da-ae58-981bb2c04b0e"
k8s_master_fips                              = []
k8s_node_fips                                = []
bastion_fips                                 = []
bastion_allowed_remote_ips                   = ["0.0.0.0/0"]
supplementary_master_groups                  = ""
supplementary_node_groups                    = ""
worker_allowed_ports                         = [
  {
    "protocol" = "tcp"
    "port_range_min" = 30000
    "port_range_max" = 32767
    "remote_ip_prefix" = "0.0.0.0/0"
  }
]


