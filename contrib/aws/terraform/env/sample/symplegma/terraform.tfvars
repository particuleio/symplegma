terragrunt = {
  include {
    path = "${find_in_parent_folders()}"
  }

  terraform {
    source = "../../../modules//symplegma"
  }
}

//
// [provider]
//
aws_region = "eu-west-1"

//
// [kubernetes]
//
cluster_name = "symplegma"

//
// [module][vpc]
//
vpc_name = "symplegma"
vpc_cidr = "10.0.0.0/16"
vpc_azs             = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
vpc_private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
vpc_public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
vpc_enable_nat_gateway = true
vpc_enable_dns_hostnames = true
vpc_tags = {
    Environment = "sample"
}

//
// [module][bastion]
//
bastion_name = "symplegma-bastion"
bastion_ami = "ami-00035f41c82244dab"
bastion_instance_type = "t2.small"
bastion_key_name = "klefevre-sorrow"

bastion_tags = {
    Terraform = "true"
    Environment = "sample"
}

//
// [module][master_asg]
//
master_asg_ami = "ami-099b2d1bdd27b4649"
master_asg_root_volume_size = 50
master_asg_max_size = 3
master_asg_min_size = 3
master_asg_desired_capacity = 3
master_asg_instance_type = "t3.large"
master_asg_key_name = "klefevre-sorrow"
master_asg_tags = [
    {
      key                 = "Environment"
      value               = "sample"
      propagate_at_launch = true
    }
  ]

//
// [module][node_asg]
//
node_asg_ami = "ami-099b2d1bdd27b4649"
node_asg_root_volume_size = 50
node_asg_max_size = 2
node_asg_min_size = 2
node_asg_desired_capacity = 2
node_asg_instance_type = "t3.large"
node_asg_key_name = "klefevre-sorrow"
node_asg_tags = [
    {
      key                 = "Environment"
      value               = "sample"
      propagate_at_launch = true
    }
  ]

//
// [nlb]
//
kubernetes_api_lb_port = 443
kubernetes_api_tg_port = 6443
kubernetes_api_lb_tags = {
      Environment = "sample"
}
