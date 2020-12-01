#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import attr

from pathlib import Path

from core.structure import Structure


__authors__ = "[Elija Feigl]"
__credits__ = "pdbCorrection.py: Thomas Martin, Ana Casanal, Elija Feigl"
__version__ = "0.5"


@attr.s(slots=True)
class Args(object):
    input: Path = attr.ib()
    output: Path = attr.ib()
    pdb2cif: bool = attr.ib()


def proc_input() -> Args:
    def get_description() -> str:
        return "namd (enrgMD) PDB to chimera PDB."

    def add_arguments(p: argparse.ArgumentParser) -> None:
        p.add_argument("--input",
                       help="input file",
                       type=str,
                       required=True,
                       default=argparse.SUPPRESS,
                       )
        p.add_argument("--output",
                       help="output file",
                       type=str,
                       required=True,
                       default=argparse.SUPPRESS,
                       )
        p.add_argument("--pdb2cif",
                       help="prep for cif-generation (overrides others)",
                       action="store_true"
                       )
    parser = argparse.ArgumentParser(
        description=get_description(),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    add_arguments(parser)
    parse = parser.parse_args()
    return Args(input=Path(parse.input),
                output=Path(parse.output),
                pdb2cif=parse.pdb2cif,
                )


def main():
    args = proc_input()

    structure = Structure(filename=args.input)
    if structure.filename.suffix == ".pdb":
        structure.parse_pdb()
        # TODO: -low- ask for additional info (name etc)
        structure.write_cif(args.output)
    elif structure.filename.suffix == ".cif":
        structure.parse_pdb()
        structure.write_pdb(args.output)
    else:
        raise IOError


if __name__ == "__main__":
    main()
