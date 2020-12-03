#!/usr/bin/env python
# -*- coding: utf-8 -*-

import attr
# TODO: remove numpy for ccompatibility
import numpy as np
from typing import Union, List, Tuple

from core.types import Number, AtomName, ResName, ChainID


@attr.s
class Atom(object):
    i_atom_coor: Union[np.ndarray, Tuple[str, str, str],
                       Tuple[float, float, float]] = attr.ib()
    i_atom_number: Union[int, str] = attr.ib()
    i_atom_name: str = attr.ib()
    i_res_name: str = attr.ib()
    i_chain_id: Union[int, str] = attr.ib()
    i_res_number: Union[int, str] = attr.ib()
    i_opaccity: Union[float, str] = attr.ib(default=0.0)
    i_temperature: Union[float, str] = attr.ib(default=0.0)

    def __attrs_post_init__(self):
        self.atom_coor: np.ndarray = self._convert_coor_input(self.i_atom_coor)
        self.atom_number: Number = Number(self.i_atom_number)
        self.atom_name: AtomName = AtomName(self.i_atom_name)
        self.res_name: ResName = ResName(self.i_res_name)
        self.chain_id: ChainID = ChainID(self.i_chain_id)
        self.res_number: Number = Number(self.i_res_number)
        self.opaccity: float = float(self.i_opaccity)
        self.temperature: float = float(self.i_temperature)
        self.element: str = self.atom_name.element_name()

    def _convert_coor_input(
            self, inpt: Union[np.ndarray, List[Union[str, float]]]
    ) -> np.ndarray:
        if isinstance(inpt, np.ndarray):
            return inpt
        elif isinstance(inpt, list):
            coor = [(float(c) if isinstance(c, str) else c) for c in inpt]
            return np.array(coor)
        else:
            raise NotImplementedError

    def asCif(self) -> str:
        return "".join([
            "ATOM ",
            self.atom_number.as_str().ljust(12, " "),
            self.element.ljust(2, " "),
            self.atom_name.as_cif().ljust(7, " "),
            ". ",
            self.res_name.as_str().ljust(3, " "),
            self.chain_id.as_cif().ljust(3, " "),
            self.chain_id.as_str().ljust(4, " "),
            self.res_number.as_str().ljust(6, " "),
            "? ",
            "{: .3f}".format(self.atom_coor[0]).ljust(8, " "),
            "{: .3f}".format(self.atom_coor[1]).ljust(8, " "),
            "{: .3f}".format(self.atom_coor[2]).ljust(8, " "),
            "{: .2f}".format(self.opaccity).ljust(6, " "),
            "{: .2f}".format(self.temperature).ljust(6, " "),
            "? ",
            self.res_number.as_str().ljust(6, " "),
            self.res_name.as_str().ljust(3, " "),
            self.chain_id.as_chimera().ljust(3, " "),
            self.atom_name.as_cif().ljust(7, " "),
            "1",
            "\n",
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
            "\n",
        ])
