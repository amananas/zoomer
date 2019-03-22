#!/bin/bash


DEVICE="/dev/sdz"
DEVICE_PARTITION_PREFIX="/dev/sdz"

sfdisk --delete "$DEVICE"
echo 'label: dos' | sfdisk "$DEVICE"
echo ',100M,c
,,,' | sfdisk "$DEVICE"
mkfs.vfat "${DEVICE_PARTITION_PREFIX}1"
mkfs.ext4 "${DEVICE_PARTITION_PREFIX}2"

mkdir -p mnt/root mnt/boot
mount "${DEVICE_PARTITION_PREFIX}1" mnt/boot
mount "${DEVICE_PARTITION_PREFIX}2" mnt/root

wget http://os.archlinuxarm.org/os/ArchLinuxARM-rpi-2-latest.tar.gz
bsdtar -xpf ArchLinuxARM-rpi-2-latest.tar.gz -C mnt/root
rm ArchLinuxARM-rpi-2-latest.tar.gz
sync
mv mnt/root/boot/* mnt/boot

cp -r root mnt/

umount mnt/root mnt/boot
rm -rf mnt

