# -*- coding: utf-8 -*-
"""Query MCUES web service."""

import gzip
import logging
from time import sleep, time as timestamp

from isbnlib.dev._bouth23 import bstream, s
from isbnlib.dev.webservice import WEBService

UA = 'isbnlib (gzip)'
LOGGER = logging.getLogger(__name__)
THROTTLING = 1


# pylint: disable=too-few-public-methods
class McuesWEBService(WEBService):
    """Class to query MCUES web service."""

    T = 0.0  # seconds

    def __init__(self, url, user_agent=UA):
        """Initialize and throttle the service."""
        last = McuesWEBService.T
        wait = 0 if timestamp() - last > THROTTLING else THROTTLING
        sleep(wait)
        WEBService.__init__(self, url, user_agent=UA)
        McuesWEBService.T = timestamp()

    def data(self):
        """Return the uncompressed data."""
        res = super(McuesWEBService, self).response()
        LOGGER.debug('Response headers:\n%s', res.info())
        data = res.read()
        if res.info().get('Content-Encoding') == 'gzip':
            buf = bstream(data)
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
        return s(data.decode('iso-8859-1').encode('utf-8'))


def query(url, user_agent=UA):
    """Query the MCUES web service."""
    service = McuesWEBService(url, user_agent=user_agent)
    data = service.data()
    LOGGER.debug('Raw data from service:\n%s', data)
    return data
