#!/usr/bin/env python
# -*- coding: utf-8 -*-

import attr

from pathlib import Path
from typing import Dict, List

from atom import Atom


@attr.s
class Structure(object):
    filename: Path = attr.ib()
    atoms: Dict[int, Atom] = dict()
    # TODO: default and slot other atributs

    def add_atom(self, atom: Atom) -> None:
        self.atoms[atom.atom_number.n] = atom

    def _parse_cif_info(self):
        raise NotImplementedError

    def _parse_cif_atom(self):
        raise NotImplementedError

    def parse_cif(self) -> None:
        self._parse_cif_info()
        self._parse_cif_atom()
        raise NotImplementedError

    def _parse_pdb_info(self):
        raise NotImplementedError

    def _parse_pdb_atom(self):
        raise NotImplementedError

    def _parse_pdb_generate_info(self):
        # generate sequences etc
        raise NotImplementedError

    def parse_pdb(self) -> None:
        self._parse_pdb_info()
        self._parse_pdb_atom()
        self._parse_pdb_generate_info()
        raise NotImplementedError

    def write_pdb(self, outfile: Path) -> None:
        pdb = PDB(self)
        pdb.write(outfile=outfile)

    def write_cif(self, outfile: Path) -> None:
        # generate sequences here (from atom)
        cif = CIF(self)
        cif.write(outfile=outfile)


class PDB(object):
    struct: Structure = attr.ib()

    def __attrs_post_init__(self):
        self.header: List[str] = self._set_header()
        self.authors: List[str] = self._set_authors()
        self.remarks: List[str] = self._set_remarks()
        self.box: List[str] == self._set_box()
        self.atoms: List[str] = self._set_atoms()

    def _set_header(self) -> List[str]:
        return ["HEADER   "]

    def _set_authors(self) -> List[str]:
        return ["AUTHOR   "]

    def _set_remarks(self) -> List[str]:
        return ["REMARK   "]

    def _set_box(self) -> List[str]:
        return ["CRYST1 1000.000 1000.000 1000.000  90.00  90.00  90.00 P 1           1"]

    def _set_atoms(self) -> List[str]:
        return [atom.asPdb() for atom in self.struct.atoms]

    def write(self, outfile: Path) -> None:
        with open(outfile) as of:
            for part in [
                    self.header,
                    self.authors,
                    self.remarks,
                    self.box,
                    self.atoms,
            ]:
                of.writelines(part)


class CIF(object):
    struct: Structure = attr.ib()

    def __attrs_post_init__(self):
        self.atoms: List[str] = self._set_atoms()
        # TODO: add other info

    def _set_atoms(self) -> List[str]:
        atom_header = ["_loop"]
        atoms = [atom.asCif() for atom in self.struct.atoms]
        return atom_header + atoms

    def write(self, outfile: Path) -> None:
        with open(outfile) as of:
            for part in [
                    # TODO: add other info
                    self.atoms,
            ]:
                of.writelines(part)
