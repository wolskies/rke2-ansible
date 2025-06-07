credit to Jim at Jim's Garage

### Configure ethernet interfaces for kube-vip

For kube-vip, primary network interfaces need to be predictable, in this case set them to `eth0`.  On Ubuntu, that's via netplan.  Change the file `/etc/netplan/50-cloud-init.yaml` to read (obviously, use the correct mac address):

```
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: true
      match:
        macaddress: 00:24:27:89:2d:a6
      set-name: eth0
```

e0:51:d8:1c:2d:00