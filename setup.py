# -*- coding: utf-8 -*-

"""isbnlib-mcues -- an isbnlib plugin for the Ministerio de Cultura of Spain database server."""


from setuptools import setup


setup(
    name='isbnlib-mcues',
    version='0.0.1',
    author='Aran Garcia-Bellido',
    author_email='arangbellido@gmail.com',
    url='_____________________________________',
    download_url='___________________________________',
    packages=['isbnlib_mcues/'],
    entry_points = {
        'isbnlib.metadata': ['isbnmcues=isbnlib_mcues:query']
    },
    install_requires=["isbnlib>=3.8.3,<3.9.0"],
    license='LGPL v3',
    description='An isbnlib plugin for the Ministerio de Cultura of Spain database server.',
    keywords='ISBN, isbnlib, MCU, Spain',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console',
        'Topic :: Text Processing :: General',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
