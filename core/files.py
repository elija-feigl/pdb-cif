#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


import attr

from pathlib import Path
from typing import List, TextIO
try:
    import importlib.resources as resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as resources

from core import cif_templates


@attr.s
class PDB(object):
    struct: "Structure" = attr.ib()

    def __attrs_post_init__(self):
        # TODO: get box from struct
        self.box = "1000.000 1000.000 1000.000"
        # TODO: add additional info

    def _header(self) -> List[str]:
        return ["HEADER   "]

    def _authors(self) -> List[str]:
        return ["AUTHOR   "]

    def _remarks(self) -> List[str]:
        return ["REMARK   "]

    def _box(self) -> List[str]:
        angles = "90.00  90.00  90.00"
        space_group = "P 1"
        z_value = "1"
        return ["CRYST1 {}  {} {}           {}".format(
            self.box, angles, space_group, z_value,)]

    def _atoms(self) -> List[str]:
        return [atom.asPdb() for atom in self.struct.atoms]

    def write(self, outfile: Path) -> None:
        with open(outfile, mode="w+") as of:
            for part in [
                    self._header(),
                    self._authors(),
                    self._remarks(),
                    self._box(),
                    self._atoms(),
            ]:
                of.writelines(part)


@attr.s
class CIF(object):
    struct: "Structure" = attr.ib()

    def __attrs_post_init__(self):
        self.atoms: List[str] = self._set_atoms()
        # TODO: add additional info

    def _set_atoms(self) -> List[str]:
        return [atom.asCif() for atom in self.struct.atoms]

    def _write_atoms(self, fo: TextIO) -> None:
        atom_header = resources.read_text(cif_templates, 'atom_header.txt')

        fo.write(atom_header)
        fo.writelines(self.atoms)

    def write(self, outfile: Path) -> None:
        close_section = "#\n"

        with open(outfile, mode="w+") as fo:
            self._write_atoms(fo)
            fo.write(close_section)
