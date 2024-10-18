Intro
=====

These are some building blocks in what should become a local LLM for financial info.
I do like investing, but I rather not read all the publications.

This software should be able to  : 

- leech reports
- embed them into a vectordb
- use a local LLM to retrieve and bundle information
- generate a report


Homelab: (did not want to create separate repo)
--------

I have an old HP dl380p gen8, which I modified:
- removed a SAS controller card, and have disks on internal controller
- add a 1TB NVME M2 disk, on PCI-e 3 adapter
- installed Proxmox
 
todo:
- boot on sata disk on cdrom port
- remove RAID1 and use disks as such: space over security
- insert NVIDIA P4 single slot

