#!/usr/bin/env python
# -*- coding: utf-8 -*-


def h36_2_int(number: str) -> int:
    """ hybrid36 string format to integer"""
    # TODO: -low- as cif has int and namd has to be recalculated fo enrgMD
    # script. (server is h36)
    raise NotImplementedError


def int_2_h36(number: int, width: int) -> str:
    """ integer to hybrid36 string
        authors:  Thomas Martin, Ana Casanal """
    digits_upper = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits_lower = digits_upper.lower()

    def encode_pure(digits: str, value: int) -> str:
        "encodes value using the given digits"
        assert value >= 0
        if (value == 0):
            return digits[0]
        n = len(digits)
        result = []
        while (value != 0):
            rest = value // n
            result.append(digits[value - rest * n])
            value = rest
        result.reverse()
        return "".join(result)

    if (number >= 1 - 10**(width - 1)):
        if (number < 10**width):
            return "{:{width}d}".format(number, width=width)
        number -= 10**width
        if (number < 26 * 36**(width - 1)):
            number += 10 * 36**(width - 1)
            return encode_pure(digits_upper, number)
        number -= 26 * 36**(width - 1)
        if (number < 26 * 36**(width - 1)):
            number += 10 * 36**(width - 1)
            return encode_pure(digits_lower, number)
    raise ValueError("value out of range.")


POS_CHAR = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
POS_CHAIN_IDS = []
for c1 in POS_CHAR:
    for c2 in POS_CHAR:
        POS_CHAIN_IDS.append(c1 + c2)


def int_2_cifSegID(number: int) -> str:
    return ""


def int_2_chimeraSegID(number: int) -> str:
    return ""
