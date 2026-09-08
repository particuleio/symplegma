# Kubeadm

Configuration uses `kubeadm.k8s.io/v1beta4`. Set overrides as native YAML in
`group_vars/all/all.yml`. Extra arguments are lists of `name` / `value` objects;
values must be strings, and repeated names are supported. Volumes and certificate
SANs are lists. Kubelet and kube-proxy component configurations are mappings.

```yaml
kubeadm_api_server_extra_args:
  - name: audit-log-maxage
    value: "30"
kubeadm_api_server_extra_volumes: []
kubeadm_controller_manager_extra_args: []
kubeadm_controller_manager_extra_volumes: []
kubeadm_scheduler_extra_args: []
kubeadm_scheduler_extra_volumes: []
kubeadm_kubelet_extra_args: []
kubeadm_api_server_cert_extra_sans:
  - api.example.com
kubeadm_kubelet_component_config:
  evictionHard:
    memory.available: 200Mi
  failSwapOn: false
kubeadm_kube_proxy_component_config: {}
```

The roles also convert legacy YAML block strings and argument mappings, but new
inventories should use native YAML. Boolean component settings must be booleans.
In-tree cloud provider flags were removed from the API server and controller
manager. For AWS, deploy the external cloud controller and use the kubelet's
`cloud-provider: external` argument shown in `contrib/aws/extra_vars.yml`.

Worker discovery verifies the control plane CA public key hash. Kubeadm controls
the supported etcd, CoreDNS and kube-proxy image versions for each Kubernetes
release; `etcd_version` in the bootstrap role controls the host tools only.

See the [kubeadm v1beta4 API](https://kubernetes.io/docs/reference/config-api/kubeadm-config.v1beta4/)
and [kubelet configuration](https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/).
