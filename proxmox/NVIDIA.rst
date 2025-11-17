Setting up NVIDIA Tesla P100
============================

the P100 was choses for balance between performance and price (second hand ebay)


Aliexpress
----------
 PCIE 4.0 3.0 16X Riser Kabel 90/180 Graden Mount Video Grafisch
Gpu 10pin Naar 1x8pin Dual 8(6 + 2)Pin Power Adapter Kabel Voor Hp Dl380 Gen8 Gen9 Server

Cutting the Riser
-----------------

a special Riser for the HP Proliant gen8 is a good idea because it has a PCIE 16x in the middle which allows for the GPU  to be plugged in. (hard to find and expensive) 

I choose the cheap option (evidently) and cut a hole in a riser to extend with a riser cable into this riser. Some more cutting had to be done because the GPU is too long.

For the gen9 there a cheaper riser card options, so no cutting needed...

Configure the BIOS
------------------

(changed IRQ for network card to 11, since conflict)

enter BIOS (F9) and on main bios screen / "Service options" menu item. Under this, enable "PCI Express 64-bit BAR   

configure proxmox host
------------------------

PROXMOX PCI-E GPU passthru

When running proxmox on this hardware, there is more config needed to enable passthru of this GPU to VM.
Enable IOMMU

Edit /etc/default/grub file, modify variable GRUB_CMDLINE_LINUX_DEFAULT adding intel_iommu=on parameter
Enable unsafe intremap

Create file /etc/modprobe.d/iommu_unsafe_interrupts.conf with contents options vfio_iommu_type1 allow_unsafe_interrupts=1
Blacklist nvidia drivers

Create file /etc/modprobe.d/nvidia-blacklist.conf with contents

# blacklist for nvidia gpu passthru
blacklist nouveau
blacklist nvidia*

Apply changes into bootloader

Run proxmox-boot-tool refresh


the idea
--------

the idea is to get nvidia to work on the proxmox host (there will be kernel modules)

for the LXC machines there is no need for kernel drivers!! since already on the host 


Download NVIDIA drivers
-------------------------

NVIDIA-Linux-x86_64-570.133.20.run

https://developer.nvidia.com/cuda-12-8-0-download-archive?target_os=Linux&target_arch=x86_64&Distribution=Debian&target_version=12&target_type=deb_local 

*nvidia is gonna need some kernel (promox) drivers

apt install pve-headers-$(uname -r) build-essential software-properties-common make nvtop htop -y

 ./NVIDIA-Linux-x86_64-570.133.20.run 


copy NVIDIA driver to LXC
---------------------------
pct push 100 NVIDIA-Linux-x86_64-570.133.20.run /root/NVIDIA-Linux-x86_64-570.133.20.run

