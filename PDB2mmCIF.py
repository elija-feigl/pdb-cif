#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import attr

from pathlib import Path

from core.structure import Structure


__authors__ = "[Elija Feigl]"
__credits__ = "hybrid36: Ralf W. Grosse-Kunstleve"
__version__ = "0.7"
__license__ = "GPL-3.0"
__status__ = "Development"
__descr__ = "namd (enrgMD) PDB to chimera PDB."


@attr.s(slots=True)
class Args(object):
    input: Path = attr.ib()
    remove_H: bool = attr.ib()


def proc_input() -> Args:
    def get_description() -> str:
        return __descr__

    def add_arguments(p: argparse.ArgumentParser) -> None:
        p.add_argument(dest="input",
                       help="input file",
                       type=str,
                       default=argparse.SUPPRESS,
                       )
        p.add_argument("-H", "--hydrogen",
                       dest="hydrogen",
                       help="remove hydrogen atoms?",
                       action="store_false",
                       default=True
                       )

    parser = argparse.ArgumentParser(
        description=get_description(),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    add_arguments(parser)
    parse = parser.parse_args()
    return Args(input=Path(parse.input),
                remove_H=parse.hydrogen,
                )


def main():
    args = proc_input()

    structure = Structure(filename=args.input, remove_H=args.remove_H)
    if structure.filename.suffix == ".pdb":
        structure.parse_pdb()
        # TODO: -low- ask for additional info (name, author, etc)
        output_name = args.input.with_suffix(".cif")
        structure.write_cif(output_name)
    elif structure.filename.suffix == ".cif":
        structure.parse_pdb()
        output_name = args.input.with_suffix(".pdb")
        structure.write_pdb(output_name)
    else:
        raise IOError


if __name__ == "__main__":
    main()
