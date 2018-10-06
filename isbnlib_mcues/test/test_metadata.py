# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file
"""nose tests for metadata."""

from nose.tools import assert_equals
from isbnlib import meta
from .._mcues import query


def test_query():
    """Test the query of metadata (mcu.es) with 'low level' queries."""
    assert_equals(len(repr(query('9781849692341'))) == 2, True)
    assert_equals(len(repr(query('9781849692343'))) == 2, True)

    assert_equals(len(repr(query('9788491043508'))) > 100, True)
    assert_equals(len(repr(query('9788437604947'))) > 100, True)
    assert_equals(len(repr(query('9788474234046'))) > 100, True)

    assert_equals(len(repr(query('9780000000'))) == 2, True)


# def test_ext_meta():
#    """Test the query of metadata (mcu.es) with 'high level' meta function."""
#    # test meta from core
#    assert_equals(len(repr(meta('9789727576807', 'porbase'))) > 100, True)

test_query()
