locals {
  kubernetes_tags = [
    {
      key                 = "kubernetes.io/cluster/${var.cluster_name}"
      value               = "owned"
      propagate_at_launch = true
    },
    {
      key                 = "Terraform"
      value               = "true"
      propagate_at_launch = true
    },
    {
      key                 = "symplegma-cluster"
      value               = "${var.cluster_name}"
      propagate_at_launch = true
    },
  ]

  network_tags = {
    "kubernetes.io/cluster/${var.cluster_name}" = "owned"
    Terraform                                   = "true"
  }

  master_tags = [
    {
      key                 = "Name"
      value               = "${var.cluster_name}-master"
      propagate_at_launch = true
    },
    {
      key                 = "symplegma-role"
      value               = "master"
      propagate_at_launch = true
    },
  ]

  node_tags = [
    {
      key                 = "Name"
      value               = "${var.cluster_name}-node"
      propagate_at_launch = true
    },
    {
      key                 = "symplegma-role"
      value               = "node"
      propagate_at_launch = true
    },
  ]
}

resource "aws_launch_template" "master" {
  name          = "${var.cluster_name}-lt-master"
  image_id      = "${var.master_asg_ami}"
  key_name      = "${var.master_asg_key_name}"
  instance_type = "${var.master_asg_instance_type}"

  iam_instance_profile {
    name = "${aws_iam_instance_profile.master.name}"
  }

  block_device_mappings {
    device_name = "/dev/xvda"

    ebs {
      volume_size = "${var.master_asg_root_volume_size}"
      volume_type = "gp2"
    }
  }
}

resource "aws_autoscaling_group" "master" {
  name                      = "${var.cluster_name}-asg-master"
  vpc_zone_identifier       = ["${module.vpc.private_subnets}"]
  min_size                  = "${var.master_asg_min_size}"
  max_size                  = "${var.master_asg_max_size}"
  desired_capacity          = "${var.master_asg_desired_capacity}"
  wait_for_capacity_timeout = 0
  tags                      = ["${concat(local.kubernetes_tags,local.master_tags,var.master_asg_tags)}"]

  target_group_arns = ["${aws_lb_target_group.kubernetes_api.arn}"]

  launch_template = {
    id      = "${aws_launch_template.master.id}"
    version = "$$Latest"
  }
}

resource "aws_launch_template" "node" {
  name          = "${var.cluster_name}-lt-node"
  image_id      = "${var.node_asg_ami}"
  key_name      = "${var.node_asg_key_name}"
  instance_type = "${var.node_asg_instance_type}"

  iam_instance_profile {
    name = "${aws_iam_instance_profile.node.name}"
  }

  block_device_mappings {
    device_name = "/dev/xvda"

    ebs {
      volume_size = "${var.node_asg_root_volume_size}"
      volume_type = "gp2"
    }
  }
}

resource "aws_autoscaling_group" "node" {
  name                      = "${var.cluster_name}-asg-node"
  vpc_zone_identifier       = ["${module.vpc.private_subnets}"]
  min_size                  = "${var.node_asg_min_size}"
  max_size                  = "${var.node_asg_max_size}"
  desired_capacity          = "${var.node_asg_desired_capacity}"
  wait_for_capacity_timeout = 0
  tags                      = ["${concat(local.kubernetes_tags,local.node_tags,var.master_asg_tags)}"]

  launch_template = {
    id      = "${aws_launch_template.node.id}"
    version = "$$Latest"
  }
}
