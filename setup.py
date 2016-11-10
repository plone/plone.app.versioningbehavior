# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

import os

version = '2.0.0.dev0'

tests_require = [
    'plone.app.dexterity',
    'plone.app.testing',
    'plone.app.testing',
    'plone.namedfile[blobs]',
    'Products.CMFDiffTool',
    'Products.CMFEditions [test]',
    'Products.CMFPlone',
    'zope.app.intid',
]

setup(
    name='plone.app.versioningbehavior',
    version=version,
    description=('Provides a behavior for using CMFEditions with '
                 'dexterity content types'),
    long_description=(open("README.rst").read() + "\n" +
                      open(os.path.join("CHANGES.rst")).read()),
    # Get more strings from
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 5.1',
        'Framework :: Zope2',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='plone dexterity behavior versioning CMFEditions',
    author='Jonas Baumann, 4teamwork GmbH',
    author_email='mailto:dexterity-development@googlegroups.com',
    url='https://pypi.org/project/plone.app.versioningbehavior',
    license='GPL version 2',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['plone', 'plone.app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.app.dexterity[relations]',
        'plone.autoform',
        'plone.dexterity>=2.0',
        'plone.namedfile',
        'plone.rfc822',
        'Products.CMFEditions>2.2.9',
        'setuptools',
        'zope.container',
    ],
    tests_require=tests_require,
    extras_require=dict(tests=tests_require),
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
