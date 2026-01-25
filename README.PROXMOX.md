# Importação de um ficheiro OVA no Proxmox (CLI)

Este guia descreve **todo o processo de importação de um OVA no Proxmox exclusivamente pela linha de comandos**, incluindo criação da VM, importação do disco, configuração de boot e limpeza final.

Configuração alvo da VM:

* **VM ID:** 9001
* **CPU:** host
* **RAM:** 8 GB
* **OS Type:** Linux
* **BIOS:** SeaBIOS
* **MAC Address:** `BC:24:11:01:0A:0A`
* **Start on boot:** ativo, com delay de 1 minuto

---

## 1️⃣ Criar pasta temporária e aceder a ela

```bash
mkdir -p /root/ova_import
cd /root/ova_import
```

---

## 2️⃣ Download do ficheiro OVA

```bash
wget https://assets.iave.pt/production/vm-images/iave-offline-production-v2-1-1.ova
```

---

## 3️⃣ Extrair o OVA

```bash
tar xvf iave-offline-production-v2-1-1.ova
```

Após a extração deverão existir ficheiros `.ovf`, `.vmdk` e possivelmente `.mf`.

---

## 4️⃣ Criar a VM vazia (ID 9001)

```bash
qm create 9001 \
  --name iave-offline \
  --memory 8192 \
  --cores 4 \
  --cpu host \
  --ostype l26 \
  --bios seabios \
  --net0 virtio=BC:24:11:01:0A:0A,bridge=vmbr0 \
  --scsihw virtio-scsi-pci \
  --onboot 1 \
  --startup order=1,up=60
```



Estas definições podem ser alteradas depois da máquina criada. 
- name - Options » Name
- memory - Hardware » Memory
- cores - Hardware » Processors
- cpu type - Hardware » Processors
- mac e bridge - Hardware » Network


A ponderar alterar `cores` para até 90% dos cores disponíveis. Por exemplo, numa máquina de 10 cores, alterar para 8 ou 9. 
Consultar o número de cores disponíveis em Node » Summary » CPU usage.

---


## 5️⃣ Remover disco existente (caso exista)

```bash
qm set 9001 --delete scsi0
```


---

## 6️⃣ Importar o disco VMDK e converter para qcow2

```bash
qm importdisk 9001 \
  ./iave-offline-production-v2-1-1-disk001.vmdk \
  local \
  --format qcow2
```

O disco será criado no storage `local`, tipicamente como:

```
local:9001/vm-9001-disk-0.qcow2
```

PS: Que ficará localmente em `/var/lib/vz/images/9001`


---

## 7️⃣ Associar o disco importado à VM

```bash
qm set 9001 --scsi0 local:9001/vm-9001-disk-0.qcow2
```

---

## 8️⃣ Definir o disco como primeiro no boot order

```bash
qm set 9001 --boot order=scsi0
```

---

## 9️⃣ Confirmar a configuração da VM

```bash
qm config 9001
```

Confirmar especialmente:

* `cpu: host`
* `memory: 8192`
* `bios: seabios`
* `scsi0` configurado
* `boot: order=scsi0`
* `onboot: 1`
* `startup: order=1,up=60`

---

## 🔟 Arrancar a VM

```bash
qm start 9001
```


O primeiro boot poderá demorar dependendo da velocidade de ligação e do número de cores. 
Em Summary, poderá monotorizar `Network Traffic`.

---

##  1️⃣1️⃣ Parar a VM ignorando o lock (se necessário)

Usar este comando caso a VM esteja bloqueada por um lock residual:

```bash
qm stop 9001 --skiplock
```

---

## 1️⃣2️⃣ Limpeza (recomendado)

Depois de confirmares que a VM arranca corretamente:

```bash
cd /root
rm -rf ova_import
```

---

## ℹ️ Notas finais

* Este procedimento assume o uso do storage `local` e da bridge `vmbr0`.
* Ajusta estes valores caso o teu ambiente Proxmox seja diferente.
* Todo o processo foi pensado para ser **reprodutível, previsível e 100% CLI**.
* Ponderar um sistema de backups regulares da VM completa, por exemplo, uma vez por dia às 22h00
* Ponderar um sistema de backups offsite dos backups criados.
