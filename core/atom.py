#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.utils import int_2_h36, h36_2_int, int_2_cifSegID, int_2_chimeraSegID
import attr
import numpy as np
from typing import Any


@attr.s
class Number(object):
    """ read from hybrid36 string string or int """
    _input: Any = attr.ib()

    def __attrs_post_init__(self):
        self.n: int = self._convert_input(self._input)

    def _convert_input(self, inpt: Any):
        if isinstance(inpt, int):
            return inpt
        elif isinstance(inpt, str):
            if inpt.isdigit():
                return int(inpt)
            else:
                return h36_2_int(inpt)
        else:
            raise NotImplementedError

    def as_pdb4namd(self, width: int) -> str:
        return self.as_h36(width=width)

    def as_h36(self, width: int) -> str:
        return int_2_h36(number=self.n, width=width)

    def as_str(self) -> str:
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

    def element_name(self) -> str:
        if len(self.name) == 1:
            return self.name
        else:
            return ''.join(filter(str.isalpha, self.name[:2]))

    def as_pdb4namd(self, width: int) -> str:
        opt = self.name
        DMNA = {v: k for k, v in iter(self.NAMD.items())}
        namePDB = DMNA[opt] if opt in DMNA.keys() else opt
        if len(namePDB) == 1:
            return namePDB.ljust(2, " ").rjust(width, " ")
        elif len(namePDB) == 2:
            return namePDB.ljust(1, " ").rjust(width, " ")
        else:
            return namePDB.rjust(width, " ")

    def as_cif(self) -> str:
        if "'" in self.name:
            return "\"{}\"".format(self.name)
        return self.name

    def as_str(self) -> str:
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

    def as_pdb4namd(self, width: int) -> str:
        """returns resname [ADE, CYT, GUA, THY], len=3 """
        DMNA = {v: k for k, v in iter(self.NAMD.items())}
        return DMNA[self.name].rjust(width, " ")

    def as_str(self) -> str:
        return self.name


@attr.s
class ChainID(object):
    _input: Any = attr.ib()

    def __attrs_post_init__(self):
        self.n: int = self._convert_input(self._input)

    def _convert_input(self, inpt: Any):
        if isinstance(inpt, int):
            return inpt
        elif isinstance(inpt, str):
            if inpt.isdigit():
                return int(inpt)
            else:
                # TODO: implement read from h36 or similar
                # -low: as cif has int-id and namd has to be reset anyways
                # reverse: int_2_cifSegID or int_2_chimSegID
                return h36_2_int(inpt)
        else:
            raise NotImplementedError

    def as_pdb4namd(self, width: int) -> str:
        nlast = int(str(self.n)[0])
        n2char = "ABCDEFGHIJ"[nlast]
        return n2char.rjust(width, " ")

    def as_cif(self):
        """1-2 letter all caps"""
        raise int_2_cifSegID(self.n).rjust(2, " ")

    def as_chimera(self):
        """2 letter h36?"""
        raise int_2_chimeraSegID(self.n)

    def as_segName4namd(self, width: int) -> str:
        return "{:0{width}d}".format(self.n, width=width)

    def as_str(self) -> str:
        return str(self.n)


@attr.s
class Atom(object):
    """ TODO: doc
    """
    atom_coor: np.Array = attr.ib()
    atom_number: Number = attr.ib()
    atom_name: AtomName = attr.ib()
    res_name: ResName = attr.ib()
    chain_id: ChainID = attr.ib()
    res_number: Number = attr.ib()
    opaccity: float = attr.ib(default=0.0)
    temperature: float = attr.ib(default=0.0)

    def __attrs_post_init__(self):
        self.element: str = self.atom_name.element_name()

    def asCif(self) -> str:
        return "".join([
            "ATOM ",
            self.atom_number.as_str().ljust(12, " "),
            self.element.ljust(2, " "),
            self.atom_name.as_cif().ljust(6, " "),
            ". ",
            self.res_name.as_str().ljust(3, " "),
            self.chain_id.as_cif().ljust(3, " "),
            self.chain_id.as_str().ljust(4, " "),
            self.res_number.as_str().ljust(6, " "),
            "? ",
            "{: .3f}".format(self.atom_coor[0]).rjust(8, " "),
            "{: .3f}".format(self.atom_coor[1]).rjust(8, " "),
            "{: .3f}".format(self.atom_coor[2]).rjust(8, " "),
            "{: .2f}".format(self.opaccity).rjust(6, " "),
            "{: .2f}".format(self.temperature).rjust(6, " "),
            "? ",
            self.res_number.as_str().ljust(6, " "),
            self.res_name.as_str().ljust(3, " "),
            self.chain_id.as_chimera().ljust(3, " "),
            self.atom_name.as_cif().ljust(6, " "),
            "1"
        ])

    def asPdb(self) -> str:
        return "".join([
            "ATOM  ",
            self.atom_number.as_pdb4namd(width=5),
            self.atom_name.as_pdb4namd(width=5),
            self.res_name.as_pdb4namd(width=4),
            self.chain_id.as_pdb4namd(width=2),
            self.res_number.as_pdb4namd(width=4),
            (4 * " "),
            "{: .3f}".format(self.atom_coor[0]).rjust(8, " "),
            "{: .3f}".format(self.atom_coor[1]).rjust(8, " "),
            "{: .3f}".format(self.atom_coor[2]).rjust(8, " "),
            "{: .2f}".format(self.opaccity).rjust(6, " "),
            "{: .2f}".format(self.temperature).rjust(6, " "),
            (6 * " "),
            self.chain_id.as_segName4namd(width=4),
            self.element,
            (2 * " "),  # charge
        ])
