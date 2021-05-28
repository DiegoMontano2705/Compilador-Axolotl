#!/usr/bin/env bash

FILE_AX=${1?Error: nombre sin .ax o .obj}
FILE_OBJ=$FILE_AX".obj"

python3 Axolotl++.py $FILE_AX".ax" 
python3 MaquinaVirtual.py $FILE_OBJ