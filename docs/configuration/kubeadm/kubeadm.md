# Kubeadm

Kubeadm configuration can be overridden in `group_vars/all/all/yml`

As Kubeadm config files are already in YAML, `symplegma-kubeadm` role
just pipes values into the configuration file. This allow you to use
all the flags and options possible without Ansible knowing them.

The following variable are self explanatory:

```
kubeadm_api_server_extra_args: {}

kubeadm_api_server_extra_volumes: {}

kubeadm_controller_manager_extra_args: {}

kubeadm_controller_manager_extra_volumes: {}

kubeadm_scheduler_extra_args: {}

kubeadm_scheduler_extra_volumes: {}

kubeadm_kubelet_extra_args: {}

kubeadm_kubelet_component_config: {}

kubeadm_kube_proxy_component_config: {}
```

These variables are added to the [Kubeadm config file](https://github.com/clusterfrak-dynamics/symplegma-kubeadm/blob/master/master/templates/kubeadm-config.yaml.j2)

## Example: customize Kubelet

```
kubeadm_kubelet_component_config: |
  evictionHard:
    memory.available:  "200Mi"
  failSwapOn: "false"
```

Check out [Kubeadm documentation](https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/)
