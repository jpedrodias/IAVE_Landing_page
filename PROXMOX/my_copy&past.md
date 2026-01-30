# Edifício 1 (on vlan 10)
```bash
mkdir -p /root/ova_import
cd /root/ova_import

wget https://assets.iave.pt/production/vm-images/iave-offline-production-v2-1-1.ova

tar xvf iave-offline-production-v2-1-1.ova

qm create 9001 \
  --name ed1-iave-offline \
  --memory 8192 \
  --cores 10 \
  --cpu host \
  --ostype l26 \
  --bios seabios \
  --net0 virtio=BC:24:11:01:0A:0A,bridge=vmbr1,tag=10 \
  --scsihw virtio-scsi-pci \
  --onboot 1 \
  --startup order=99,up=90

sync

qm importdisk 9001 \
  ./iave-offline-production-v2-1-1-disk001.vmdk \
  local \
  --format qcow2

sync
  
qm set 9001 --scsi0 local:9001/vm-9001-disk-0.qcow2
qm set 9001 --boot order=scsi0

qm config 9001

cd /root/
rm  -r /root/ova_import

qm start 9001
```

**Stop VM** 
```
qm stop 9001 --skiplock
```




***
# Edifício 2 (on vlan 10)
```bash
mkdir -p /root/ova_import
cd /root/ova_import

wget https://assets.iave.pt/production/vm-images/iave-offline-production-v2-1-1.ova

tar xvf iave-offline-production-v2-1-1.ova

qm create 9002 \
  --name ed2-iave-offline \
  --memory 8192 \
  --cores 10 \
  --cpu host \
  --ostype l26 \
  --bios seabios \
  --net0 virtio=BC:24:11:02:0A:0A,bridge=vmbr1,tag=10 \
  --scsihw virtio-scsi-pci \
  --onboot 1 \
  --startup order=99,up=90
 
sync

qm importdisk 9002 \
  ./iave-offline-production-v2-1-1-disk001.vmdk \
  local \
  --format qcow2

sync

qm set 9002 --scsi0 local:9002/vm-9002-disk-0.qcow2
qm set 9002 --boot order=scsi0

qm config 9002

qm start 9002
```


**Stop VM** 
```
qm stop 9002 --skiplock
```
***


# Edifício 3 (on vlan 10)
```bash
mkdir -p /root/ova_import
cd /root/ova_import

wget https://assets.iave.pt/production/vm-images/iave-offline-production-v2-1-1.ova

tar xvf iave-offline-production-v2-1-1.ova

qm create 9003 \
  --name ed3-iave-offline \
  --memory 8192 \
  --cores 10 \
  --cpu host \
  --ostype l26 \
  --bios seabios \
  --net0 virtio=BC:24:11:03:0A:0A,bridge=vmbr1,tag=10 \
  --scsihw virtio-scsi-pci \
  --onboot 1 \
  --startup order=99,up=90

sync

qm importdisk 9003 \
  ./iave-offline-production-v2-1-1-disk001.vmdk \
  local \
  --format qcow2
sync
 
qm set 9003 --scsi0 local:9003/vm-9003-disk-0.qcow2
qm set 9003 --boot order=scsi0

qm config 9003

qm start 9003
rm  -r /root/ova_import
```


**Stop VM** 
```
qm stop 9003 --skiplock
```
