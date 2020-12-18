#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
from __future__ import annotations


import attr

from pathlib import Path
from typing import List, TextIO, TYPE_CHECKING, Dict, Tuple
if TYPE_CHECKING:
    from core.structure import Structure
try:
    import importlib.resources as resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as resources

from core import cif_templates
from core.types import ChainID, ResName


@attr.s
class PDB(object):
    struct: Structure = attr.ib()

    def __attrs_post_init__(self):
        # TODO: get box from struct
        self.box = "1000.000 1000.000 1000.000"

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
    struct: Structure = attr.ib()

    def __attrs_post_init__(self):
        self.atoms: List[str] = self._set_atoms()
        self.chains, self.seqs = self._get_chains_seqs()

    def _set_atoms(self) -> List[str]:
        return [atom.asCif() for atom in self.struct.atoms]

    def _get_chains_seqs(self) -> Tuple[
            Dict[int, int], Dict[int, List[ResName]]]:
        chains: Dict[int, int] = dict()
        seqs: Dict[int, List[ResName]] = dict()
        C3ps = [a for a in self.struct.atoms if a.atom_name.as_str() == "C3\'"]
        for a in C3ps:
            chain_id = a.chain_id.n
            res_number = a.res_number.n

            if chain_id not in chains:
                chains[chain_id] = res_number
            elif res_number > chains[chain_id]:
                chains[chain_id] = res_number

            if chain_id not in seqs:  # only res not atom
                seqs[chain_id] = [a.res_name]
            else:
                seqs[chain_id].append(a.res_name)

        return chains, seqs

    def _write_atoms(self, fo: TextIO) -> None:
        atom_header = resources.read_text(cif_templates, "atom_header.txt")
        fo.write(atom_header)
        fo.writelines(self.atoms)

    def _write_header(self, fo: TextIO) -> None:
        header = resources.read_text(cif_templates, "header.txt")
        fo.write("data_{}\n".format(self.struct.name))
        fo.write(header)

    def _write_pdbx_struct(self, fo: TextIO) -> None:
        pdbx_struct = resources.read_text(cif_templates, "pdbx_struct.txt")
        pdbx_struct = pdbx_struct.replace("NCHAINS", str(len(self.chains)))
        fo.write(pdbx_struct)

    def _write_entity(self, fo: TextIO) -> None:
        entity = resources.read_text(cif_templates, "entity.txt")
        fo.write(entity)
        for chain_id, length in self.chains.items():
            is_staple = (length < 500)
            n = str(chain_id).ljust(4)
            src = "syn" if is_staple else "?  "
            typ = "\'STAPLE STRAND\'  " if is_staple else "\'SCAFFOLD STRAND\'"
            fo.write("{} polymer {} {} ?   1 ? ? ? ?\n".format(n, src, typ))

    def _write_entity_src(self, fo: TextIO) -> None:
        entity_src = resources.read_text(cif_templates, "entity_src.txt")
        fo.write(entity_src)
        for chain_id, length in self.chains.items():
            is_staple = (length < 500)
            n = str(chain_id).ljust(4)
            typ = "\'synthetic construct\'" if is_staple else "?".ljust(21)
            tax = "32630" if is_staple else "?".ljust(5)
            fo.write("{}   1 sample 1 {} {} ? {} ?\n".format(
                n, str(length).ljust(5), typ, tax))

    def _write_entity_poly(self, fo: TextIO) -> None:
        entity_poly = resources.read_text(cif_templates, "entity_poly.txt")
        fo.write(entity_poly)
        for chain_id, seq in self.seqs.items():
            n = str(chain_id).ljust(4)
            cid = ChainID(chain_id).as_chimera()
            seq1 = "".join(["({})".format(s.as_str()) for s in seq])
            seq2 = "".join([s.as_X() for s in seq])
            fo.write(
                "{} polydeoxyribonucleotide no no\n;{}\n;\n{} {} ?\n".format(
                    n, seq1, seq2, cid)
            )

    def write(self, outfile: Path) -> None:
        with open(outfile, mode="w+") as fo:
            self._write_header(fo)
            self._write_pdbx_struct(fo)
            self._write_atoms(fo)
            self._write_entity(fo)
            self._write_entity_src(fo)
            self._write_entity_poly(fo)
