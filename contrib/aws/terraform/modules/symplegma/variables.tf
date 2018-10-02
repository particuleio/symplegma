variable "aws_region" {}

variable "cluster_name" {}

variable "vpc_name" {}

variable "vpc_cidr" {}

variable "vpc_azs" {
  type = "list"
}

variable "vpc_private_subnets" {
  type = "list"
}

variable "vpc_public_subnets" {
  type = "list"
}

variable "vpc_enable_nat_gateway" {}

variable "vpc_enable_dns_hostnames" {}

variable "vpc_tags" {
  type = "map"
}

variable "bastion_name" {}

variable "bastion_ami" {}

variable "bastion_instance_type" {}

variable "bastion_key_name" {}

variable "bastion_tags" {
  type = "map"
}

variable "master_asg_ami" {}

variable "master_asg_min_size" {}

variable "master_asg_max_size" {}

variable "master_asg_desired_capacity" {}

variable "master_asg_tags" {
  type = "list"
}

variable "master_asg_key_name" {}

variable "master_asg_instance_type" {}

variable "master_asg_root_volume_size" {}

variable "node_asg_ami" {}

variable "node_asg_min_size" {}

variable "node_asg_max_size" {}

variable "node_asg_desired_capacity" {}

variable "node_asg_tags" {
  type = "list"
}

variable "node_asg_key_name" {}

variable "node_asg_instance_type" {}

variable "node_asg_root_volume_size" {}

variable "kubernetes_api_lb_tags" {
  type = "map"
}
variable "kubernetes_api_lb_port" {}

variable "kubernetes_api_tg_port" {}
