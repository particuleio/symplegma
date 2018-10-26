# Deploying on AWS

Symplegma supports AWS as a cloud provider.

## Architecture

`contrib/aws/` contains terraform file to deploy the following architecture. This is strongly opinionated and deploys the following architecture:

![aws reference architecture](./images/aws-infra-transparent.png)

This is subject to change in the future as PR are welcomed to make the possibilities evolved.

## Terraform and Terragrunt

### Terragrunt modules

Symplegma is packaged in the form a [Terragrunt module](https://github.com/gruntwork-io/terragrunt) available [here](https://github.com/clusterfrak-dynamics/symplegma/tree/master/contrib/aws/terraform).


### Terragrunt variables

```
{!contrib/aws/terraform/env/sample/symplegma/terraform.tfvars!}
```


