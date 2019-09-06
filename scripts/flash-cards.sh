#!/bin/bash

RPI_IMAGE=rpi-esu-bridge-ro-20180708-a6d94c.img

umount /dev/sdd1
umount /dev/sde1
umount /dev/sdf1
umount /dev/sdg1
umount /dev/sdh1
umount /dev/sdi1
umount /dev/sdj1
umount /dev/sdd2
umount /dev/sde2
umount /dev/sdf2
umount /dev/sdg2
umount /dev/sdh2
umount /dev/sdi2
umount /dev/sdj2

dd if=$RPI_IMAGE of=/dev/sdd &
dd if=$RPI_IMAGE of=/dev/sde &
dd if=$RPI_IMAGE of=/dev/sdf &
dd if=$RPI_IMAGE of=/dev/sdg &
dd if=$RPI_IMAGE of=/dev/sdh &
dd if=$RPI_IMAGE of=/dev/sdi &
dd if=$RPI_IMAGE of=/dev/sdj &

