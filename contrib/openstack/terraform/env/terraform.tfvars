terragrunt = {
  remote_state {
    backend = "swift"
    config {
      container = "${path_relative_to_include()}"
    }
  }
}
