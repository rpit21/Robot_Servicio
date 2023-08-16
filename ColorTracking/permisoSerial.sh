#!/bin/bash
echo "jetson123" |sudo -S usermode -a -G dialout jetsonnano
sudo chmod a+rw /dev/ttyTHS1

echo Permisos a los puertos Dados