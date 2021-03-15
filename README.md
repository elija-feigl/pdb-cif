[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Python-version:](https://img.shields.io/badge/python-v3.7-green)]() [PDB mmCIF converter](#pdbmmcifconverter) | [Usage](#usage) | [Requirements](#requirements) | [References](#references) 


# NOTE
further development of this code has been moved to https://github.com/elija-feigl/dnaFit
this repository might not be updated in the future

# PDB mmCIF converter
[PDB_CIF](https://github.com/elija-feigl/pdb-cif) namd (enrgMD) PDB to chimera PDB converter for DNA origami nano structures.

STATUS: development

currently supported conversions:
PDB (namd) -> mmCIF (rcsb, chimera(X))

planned conversions:
PDB (namd) -> PDB (coot)
PDB (oxDNA) -> mmCIF
mmCIF -> PDB (namd, coot)


NOTE: this code is exclusively written for DNA origami nano structures

# Usage
```
python3 PDB2mmCIF.py [-h] [-H] INPUT
```
positional arguments:
  input           input file

optional arguments:
  -h, --help      show this help message and exit
  -H, --hydrogen  remove hydrogen atoms? (default: True)

# Requirements
required PyPI packages:
```
attrs >= 19.3.0 (type hinting)
numpy >= 1.19.4
```
