# Calico

Calico works pretty much out of the box. Customization can still be done
to enhance performances.

## Changing pods CIDR

Calico role picks up the `kubeadm_pod_subnet` [variable](https://github.com/clusterfrak-dynamics/symplegma-kubeadm/blob/master/master/defaults/main.yaml#L20) and default to `192.168.0.0/16`.

## MTU consideration

Calico does not automatically compute [MTU](https://docs.projectcalico.org/v3.8/networking/mtu#mtu-configuration)

MTU should be set accordingly to your environment.

### AWS with src/dest check enable (default) and single or multiple AZs

```
calico_mtu: 8981
calico_ipv4pool_ipip: "Always"
```

### AWS with src/dest check disable and multiple AZs

```
calico_mtu: 8981
calico_ipv4pool_ipip: "CrossSubnet"
```

### AWS with src/dest check disable and single AZ

```
calico_mtu: 9001
calico_ipv4pool_ipip: "Never"
```

### Bare metal deployment with flat layer 2

```
calico_mtu: 1500
calico_ipv4pool_ipip: "Never"
```

### Bare metal deployment with multiple routed layer 3

```
calico_mtu: 1480
calico_ipv4pool_ipip: "Always"
```

### Bare metal deployment with flat layer 2 and Jumbo Frame enabled

```
calico_mtu: 9000
calico_ipv4pool_ipip: "Never"
```
### Bare metal deployment with multiple routed layer 3 and Jumbo Frame enabled

```
calico_mtu: 8980
calico_ipv4pool_ipip: "Always"
```
