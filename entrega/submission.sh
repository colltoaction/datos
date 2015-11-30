#!/usr/bin/env bash
./compile.sh
cat header.txt
echo
echo "Presione una tecla para comenzar"
read -n 1
time build/entrega /home/martin/Documents/repos/datos/entrega/trainFilteredSinBinarizarV3-columnas.csv \
                   /home/martin/Documents/repos/datos/entrega/testFilteredSinBinarizarV3-columnas.csv \
    | 7zr a -si /home/martin/Documents/repos/datos/entrega/predicted.csv.7z
