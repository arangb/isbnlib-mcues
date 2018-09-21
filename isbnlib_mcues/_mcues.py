# -*- coding: utf-8 -*-
"""Query the http://www.mcu.es/webISBN/tituloSimpleFilter.do service for Spanish ISBN database metadata."""


import logging
import re
from isbnlib.dev import stdmeta
from isbnlib.dev._bouth23 import u

UA = 'isbnlib (gzip)'
SERVICE_URL = 'http://www.mcu.es/webISBN/tituloSimpleFilter.do?cache=init&prev_layout=busquedaisbn&layout=busquedaisbn&language=es'
LOGGER = logging.getLogger(__name__)

def parser_mcues(data):
    """Parse the response from the MCU service. The data will be an array with each line as a string of the output webpage"""
    recs={}
    recs['Authors']=[] # this should be an array, otherwise stdmeta gives a NotValidMetadataError
    try:
		for line in data:
			line = line.replace('\n',' ') # remove carriage return
			if len(recs)==4:
				break
			# Author:
			#                     <strong>Garc<ED>a M<E1>rquez, Gabriel (1928- )</strong>
			elif re.search("\s{10}<strong>.+</strong>", line):
				authors=re.findall('>.+<',line)[0]
				authors=u(authors.replace('>','').replace('<',''))
				recs['Authors'].append(authors)
			# Publisher:
			#<a href="/webISBN/editorialDetalle.do?sidEditorial=2399&amp;action=busquedaInicial&amp;noValidating=true&amp;POS=0&amp;MAX=50&amp;TOTAL=0&amp;prev_layout=busquedaisbn&amp;layout=busquedaeditoriales&amp;language=es" tabindex="107">Ediciones C<E1>tedra, S.A.</a>
			elif re.search('tabindex=\"107\">', line):
				publisher=re.findall('>.+<',line)[0]
				recs['Publisher']=u(publisher.replace('>','').replace('<',''))
			# Title:
			#<a href="/webISBN/tituloDetalle.do?sidTitul=384067&amp;action=busquedaInicial&amp;noValidating=true&amp;POS=0&amp;MAX=50&amp;TOTAL=0&amp;prev_layout=busquedaisbn&amp;layout=busquedaisbn&amp;language=es" tabindex="106">Cien a<F1>os de soledad</a>
			elif re.search('tabindex=\"106\">', line):
				title=re.findall('>.+<',line)[0]
				recs['Title']=u(title.replace('>','').replace('<',''))
			# Publication year:
			# &nbsp;&nbsp;(1987)&nbsp;&nbsp;</strong>
			#elif re.search('\&nbsp\;\&nbsp\;\(\d{4}\)\&nbsp\;\&nbsp\;', line):
			elif re.search('\(\d{4}\)', line):
				recs['Year']=u(re.findall('\d{4}',line)[0])
			elif line == '':
				continue
    
    except IndexError:
        LOGGER.debug('Check the parsing for Spanish MCU (possible error!)')
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
    """Query the Spanish MCU service for metadata. This service is not an API, it doesn't return a JSON or xml that we can easily parse. We need to submit the ISBN in a form on the website and then parse the resulting webpage. I could not make it work just using urllib and urllib2, so I need to use the module mechanicalsoup that works in Python2 and 3. To install: sudo pip install mechanicalsoup"""
    import mechanicalsoup
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(SERVICE_URL)
    # Fill-in the search form
    browser.select_form('#libroBusquedaSimpleForm')
    browser["params.cisbnExt"] = isbn 
    browser.submit_selected()
    # Check we got back a correct webpage: Any "Aviso importante" means there was an error with that ISBN.
    if len(browser.get_current_page().findAll(text=re.compile('Aviso importante')))>0:
    #'no es un ISBN válido. Acuda a la ayuda para observar los formatos válidos'):  # pragma: no cover
    #'No se ha encontrado ningún resultado. Modifique los parámetros para ampliar el campo de búsqueda.'
        LOGGER.debug('No data from Spanish MCU for isbn %s', isbn)
        return {}
    
    # Could use the BeautifulSoup methods to parse the output faster?
    #print browser.get_current_page().select_one("a[tabindex=106]") # Authors
    #print browser.get_current_page().select_one("a[href*=editorialDetalle]") # Publishers
    
    response_web=str(browser.get_current_page()) # just get the raw text (things like &nbsp; will be lost)
    result_lines = re.split('\n',response_web) # ok, now we have a list of each line in the webpage
    recs = parser_mcues(result_lines) # send it to the parser
    
    return _mapper(isbn, recs)
