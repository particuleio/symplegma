module "bastion" {
  source                      = "terraform-aws-modules/ec2-instance/aws"
  version                     = "~> 2.0"
  name                        = var.bastion_name
  instance_count              = 1
  associate_public_ip_address = true

  ami                    = var.bastion_ami
  instance_type          = var.bastion_instance_type
  key_name               = var.bastion_key_name
  monitoring             = true
  vpc_security_group_ids = [aws_default_security_group.vpc_default_sg.id]
  subnet_id              = module.vpc.public_subnets[0]

  tags = var.bastion_tags
}
