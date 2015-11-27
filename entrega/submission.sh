#!/usr/bin/env bash
./compile.sh
build/entrega /home/martin/Documents/repos/datos/entrega/trainFilteredSinBinarizarV3-columnas.csv \
              /home/martin/Documents/repos/datos/entrega/testFilteredSinBinarizarV3-columnas.csv \
    | 7zr a -si /media/martin/MARTIN/predicted.csv.7z
