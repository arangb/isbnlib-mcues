# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file
"""Simple checks with a few examples. Just to see if it works.
To run: python3 -m isbnlib_mcues.test.simpletest   # no .py at the end"""

from nose.tools import assert_equals
import isbnlib
from .._mcues import query


def test_mcu():
    """Simple tests for some remarkable cases."""
    print(query('9788474335255'))
    print(query('9788499083728'))  # Two authors separated by ';'
    print(query('9788491043508'))  # Los tres primeros minutos sin acentos
    print(query('9788437604947'))  # Cien años de soledad
    print(query('9788496208421')) # Cancion de fuego y hielo (ISBN gives two results)
    print(query('9788496208964')) # Juego de tronos, parte the la anterior. Publisher field is wrong: appears in tabindex=108 and not in 107
    print(query('9788492510283'))
    print(query('8489034869')) # this ISBN-10 doesn't return a hit in MCU

test_mcu()
