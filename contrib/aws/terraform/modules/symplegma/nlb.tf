resource "aws_lb" "kubernetes_api" {
  name               = "${var.cluster_name}-kubernetes-api-nlb"
  internal           = false
  load_balancer_type = "network"
  subnets            = ["${module.vpc.public_subnets}"]

  enable_cross_zone_load_balancing = true

  tags = "${var.kubernetes_api_lb_tags}"
}

resource "aws_lb_listener" "kubernetes_api" {
  load_balancer_arn = "${aws_lb.kubernetes_api.arn}"
  port              = "${var.kubernetes_api_lb_port}"
  protocol          = "TCP"

  # Be sure to create an aws_lb_target_group first
  default_action {
    target_group_arn = "${aws_lb_target_group.kubernetes_api.arn}"
    type             = "forward"
  }
}

resource "aws_lb_target_group" "kubernetes_api" {
  name     = "${var.cluster_name}-kubernetes-api-tg"
  port     = "${var.kubernetes_api_tg_port}"
  protocol = "TCP"
  vpc_id   = "${module.vpc.vpc_id}"
}

output "kubernetes_api_lb_dns_name" {
  value = "${aws_lb.kubernetes_api.dns_name}"
}
