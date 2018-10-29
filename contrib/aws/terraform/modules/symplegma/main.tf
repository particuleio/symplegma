terraform {
  backend "s3" {}
}

provider "aws" {
  region = "${var.aws_region}"
}

output "aws_region" {
  region = "${var.aws_region}"
}

output "cluster_name" {
  cluster_name = "${var.cluster_name}"
}
