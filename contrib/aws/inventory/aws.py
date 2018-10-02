#!/usr/bin/env python

from __future__ import print_function
import boto3
import os
import argparse
import json

class SearchEC2Tags(object):

  def __init__(self):
    self.parse_args()
    if self.args.list:
      self.search_tags()
    if self.args.host:
      data = {}
      print(json.dumps(data, indent=2))

  def parse_args(self):

    ##Check if VPC_VISIBILITY is set, if not default to private
    if "SYMPLEGMA_VPC_VISIBILITY" in os.environ:
      self.vpc_visibility = os.environ['SYMPLEGMA_VPC_VISIBILITY']
    else:
      self.vpc_visibility = "private"

    ##Support --list and --host flags. We largely ignore the host one.
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', action='store_true', default=False, help='List instances')
    parser.add_argument('--host', action='store_true', help='Get all the variables about a specific instance')
    self.args = parser.parse_args()

  def search_tags(self):
    hosts = {}
    hosts['_meta'] = { 'hostvars': {} }

    ##Search ec2 three times to find nodes of each group type. Relies on kubespray-role key/value.
    for group in ["master", "node", "etcd"]:
      hosts[group] = []
      tag_role_key = "symplegma-role"
      tag_role_value = ["*"+group+"*"]
      tag_env_key = "symplegma-cluster"
      tag_env_value = [os.environ['SYMPLEGMA_CLUSTER']]
      region = os.environ['SYMPLEGMA_AWS_REGION']

      ec2 = boto3.resource('ec2', region)

      instances = ec2.instances.filter(Filters=[{'Name': 'tag:'+tag_role_key, 'Values': tag_role_value}, {'Name': 'tag:'+tag_env_key, 'Values': tag_env_value}, {'Name': 'instance-state-name', 'Values': ['running']}])
      for instance in instances:
        if self.vpc_visibility == "public":
          hosts[group].append(instance.public_dns_name)
          hosts['_meta']['hostvars'][instance.public_dns_name] = {
             'ansible_ssh_host': instance.public_ip_address
          }
        else:
          hosts[group].append(instance.private_dns_name)
          hosts['_meta']['hostvars'][instance.private_dns_name] = {
             'ansible_ssh_host': instance.private_ip_address
          }

    hosts['k8s-cluster'] = {'children':['master', 'node']}
    print(json.dumps(hosts, sort_keys=True, indent=2))

SearchEC2Tags()
