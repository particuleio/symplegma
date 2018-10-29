terraform {
  backend "s3" {}
}

provider "aws" {
  region = "${var.aws_region}"
}

output "aws_region" {
  value = "${var.aws_region}"
}

output "cluster_name" {
  value = "${var.cluster_name}"
}
