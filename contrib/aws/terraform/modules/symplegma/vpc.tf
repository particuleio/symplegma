module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 2.0"
  name    = var.vpc_name
  cidr    = var.vpc_cidr

  azs             = var.vpc_azs
  private_subnets = var.vpc_private_subnets
  public_subnets  = var.vpc_public_subnets

  enable_nat_gateway   = var.vpc_enable_nat_gateway
  enable_dns_hostnames = var.vpc_enable_dns_hostnames

  tags = merge(local.network_tags, var.vpc_tags)
}
