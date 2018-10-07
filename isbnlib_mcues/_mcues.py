# -*- coding: utf-8 -*-
"""Query the http://www.mcu.es/webISBN service for
Spanish ISBN database metadata."""

import logging
import re
from isbnlib.dev import stdmeta
from isbnlib.dev._bouth23 import u
from ._mcueswebservice import query as wquery

UA = 'isbnlib (gzip)'
SERVICE_URL = 'http://www.mcu.es/webISBN/tituloSimpleDispatch.do?cache=init&prev_layout=busquedaisbn&layout=busquedaisbn&language=es&params.cisbnExt={isbn}&action=Buscar'
LOGGER = logging.getLogger(__name__)


def parser_mcues(data):
    """Parse the response from the MCU service. The input data is the result webpage in html from the search."""
    data = re.split('\n', data)  # split into lines for loop
    recs = {}
    recs['Authors'] = [
    ]  # this should be an array, otherwise stdmeta gives a NotValidMetadataError
    try:
        for line in data:
            line = line.replace('\n', ' ')  # remove carriage return
            if len(recs) == 4:  # skip the rest of the file if we have all recs
                break
            # Author:
            #                     <strong>Garc<ED>a M<E1>rquez, Gabriel (1928- )</strong>
            elif re.search(r"\s{10}<strong>.+</strong>", line):
                authors = re.findall('>.+<', line)[0]
                authors = u(
                    authors.replace('>', '').replace('<', '').split('(')[0])
                recs['Authors'].append(authors)
            # Publisher:
            #<a href="/webISBN/editorialDetalle.do?sidEditorial=2399&amp;action=busquedaInicial&amp;noValidating=true&amp;POS=0&amp;MAX=50&amp;TOTAL=0&amp;prev_layout=busquedaisbn&amp;layout=busquedaeditoriales&amp;language=es" tabindex="107">Ediciones C<E1>tedra, S.A.</a>
            elif re.search('tabindex=\"107\">', line):
                publisher = re.findall('>.+<', line)[0]
                recs['Publisher'] = u(
                    publisher.replace('>', '').replace('<', ''))
            # Title:
            #<a href="/webISBN/tituloDetalle.do?sidTitul=384067&amp;action=busquedaInicial&amp;noValidating=true&amp;POS=0&amp;MAX=50&amp;TOTAL=0&amp;prev_layout=busquedaisbn&amp;layout=busquedaisbn&amp;language=es" tabindex="106">Cien a<F1>os de soledad</a>
            elif re.search('tabindex=\"106\">', line):
                title = re.findall('>.+<', line)[0]
                recs['Title'] = u(title.replace('>', '').replace('<', ''))
            # Publication year:
            # &nbsp;&nbsp;(1987)&nbsp;&nbsp;</strong>
            #elif re.search('\&nbsp\;\&nbsp\;\(\d{4}\)\&nbsp\;\&nbsp\;', line):
            elif re.search(r'\(\d{4}\)', line):
                recs['Year'] = u(re.findall(r'\d{4}', line)[0])
            elif line == '':
                continue

    except IndexError:
        LOGGER.debug('Check the parsing for Spanish MCU (possible error!)')
    try:
        # delete almost empty records
        if not recs['Title'] and not recs['Authors']:
            recs = {}
    except KeyError:
        recs = {}
    return recs


def _mapper(isbn, records):
    """Make records canonical.
    canonical: ISBN-13, Title, Authors, Publisher, Year, Language
    """
    # handle special case
    if not records:  # pragma: no cover
        return {}
    # add ISBN-13
    records['ISBN-13'] = u(isbn)
    # call stdmeta for extra cleaning and validation
    return stdmeta(records)


def query(isbn):
    """Query the Spanish MCU service for metadata. """
    data = parser_mcues(wquery(SERVICE_URL.format(isbn=isbn), user_agent=UA))
    if not data:  # pragma: no cover
        LOGGER.debug('No data from MCU for isbn %s', isbn)
        return {}
    return _mapper(isbn, data)
