#!/usr/bin/env python
# -*- coding: utf-8 -*-

import attr
import numpy as np
from typing import Any

from utils import number_2_hybrid36 as int_2_h36
from utils import hybrid36_2_number as h36_2_int


@attr.s
class Number(object):
    """ read from hybrid36 string string or int """
    _input: Any = attr.ib()

    def __attrs_post_init__(self):
        self.n: int = self._convert_input(self._input)

    def _convert_input(self, inpt):
        if isinstance(inpt, int):
            return inpt
        elif isinstance(inpt, str):
            if inpt.isdigit():
                return int(inpt)
            else:
                return h36_2_int(inpt)
        else:
            raise NotImplementedError

    def as_h36(self, width):
        return int_2_h36(number=self.n, width=width)

    def as_str(self):
        return str(self.n)


@attr.s
class AtomName(object):
    """ use cif standart """
    _input: str = attr.ib()

    def __attrs_post_init__(self):
        self.name: str = self._convert_input(ipt=self._input)
        self.NAMD = {"O1P": "OP1", "O2P": "OP2", "C5M": "C7", }

    def _convert_input(self, ipt: str) -> str:
        ipt = ipt.strip()
        return self.NAMD[ipt] if ipt in self.NAMD.keys() else ipt

    def as_pdb4namd(self):
        """
    Atom names start with element symbols right-justified in columns 13-14 as
    permitted by the length of the name. For example, the symbol FE for iron
    appears in columns 13-14, whereas the symbol C for carbon appears in column
    14 (see Misaligned Atom Names). If an atom name has four characters,
    however, it must start in column 13 even if the element symbol is a single
    character (for example, see Hydrogen Atoms).
        """
        opt = self.name
        DMNA = {v: k for k, v in iter(self.NAMD.items())}
        namePDB = DMNA[opt] if opt in DMNA.keys() else opt
        # TODO check justification rules
        return namePDB

    def as_str(self):
        return self.name


@attr.s
class ResName(object):
    """resname [DA, DC, DG, DT]"""
    _input: Any = attr.ib()

    def __attrs_post_init__(self):
        self.name: str = self._convert_input(inpt=self._input)
        self.NAMD = {"CYT": "DC", "GUA": "DG", "THY": "DT", "ADE": "DA", }

    def _convert_input(self, inpt: str) -> str:
        inpt = inpt.strip()
        return self.NAMD[inpt] if inpt in self.NAMD.keys() else inpt

    def as_pdb4namd(self):
        """returns resname [ADE, CYT, GUA, THY], len=3 """
        DMNA = {v: k for k, v in iter(self.NAMD.items())}
        return DMNA[self.name]

    def as_str(self):
        return self.name


@attr.s
class ChainID(object):
    """ read from hybrid36 string string or int """
    _input: Any = attr.ib()

    def __attrs_post_init__(self):
        self.n: int = self._convert_input(self._input)

    def _convert_input(self, inpt: str) -> str:
        raise NotImplementedError


@attr.s
class Atom(object):
    """
1234567890123456789012345678901234567890123456789012345678901234567890123456789
Atom  Asnum_Atna-Rna_IRsqn_   XxxxxxxxYyyyyyyyZzzzzzzzOoooooTttttt.     SegmElC
#energMD
ATOM     11  C5' ADE D   1     202.444 396.338 395.231  0.00  0.00      D001
#2cif
ATOM     11  C5'  DTAA   1     -95.447  -2.873 127.534  1.00  0.00      AA00 C
    """
    atom_coor: np.Array = attr.ib()
    atom_number: Number = attr.ib()
    atom_name: AtomName = attr.ib()
    res_name: ResName = attr.ib()
    chain_id: ChainID = attr.ib()
    res_number: Number = attr.ib()

    def asCif(self) -> str:
        raise NotImplementedError

    def asPdb(self) -> str:
        raise NotImplementedError
