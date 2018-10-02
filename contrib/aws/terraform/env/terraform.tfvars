terragrunt = {
  remote_state {
    backend = "s3"
    config {
      bucket         = "symplegma-remote-state"
      key            = "${path_relative_to_include()}"
      region         = "eu-west-1"
      encrypt        = true
      dynamodb_table = "symplegma-remote-state-lock"
    }
  }
}
