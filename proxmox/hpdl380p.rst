Upgrading homelab HP DL 380p
============================



latest BIOS
-----------

- download latest firmware (BIOS) for linux in RPM format
- firmware-system-p70-2019.05.24-1.1
- on ubuntu (unpack with Ark)
- look for CPQP7013.6B8 (4MB in size)
- use ilo to upload firmware (update)

M2 disk drive
-------------
- M.2 NGFF SSD naar PCI-E 3.0 X16 High-Speed SSD  (ashata = 5euro)
- need MVME (one notch) m2 card
- it should show up in BIOS / PCI devices
- on linux :#lsblk it should show up 
 
