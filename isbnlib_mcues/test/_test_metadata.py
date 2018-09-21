# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file
"""Simple checks with a few examples. Just to see if it works."""

from nose.tools import assert_equals
import isbnlib
from _mcues import query

def test_mcu():
	# print(query('9788474335255'))
	# print(query('9788499083728')) # Two authors separated by ';'
	# print(query('9788491043508')) # Los tres primeros minutos sin acentos
	print(query('9788437604947'))  # Cien años de soledad
	# print(query('9788496208964')) # George Martin editorial sale mal en campo 108 en vez de 107
	# print(query('9788492510283')) 
	
def test_mcu_long():	
	for e in ['9788425208805','9788425208171','9788425208829','9788425208188','9788425208195','9788400000165','9788472731103','9788474332605','9788478121816','9788496387065','9788400070847','9788486763183']:	#['9788474838190','9788450547948','9788484480020','9788450054026','8489034869','9788432304279','9788478125548','9788472143203''9788474234152','9788450551099','9788476355329','9788476351970','9788474968446','9788474234046','9788420622958','9788474232950','9788474230581','9788434465510','9788480951951','9788477823421','9788472143265','9788487159886']:	
		if isbnlib._core.is_isbn10(e):
			e=isbnlib._core.to_isbn13(e)
			print(e)
		print(query(e))

test_mcu()
