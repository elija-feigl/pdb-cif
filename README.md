[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Python-version:](https://img.shields.io/badge/python-v3.7-green)]() [PDB mmCIF converter](#pdbmmcifconverter) | [Usage](#usage) | [Requirements](#requirements) | [References](#references) 

# PDB mmCIF converter
[FitViewer](https://github.com/elija-feigl/pdb-cif) namd (enrgMD) PDB to chimera PDB converter for DNA origami nano structures.

STATUS: development

currently supported conversion:
PDB (namd) -> mmCIF (rcsb, chimera(X))  
PDB (namd) -> PDB (coot)

NOTE: this code is exclusively written for DNA origami nano structures

# Usage
```
python3 PDB2mmCIF.py [-h] -i INPUT -o OUTPUT [-H]
```
optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input file
  -o OUTPUT, --output OUTPUT
                        output file
  -H, --hydrogen        remove hydrogen atoms? (default: True)

# Requirements
required PyPI packages:
```
attrs >= 19.3.0 (type hinting)
```